import logging
logger = logging.getLogger(__name__)

import datetime
import StringIO
import binascii
import urllib2
import avs
import rate
import ship

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
         self.post_url = 'https://wsbeta.fedex.com:443/xml'
      else:
         self.post_url = 'https://ws.fedex.com:443/xml'
      
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
      
   def add_shipper(self, address):
      pass
      
   def add_recipient(self, address):
      pass
      
   def add_package(self, package):
      pass
      
   def verify(self, address):
      self.request = avs.AddressValidationRequest()
      self.add_version('aval', 2, 0, 0)
      self.namespacedef = 'xmlns:ns="http://fedex.com/ws/addressvalidation/v2"'
      # Timestamp format =  YYYY-MM-DDTHH:MM:SS-xx:xx utc
      self.request.RequestTimestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-00:00')
      
      # Validation Address
      self.request.AddressesToValidate = [avs.AddressToValidate()]
      if len(address.company) > 0:
         self.request.AddressesToValidate[0].CompanyName = address.company
      self.request.AddressesToValidate[0].Address = avs.Address()
      self.request.AddressesToValidate[0].Address.StreetLines = [address.street1, address.street2]
      self.request.AddressesToValidate[0].Address.City = address.city
      self.request.AddressesToValidate[0].Address.StateOrProvinceCode = address.state
      self.request.AddressesToValidate[0].Address.PostalCode = address.zip
      #self.request.AddressesToValidate[0].Address.UrbanizationCode = address. # For Puerto Rico... not sure what to do about it right now
      if address.country == 'PR':
         logger.warning('Urbanization Code should be used for Puerto Rico.')
      self.request.AddressesToValidate[0].Address.CountryCode = address.country
      
      # Validation Options
      self.request.Options = avs.AddressValidationOptions()
      self.request.Options.VerifyAddresses = True
      self.request.Options.CheckResidentialStatus = True
      self.request.Options.MaximumNumberOfMatches = 3
      self.request.Options.StreetAccuracy = 'MEDIUM'
      self.request.Options.DirectionalAccuracy = 'MEDIUM'
      self.request.Options.CompanyNameAccuracy = 'LOOSE'
      self.request.Options.ConvertToUpperCase = True
      self.request.Options.RecognizeAlternateCityNames = True
      
      response = self.send()
      return response
      
   def rate(self, package, packaging_type, from_address, to_address):
      self.request = rate.RateRequest()
      self.add_version('crs', 10, 0, 0)
      self.namespacedef = 'xmlns:ns="http://fedex.com/ws/rate/v10"'
      
      self.send()

   def label(self, packages, packaging_type, service_type, from_address, to_address, email_alert=None, evening=False, payment=None, delivery_instructions=''):
      self.request = ship.ProcessShipmentRequest()
      self.add_version('ship', 10, 0, 0)
      self.namespacedef = 'xmlns:ns="http://fedex.com/ws/ship/v10"'
      
      self.send()
      
   def send(self):
      self.add_auth()
      
      data = StringIO.StringIO()
      self.request.export(data, 0, namespacedef_=self.namespacedef)
      data = data.getvalue()
      
      # Add xml header
      data = '<?xml version="1.0" encoding="UTF-8"?>\n' + data
      data = data.encode('utf-8')
      
      logger.debug('XML Request:\n%s' % data)
      print data
      
      # Get the response
      response = urllib2.urlopen(self.post_url, data)
      if response.code != 200:
         logger.error('HTTP Error %s' % str(response.code))
         raise Exception('HTTP Error %s' % str(response.code))
      
      response_data = response.read()
      logger.debug('XML Response:\n%s' % response_data)
      
      return response_data
      
Fedex = FedEx 