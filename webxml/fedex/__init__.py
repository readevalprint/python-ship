import logging
logger = logging.getLogger(__name__)

import avs
import rate
import ship

class FedEx(object):
   def __init__(self, credentials_dictionary={}, debug=True, key='', password='', account='', meter=''):
      self.key = credentials_dictionary.get('key', key)
      self.password = credentials_dictionary('password', password)
      self.account = credentials_dictionary('account_number', account)
      self.meter = credentials_dictionary('meter_number', meter)
      self.debug = debug
      self.request = None
      
   def add_auth(self):
      self.request.WebAuthenticationDetail = ship.WebAuthenticationDetail()
      self.request.WebAuthenticationDetail.UserCredential = ship.WebAuthenticationCredential()
      self.request.WebAuthenticationDetail.UserCredential.Key = self.key      
      self.request.WebAuthenticationDetail.UserCredential.Password = self.password
      self.request.ClientDetail = ship.ClientDetail()
      self.request.ClientDetail.AccountNumber = self.account
      self.request.ClientDetail.MeterNumber = self.meter
      
   def add_version(self, service, major, intermediate = 0, minor = 0)
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
      # Timestamp format =  YYYY-MM-DDTHH:MM:SS-xx:xx utc
      self.request.RequestTimestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-00:00')
      
      # Validation Address
      self.request.AddressToValidate
      
      # Validation Options
      self.request.Options = AddressValidationOptions()
      self.request.Options.
      self.request.Options.MaximumNumberOfMatches = 3
      self.request.Options.StreetAccuracy = 'MEDIUM'
      self.request.Options.DirectionalAccuracy = 'MEDIUM'
      self.request.Options.CompanyNameAccuracy = 'LOOSE'
      self.request.Options.ConvertToUpperCase = True
      self.request.Options.RecognizeAlternateCityNames = True
      
      self.send()
      
   def rate(self, package, packaging_type, from_address, to_address):
      self.request = rate.RateRequest()
      self.add_version('crs', 10, 0, 0)
      
      self.send()

   def label(self, packages, packaging_type, service_type, from_address, to_address, email_alert=None, evening=False, payment=None, delivery_instructions=''):
      self.request = ship.ProcessShipmentRequest()
      self.add_version('ship', 10, 0, 0)
  
      
      self.send()
      
   def send():
      self.add_auth()
      
      