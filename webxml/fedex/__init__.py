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
         self.post_url = 'https://gatewaybeta.fedex.com:443/xml/'
      else:
         self.post_url = 'https://gateway.fedex.com:443/xml/'
      
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
      self.namespacedef = ''
      # Timestamp format =  YYYY-MM-DDTHH:MM:SS-xx:xx utc
      self.request.RequestTimestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-00:00')
      
      # Transaction Detail
      self.request.TransactionDetail = avs.TransactionDetail()
      self.request.TransactionDetail.CustomerTransactionId = datetime.datetime.now().strftime('avs.%Y%m%d.%H%M%S')
      
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
      self.request.export(data, 0, namespace_='', namespacedef_=self.namespacedef)
      data = data.getvalue()

      data = data.encode('ascii')
      data = test_avs
      logger.debug('XML Request:\n%s' % data)
      
      request = urllib2.Request(self.post_url)
      request.add_data(data)
      request.add_header('Referer', 'www.wholesaleimport.com')
      request.add_header('Host', request.get_host().split(':')[0])
      request.add_header('Port', request.get_host().split(':')[1])
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
      
Fedex = FedEx 

test_avs = '''<AddressValidationRequest>
<WebAuthenticationDetail>
<UserCredential>
<Key>cqDgZ1X4Og4hJ6Mi</Key>
<Password>5SkxQ0WtOzXeDZDi63xaj1nGz</Password>
</UserCredential>
</WebAuthenticationDetail>
<ClientDetail>
<AccountNumber>510087860</AccountNumber>
<MeterNumber>100076071</MeterNumber>
</ClientDetail>
<TransactionDetail>
<CustomerTransactionId>WSVC_addressvalidation</CustomerTransactionId>
</TransactionDetail>
<Version>
<ServiceId>aval</ServiceId>
<Major>2</Major>
<Intermediate>0</Intermediate>
<Minor>0</Minor>
</Version>
<RequestTimestamp>2011-12-02T23:15:49-00:00</RequestTimestamp>
<Options>
<VerifyAddresses>1</VerifyAddresses>
<CheckResidentialStatus>1</CheckResidentialStatus>
<MaximumNumberOfMatches>10</MaximumNumberOfMatches>
<StreetAccuracy>EXACT</StreetAccuracy>
<DirectionalAccuracy>EXACT</DirectionalAccuracy>
<CompanyNameAccuracy>EXACT</CompanyNameAccuracy>
<ConvertToUpperCase>1</ConvertToUpperCase>
<RecognizeAlternateCityNames>1</RecognizeAlternateCityNames>
<ReturnParsedElements>1</ReturnParsedElements>
</Options>
<AddressesToValidate>
<AddressId>String</AddressId>
<CompanyName>String</CompanyName>
<Address>
<StreetLines>475 PARK AVE S FL 11</StreetLines>
<City>NEWYORK</City>
<StateOrProvinceCode>NY</StateOrProvinceCode>
<PostalCode>10016</PostalCode>
<UrbanizationCode>String</UrbanizationCode>
<CountryCode>US</CountryCode>
<Residential>1</Residential>
</Address>
</AddressesToValidate>
</AddressValidationRequest>'''
