import logging
logger = logging.getLogger(__name__)
print __name__

import datetime
import StringIO
import binascii
import urllib2
import avs as avs_xml
import rate as rate_xml
import ship as ship_xml
import soapenvelope as soap_xml

SERVICES = [
      "EUROPE_FIRST_INTERNATIONAL_PRIORITY",
      "FEDEX_1_DAY_FREIGHT",
      "FEDEX_2_DAY",
      "FEDEX_2_DAY_AM",
      "FEDEX_2_DAY_FREIGHT",
      "FEDEX_3_DAY_FREIGHT",
      "FEDEX_EXPRESS_SAVER",
      "FEDEX_FIRST_FREIGHT",
      "FEDEX_FREIGHT_ECONOMY",
      "FEDEX_FREIGHT_PRIORITY",
      "FEDEX_GROUND",
      "FIRST_OVERNIGHT",
      "GROUND_HOME_DELIVERY",
      "INTERNATIONAL_ECONOMY",
      "INTERNATIONAL_ECONOMY_FREIGHT",
      "INTERNATIONAL_FIRST",
      "INTERNATIONAL_PRIORITY",
      "INTERNATIONAL_PRIORITY_FREIGHT",
      "PRIORITY_OVERNIGHT",
      "SMART_POST",
      "STANDARD_OVERNIGHT",
]

PACKAGES = [
    'FEDEX_BOX',
    'FEDEX_ENVELOPE',
    'FEDEX_PAK',
    'FEDEX_TUBE',
    'YOUR_PACKAGING',
]

class FedexError(Exception):
    pass

class FedexWebError(FedexError):
    def __init__(self, fault, document):
        self.fault = fault
        self.document = document
        
        fault = self.document.childAtPath('/Envelope/Body/Fault/detail/fault')
        code = fault.childAtPath('/errorCode').getText()
        reason = fault.childAtPath('/reason').getText()
        messages = fault.childrenAtPath('/details/ValidationFailureDetail/message')
        words = [ x.getText() for x in messages ]
        error_lines = '\n'.join(words)
        
        error_text = 'FedEx error %s: %s Details:\n%s ' % (code, reason, error_lines)
        super(FedexError, self).__init__(error_text)

class FedexShipError(FedexError):
    def __init__(self, reply):
        self.reply = reply
        messages = [ 'FedEx error %s: %s' % (x.Code, x.LocalizedMessage or x.Message) for x in reply.Notifications ]
        error_text = '\n'.join(messages)
        super(FedexError, self).__init__(error_text)

