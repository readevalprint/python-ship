import re

def debug_print_tree(elem):   
   import xml.etree.ElementTree as etree
   from xml.dom.minidom import parseString
   node = parseString(etree.tostring(elem).replace('\n', ''))
   print(node.toprettyxml(indent="   "))
   
import logging
def setLoggingLevel(level = logging.ERROR):
   """ Convenience function to set all the logging in one place """
   logging.getLogger('%s.ups' % __name__.split('.')[0]).setLevel(level)
   logging.getLogger('%s.fedex' % __name__.split('.')[0]).setLevel(level)
   logging.getLogger('%s.endicia' % __name__.split('.')[0]).setLevel(level)
   logging.getLogger('suds.client').setLevel(level)
   logging.getLogger('suds.transport').setLevel(level)
   logging.getLogger('suds.xsd.schema').setLevel(level)
   logging.getLogger('suds.wsdl').setLevel(level)

class Package(object):
    def __init__(self, weight_in_ozs, length, width, height, value=0, require_signature=False, reference=u'', dry_ice_weight_in_ozs=0.0):
        self.weight = weight_in_ozs / 16.0
        self.length = length
        self.width = width
        self.height = height
        self.value = value
        self.require_signature = require_signature
        self.reference = reference
        self.dry_ice_weight = dry_ice_weight_in_ozs / 35.27397
    
    @property
    def weight_in_ozs(self):
        return self.weight * 16

    @property
    def weight_in_lbs(self):
        return self.weight

class Address(object):
    def __init__(self, name, address, city, state, zip, country, address2='', phone='', email='', is_residence=True, company_name='', use_domestic_corrections = True):
        self.company_name = company_name or ''
        self.name = name or ''
        self.address1 = address or ''
        self.address2 = address2 or ''
        self.city = city or ''
        self.state = state or ''
        self.zip = re.sub('[^\w]', '', unicode(zip).split('-')[0]) if zip else ''
        self.country = get_country_code(country, use_domestic_corrections)
        self.phone = re.sub('[^0-9]*', '', unicode(phone)) if phone else ''
        self.email = email or ''
        self.is_residence = is_residence or False
        
    def getCompany(self):
        return self.company_name
    def setCompany(self, value):
        self.company_name = value
    company = property(getCompany, setCompany)
        
    def getStreet1(self):
        return self.address1
    def setStreet1(self, value):
        self.address1 = value
    street1 = property(getStreet1, setStreet1)
      
    def getStreet2(self):
        return self.address2
    def setStreet2(self, value):
        self.address2 = value
    street2 = property(getStreet2, setStreet2)
    
    
    def __eq__(self, other):
        return vars(self) == vars(other)
    
    def __repr__(self):
        street = self.address1
        if self.address2:
            street += '\n' + self.address2
        return '%s\n%s\n%s, %s %s %s' % (self.name, street, self.city, self.state, self.zip, self.country)

import iso
def get_country_code(country, use_domestic_corrections = False):
   country = country.upper()
   if len(country) == 2:
      # If it's a 2 digit code, generate an exception if it's not valid
      name = iso.CODE_TO_COUNTRY[country]
      code = country
   elif country in iso.COUNTRY_TO_CODE:
      # If spelling is exactly like the ISO 3166, slim odds here
      code = iso.COUNTRY_TO_CODE[country]
   else:   
      # Otherwise use name guesses, or just return whatever was passed in so we can UPS, FedEx or Endicia can send us a confusing error message
      code = iso.GUESS_TO_CODE.get(country, country)
   if use_domestic_corrections:
      # Fix the country to US if it's places like Guam or US Virigin Islands
      code  = iso.ISO_US_MAIL_CORRECTIONS.get(code, code)
   return code