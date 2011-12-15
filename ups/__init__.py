import logging
logger = logging.getLogger(__name__)

import datetime
import StringIO
import binascii
import urllib2

SERVICES = [
    ('03', 'UPS Ground'),
    ('11', 'UPS Standard'),
    ('01', 'UPS Next Day'),
    ('14', 'UPS Next Day AM'),
    ('13', 'UPS Next Day Air Saver'),
    ('02', 'UPS 2nd Day'),
    ('59', 'UPS 2nd Day AM'),
    ('12', 'UPS 3-day Select'),
    ('65', 'UPS Saver'),
    ('07', 'UPS Worldwide Express'),
    ('08', 'UPS Worldwide Expedited'),
    ('54', 'UPS Worldwide Express Plus'),
]

SERVICES_LOOKUP = dict(SERVICES)

PACKAGES = [
    ('02', 'Custom Packaging'),
    ('01', 'UPS Letter'),
    ('03', 'Tube'),
    ('04', 'PAK'),
    ('21', 'UPS Express Box'),
    ('2a', 'Small Express Box'),
    ('2b', 'Medium Express Box'),
    ('2c', 'Large Express Box'),
]

import accessrequest as access_xml
import raterequest as rate_xml
import rateresponse as rate_response_xml

import xavrequest as avs_xml
import xavresponse as avs_response_xml

# Dumbness that I have something name shipping somewhere else and this import needs to work both in the lib for testing and in my other library
import os.path
working_dir = os.path.dirname(__file__)
parent_dir = os.path.split(working_dir)[0]
root_namespace = os.path.split(parent_dir)[1]
if len(root_namespace) > 0:
   root_namespace += '.'
shipping = __import__(root_namespace + 'shipping')