class FedEx(object):
   def __init__(self, credentials_dictionary={}, debug=True, key='', password='', account='', meter=''):
      self.key = credentials_dictionary.get('key', key)
      self.password = credentials_dictionary.get('password', password)
      self.account = credentials_dictionary.get('account_number', account)
      self.meter = credentials_dictionary.get('meter_number', meter)
      self.debug = debug
      self.request = None
      self.namespacedef = ''
      if self.debug:
         self.post_url = 'https://wsbeta.fedex.com:443/xml/'
      else:
         self.post_url = 'https://ws.fedex.com:443/xml/'
      self.post_url_suffix = ''
      
   def add_auth(self):
      self.request.WebAuthenticationDetail = ship.WebAuthenticationDetail()
      self.request.WebAuthenticationDetail.UserCredential = ship.WebAuthenticationCredential()
      self.request.WebAuthenticationDetail.UserCredential.Key = self.key      
      self.request.WebAuthenticationDetail.UserCredential.Password = self.password
      self.request.ClientDetail = ship.ClientDetail()
      self.request.ClientDetail.AccountNumber = self.account
      self.request.ClientDetail.MeterNumber = self.meter
      
   def add_version(self, service, major, intermediate = 0, minor = 0):
      self.request.Version = ship.VersionId()
      self.request.Version.ServiceId = service
      self.request.Version.Major = major
      self.request.Version.Intermediate = intermediate
      self.request.Version.Minor = minor
      
   def make_party(self, namespace, address, fedex_account = None, tax_id = None):
      party = namespace.Party()
      party.AccountNumber = fedex_account
      party.Contact = namespace.Contact()
      party.Contact.PersonName = address.name
      party.Contact.PhoneNumber = address.phone
      party.Contact.EMailAddress = address.email
      party.Address = namespace.Address()
      party.Address.StreetLines = [address.address1, address.address2 ]
      party.Address.City = address.city
      party.Address.StateOrProvinceCode = address.state
      party.Address.PostalCode = address.zip
      party.Address.CountryCode = address.country
      party.Address.Residential = address.is_residence
      return party
      
   def add_package(self, package):
      pass
      
   def verify(self, address):
      self.request = avs_xml.AddressValidationRequest()
      self.add_version('aval', 2, 0, 0)
      self.namespacedef = 'xmlns:ns="http://fedex.com/ws/addressvalidation/v2"'
      self.post_url_suffix = 'addressvalidation/'
      # Timestamp format =  YYYY-MM-DDTHH:MM:SS-xx:xx utc
      self.request.RequestTimestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-00:00')
      
      # Transaction Detail
      self.request.TransactionDetail = avs_xml.TransactionDetail()
      self.request.TransactionDetail.CustomerTransactionId = datetime.datetime.now().strftime('avs_xml.%Y%m%d.%H%M%S')
      
      # Validation Address
      self.request.AddressesToValidate = [avs_xml.AddressToValidate()]
      if len(address.company) > 0:
         self.request.AddressesToValidate[0].CompanyName = address.company
      self.request.AddressesToValidate[0].Address = avs_xml.Address()
      self.request.AddressesToValidate[0].Address.StreetLines = [address.street1, address.street2]
      self.request.AddressesToValidate[0].Address.City = address.city
      self.request.AddressesToValidate[0].Address.StateOrProvinceCode = address.state
      self.request.AddressesToValidate[0].Address.PostalCode = address.zip
      #self.request.AddressesToValidate[0].Address.UrbanizationCode = address. # For Puerto Rico... not sure what to do about it right now
      if address.country == 'PR':
         logger.warning('Urbanization Code should be used for Puerto Rico.')
      self.request.AddressesToValidate[0].Address.CountryCode = address.country
      
      # Validation Options
      self.request.Options = avs_xml.AddressValidationOptions()
      self.request.Options.VerifyAddresses = 1
      self.request.Options.CheckResidentialStatus = 1
      self.request.Options.MaximumNumberOfMatches = 3
      self.request.Options.StreetAccuracy = 'MEDIUM'
      self.request.Options.DirectionalAccuracy = 'MEDIUM'
      self.request.Options.CompanyNameAccuracy = 'LOOSE'
      self.request.Options.ConvertToUpperCase = 1
      self.request.Options.RecognizeAlternateCityNames = 1
      self.request.Options.ReturnParsedElements = 1
      
      response = self.send()
      return response
      
   def rate(self, packages, packaging_type, from_address, to_address, fedex_account=None, service_type=None):
      self.request = rate_xml.RateRequest()
      self.add_version('crs', 10, 0, 0)
      self.namespacedef = 'xmlns:ns="http://fedex.com/ws/rate/v10"'
      self.post_url_suffix = 'rate/'
      
      # Request Config
      self.request.ReturnTransitAndCommit = True
      
      # Transaction Detail
      self.request.TransactionDetail = rate_xml.TransactionDetail()
      self.request.TransactionDetail.CustomerTransactionId = datetime.datetime.now().strftime('rate.%Y%m%d.%H%M%S')
      
      # Shipment Details
      self.request.RequestedShipment = rate_xml.RequestedShipment()
      self.request.RequestedShipment.RateRequestTypes.append('ACCOUNT')
      self.request.RequestedShipment.ShipTimestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-00:00')
      # Get rid of the country warning if we are shipping the same country
      if to_address.country == from_address.country:
         # Domestic
         self.request.RequestedShipment.EdtRequestType = 'NONE'
      else:
         # International
         self.request.RequestedShipment.EdtRequestType = 'ALL'
      self.request.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
      
      self.request.RequestedShipment.PackagingType = packaging_type
      self.request.RequestedShipment.PackageDetail = 'INDIVIDUAL_PACKAGES'
      self.request.RequestedShipment.ReturnTransitAndCommit = True
      
      # Specify the service types if provided
      self.request.RequestedShipment.ServiceType = service_type
      
      # Add addresses
      self.request.RequestedShipment.Shipper = self.make_party(rate_xml, from_address, fedex_account)
      if fedex_account is None:
         self.request.RequestedShipment.Shipper.AccountNumber = self.account
      self.request.RequestedShipment.Recipient = self.make_party(rate_xml, to_address)
      
      # Add packages
      self.request.RequestedShipment.PackageCount = len(packages)
      self.request.RequestedShipment.RequestedPackageLineItems = []
      self.request.RequestedShipment.TotalWeight = rate_xml.Weight()
      self.request.RequestedShipment.TotalWeight.Value = 0
      self.request.RequestedShipment.TotalWeight.Units = 'LB'
      sequence = 1
      for p in packages:
         package = rate_xml.RequestedPackageLineItem()
         package.SequenceNumber = sequence
         package.GroupNumber = sequence
         package.GroupPackageCount = 1
         package.PhysicalPackaging = 'BOX'
         package.InsuredValue = rate_xml.Money()
         package.InsuredValue.Amount = p.value
         package.InsuredValue.Currency = 'USD'
         
         package.Weight = rate_xml.Weight()
         package.Weight.Units = 'LB'
         package.Weight.Value = p.weight
         
         package.Dimensions = rate_xml.Dimensions()
         package.Dimensions.Units = 'IN'
         package.Dimensions.Length = p.length
         package.Dimensions.Width = p.width
         package.Dimensions.Height = p.height
         
         package.SpecialServicesRequested = rate_xml.PackageSpecialServicesRequested()
         package.SpecialServicesRequested.SpecialServiceTypes = []
         if hasattr(p, 'require_signature'):
            package.SpecialServicesRequested.SpecialServiceTypes.append('SIGNATURE_OPTION')
            package.SpecialServicesRequested.SignatureOptionDetail = rate_xml.SignatureOptionDetail()
            if p.require_signature in ('ADULT', 'DIRECT', 'INDIRECT', 'NO_SIGNATURE_REQUIRED'):
               package.SpecialServicesRequested.SignatureOptionDetail.OptionType = p.require_signature.upper()
               # Indirect = $2.00, Direct = $3.25, Adult = $4.25
            elif p.require_signature:
               # Use indirect if not specified because it's the least expensive and should suffice for proof of delivery to address on CC or PayPal chargeback which is all that it should matter for
               package.SpecialServicesRequested.SignatureOptionDetail.OptionType = 'INDIRECT'
            else:
               package.SpecialServicesRequested.SignatureOptionDetail.OptionType = 'NO_SIGNATURE_REQUIRED'

         if hasattr(p, 'dry_ice_weight') and p.dry_ice_weight > 0:
             package.SpecialServicesRequested.SpecialServiceTypes.append('DRY_ICE')
             package.SpecialServicesRequested.DryIceWeight = rate_xml.Weight()
             package.SpecialServicesRequested.DryIceWeight.Units = 'KG'
             package.SpecialServicesRequested.DryIceWeight.Value = p.dry_ice_weight

         
         self.request.RequestedShipment.RequestedPackageLineItems.append(package)
         self.request.RequestedShipment.TotalWeight.Value = self.request.RequestedShipment.TotalWeight.Value + p.weight
         sequence = sequence + 1

      response = self.send()
      response_xml = rate_xml.parseString(response)
      
      notifications = []
      if response_xml.HighestSeverity in ('ERROR', 'FAILURE'):
         raise FedexShipError(response_xml)
      elif response_xml.HighestSeverity == 'WARNING':
         for notification in response_xml.Notifications:
            if notification.Code == '556':
               raise FedexError(notification.Message)
         notifications.append(notification.Message)
         logger.warning(notification.Message)
         
      parsed_response = {'status' : response_xml.HighestSeverity, 'info' : [], 'messages' : notifications}
      for details in response_xml.RateReplyDetails:
         delivery_day = 'Unknown'
         if details.DeliveryDayOfWeek:
            delivery_day = details.DeliveryDayOfWeek
         parsed_response['info'].append({
            'service' : details.ServiceType,
            'package' : details.PackagingType,
            'delivery_day' : delivery_day,
            'cost' : details.RatedShipmentDetails[0].ShipmentRateDetail.TotalNetCharge.Amount
         })
      return parsed_response

   def label(self, packages, packaging_type, service_type, from_address, to_address, email_alert=None, evening=False, payment=None, delivery_instructions=''):
      self.request = ship.ProcessShipmentRequest()
      self.add_version('ship', 10, 0, 0)
      self.namespacedef = 'xmlns:ns="http://fedex.com/ws/ship/v10"'
      self.post_url_suffix = 'ship/'
      
      self.send()
      
   def send(self):
      logger.setLevel(10)
      self.add_auth()
      
      data = StringIO.StringIO()
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
         
      if 'soapenv:Fault' in response_data:
         # FedEx returns a soap fault so parse the soap envelope and do something smart
         #soap_error = soap_xml.parseString(response_data)
         print response_data
      
      return response_data
      
Fedex = FedEx