class UPS(object):
   def __init__(self, credentials_dictionary={}, debug=True, username='', password='', account='', license=''):
      self.access = access_xml.AccessRequest()
      self.access.AccessLicenseNumber = credentials_dictionary.get('access_license', license)
      self.access.UserId = credentials_dictionary.get('username', username)
      self.access.Password = credentials_dictionary.get('password', password)
      
      self.account = credentials_dictionary.get('shipper_number', account)
      self.debug = debug
      self.request = None
      self.namespacedef = ''
      if self.debug:
         self.post_url = 'https://wwwcie.ups.com/ups.app/xml/'
      else:
         self.post_url = 'https://onlinetools.ups.com/ups.app/xml/'
      self.post_url_suffix = ''
      
   def make_shipper(self, namespace, from_address, ups_account):
      shipper = namespace.ShipperType()
      shipper.Name = from_address.company[:35]
      if len(shipper.Name) == 0:
         shipper.Name = from_address.name[:35]
      if ups_account and len(ups_account) > 0:
         shipper.ShipperNumber = ups_account
      else:
         # Fall back to the account from configuration
         shipper.ShipperNumber = self.account
      shipper.Address = namespace.AddressType()
      shipper.Address.AddressLine1 = from_address.address1
      shipper.Address.AddressLine2 = getattr(from_address, 'address2', '')
      shipper.Address.AddressLine3 = getattr(from_address, 'address3', '')
      shipper.Address.City = from_address.city
      if from_address.country in ('US', 'CA', 'IE'):
         shipper.Address.StateProvinceCode = from_address.state
      shipper.Address.PostalCode = from_address.zip
      shipper.Address.CountryCode = from_address.country
      if from_address.is_residence:
         shipper.Address.ResidentialAddressIndicator = ''
      return shipper
      
   def make_ship_to(self, namespace, to_address):
      ship_to = namespace.ShipToType()
      ship_to.Name = to_address.company[:35]
      if len(ship_to.Name) == 0:
         ship_to.Name = to_address.name[:35]
      ship_to.Address = namespace.AddressType()
      ship_to.Address.AddressLine1 = to_address.address1
      ship_to.Address.AddressLine2 = getattr(to_address, 'address2', '')
      ship_to.Address.AddressLine3 = getattr(to_address, 'address3', '')
      ship_to.Address.City = to_address.city
      if to_address.country in ('US', 'CA', 'IE'):
         ship_to.Address.StateProvinceCode = to_address.state
      ship_to.Address.PostalCode = to_address.zip
      ship_to.Address.CountryCode = to_address.country
      if to_address.is_residence:
         ship_to.Address.ResidentialAddressIndicator = ''
      return ship_to
         
   def verify(self, address, transaction_id = None):
      self.post_url_suffix = 'XAV'
      self.request = avs_xml.AddressValidationRequest()
      self.request.Request = avs_xml.RequestType()
      self.request.Request.TransactionReference = avs_xml.TransactionReferenceType()
      if transaction_id != None:
         self.request.Request.TransactionReference.CustomerContext = str(transaction_id)
      else:
         self.request.Request.TransactionReference.CustomerContext = datetime.datetime.now().strftime('xav.%Y%m%d.%H%M%S')
      self.request.Request.RequestAction = 'XAV'
      self.request.Request.RequestOption = 3 # Address Validation w/ Classification (not documented in xml spec)
      
      # Do not set the regional request indicator if using address classification
      #self.request.RegionalRequestIndicator = ''
      
      # Maximum Result Candidates default is 15
      self.request.MaximumListSize = 5
      
      self.request.AddressKeyFormat = []
      address_info = avs_xml.AddressKeyFormatType()
      address_info.ConsigneeName = address.name
      address_info.AddressLine = [ address.address1, address.address2 ]
      address_info.PoliticalDivision2 = address.city
      address_info.PoliticalDivision1 = address.state
      address_info.PostcodePrimaryLow = address.zip
      address_info.CountryCode = address.country
      self.request.AddressKeyFormat.append(address_info)
      
      response = self.send()
      print response
      response_xml = avs_response_xml.parseString(response)
      
      parsed_response = {
         'status' : response_xml.Response.ResponseStatusDescription, 
         'transaction_id' : response_xml.Response.TransactionReference.CustomerContext,
         'candidates' : []}
         
      if response_xml.AddressClassification:
         parsed_response['class_code'] = response_xml.AddressClassification.Code
         parsed_response['class_description'] = response_xml.AddressClassification.Description
         
      parsed_response['valid'] = response_xml.ValidAddressIndicator == True
      parsed_response['ambiguous'] =  response_xml.AmbiguousAddressIndicator == True
      parsed_response['no_candidates'] = response_xml.NoCandidatesIndicator == True
      
      if not parsed_response['no_candidates']:
         for candidate in response_xml.AddressKeyFormat:
            name = candidate.ConsigneeName 
            if name == None:
               name = ''
            a = shipping.Address(
                  name,
                  candidate.AddressLine[0],
                  candidate.PoliticalDivision2,
                  candidate.PoliticalDivision1,
                  candidate.PostcodePrimaryLow,
                  candidate.CountryCode)
            if len(candidate.AddressLine) > 1:
               a.address2 = candidate.AddressLine[1]

            if a not in parsed_response['candidates']:
               parsed_response['candidates'].append(a)

      return parsed_response
      
   validate = verify
      
   def rate(self, packages, packaging_type, from_address, to_address, ups_account=None, rate_type='00', service_type=None, transaction_id=None):
      self.post_url_suffix = 'Rate'
      self.request = rate_xml.RatingServiceSelectionRequest()
      self.request.Request = rate_xml.RequestType()
      self.request.Request.TransactionReference = rate_xml.TransactionReferenceType()
      if transaction_id != None:
         self.request.Request.TransactionReference.CustomerContext = str(transaction_id)
      else:
         self.request.Request.TransactionReference.CustomerContext = datetime.datetime.now().strftime('rate.%Y%m%d.%H%M%S')
      self.request.Request.RequestAction = 'Rate'
      self.request.Request.RequestOption = 'Shop'
      
      self.request.PickupType = rate_xml.CodeType()
      self.request.PickupType.Code = '01' # Using Daily Pickup
         
      
      self.request.CustomerClassification = rate_xml.CodeType()
      self.request.CustomerClassification.Code = rate_type
      
      self.request.Shipment = rate_xml.ShipmentType()
      self.request.Shipment.RateInformation = rate_xml.RateInformationType()
      self.request.Shipment.RateInformation.NegotiatedRatesIndicator = ''
      if service_type:
         # Set the service type if needed
         self.request.Shipment.Service = rate_xml.CodeDescriptionType()
         self.request.Shipment.Service.Code = service_type
      
      self.request.Shipment.Shipper = self.make_shipper(rate_xml, from_address, ups_account)
      self.request.Shipment.ShipTo = self.make_ship_to(rate_xml, to_address)
      self.request.Shipment.Package = []
      
      for p in packages:
         package = rate_xml.PackageType()
         package.PackagingType  = rate_xml.PackagingTypeType()
         package.PackagingType.Code = packaging_type

         package.Dimensions = rate_xml.DimensionsType()
         package.Dimensions.UnitOfMeasurement = rate_xml.UnitOfMeasurementType()
         package.Dimensions.UnitOfMeasurement.Code = 'IN'  #Other choice is CM
         package.Dimensions.Length = p.length
         package.Dimensions.Width = p.width
         package.Dimensions.Height = p.height
         
         package.PackageWeight = rate_xml.WeightType()
         package.PackageWeight.UnitOfMeasurement = rate_xml.UnitOfMeasurementType()
         package.PackageWeight.UnitOfMeasurement.Code = 'LBS'  #Other choice is KGS
         package.PackageWeight.Weight = p.weight
         
         # Always declare a value for insurance when rating
         package.PackageServiceOptions = rate_xml.PackageServiceOptionsType()
         package.PackageServiceOptions.InsuredValue = rate_xml.InsuredValueType()
         package.PackageServiceOptions.InsuredValue.MonetaryValue = p.value or 100
         package.PackageServiceOptions.InsuredValue.CurrencyCode = 'USD'
         
         if p.require_signature:
            package.PackageServiceOptions.DeliveryConfirmation = rate_xml.DeliveryConfirmationType()
            # Valid values are: 
            #     1 - Delivery Confirmation; 
            #     2 - Delivery Confirmation Signature Required; 
            #     3 - Delivery Confirmation Adult Signature Required
            if type(p.require_signature) == int and p.require_signature in (1, 2, 3):
               package.PackageServiceOptions.DeliveryConfirmation.DCISType = p.require_signature
            else:
               # Pick 1 for signature required, 2 for adult signature.
               package.PackageServiceOptions.DeliveryConfirmation.DCISType = 1

         self.request.Shipment.Package.append(package)

      response = self.send()
      response_xml = rate_response_xml.parseString(response)
      
      info = []
      for r in response_xml.RatedShipment:
          try:
              cost = r.NegotiatedRateCharges.TotalCharge.MonetaryValue
          except AttributeError:
              cost = r.TotalCharges.MonetaryValue
          info.append({
              'service': SERVICES_LOOKUP.get(r.Service.Code, 'Unknown Service: {}'.format(r.Service.Code)),
              'package': '',
              'delivery_day': '',
              'cost': cost
          })
      
      parsed_response = {
         'status' : response_xml.Response.ResponseStatusDescription, 
         'transaction_id' : response_xml.Response.TransactionReference.CustomerContext,
         'info' : info}
      
      return parsed_response

   def label(self, packages, packaging_type, service_type, from_address, to_address, email_alert=None, evening=False, payment=None, delivery_instructions=''):
      pass
      
   def send(self):
      data = StringIO.StringIO()
      data.write('<?xml version="1.0" ?>\n')
      self.access.export(data, 0, namespacedef_=self.namespacedef)
      data.write('<?xml version="1.0" ?>\n')
      self.request.export(data, 0, namespacedef_=self.namespacedef)
      data = data.getvalue()

      data = data.encode('ascii')
      logger.debug('XML Request:\n%s' % data)
      
      request = urllib2.Request(self.post_url + self.post_url_suffix)
      request.add_data(data)
      request.add_header('Accept', 'image/gif, image/jpeg, image/pjpeg, text/plain, text/html, */*')
      request.add_header('Content-Type', 'text/xml')
      request.add_header('Content-length', str(len(data)))
      
      # Get the response
      response = urllib2.urlopen(request)
      if response.code != 200:
         logger.error('HTTP Error %s' % str(response.code))
         raise Exception('HTTP Error %s' % str(response.code))
      
      response_data = response.read()
      logger.debug('XML Response:\n%s' % response_data)
      
      return response_data
      
Ups = UPS
