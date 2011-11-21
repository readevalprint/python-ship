import logging
logger = logging.getLogger(__name__)

import os
from datetime import datetime
import binascii
import suds
from suds.client import Client
from suds.sax.element import Element
import urllib
import urlparse

from shipping import Address

SERVICES = [
    'FEDEX_GROUND',
    'GROUND_HOME_DELIVERY',
    'FEDEX_EXPRESS_SAVER',
    'FEDEX_2_DAY',
    'STANDARD_OVERNIGHT',
    'PRIORITY_OVERNIGHT',
    'FIRST_OVERNIGHT',
    'FEDEX_1_DAY_FREIGHT',
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
        
        messages = [ 'FedEx error %s: %s' % (x.Code, x.LocalizedMessage if hasattr(x, 'LocalizedMessage') else x.Message) for x in reply.Notifications ]
        error_text = '\n'.join(messages)
        super(FedexError, self).__init__(error_text)
        
from shipping import Package

class Fedex(object):
    def __init__(self, credentials, debug = True):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.wsdl_dir = os.path.join(this_dir, 'wsdl', 'fedex')
        self.credentials = credentials
        self.debug = debug
    
    def create_client(self, wsdl_name):
        wsdl_file_path = os.path.join(self.wsdl_dir, wsdl_name)
        # Use os specific url to deal with windows drive letters "C://" makes 'C' look like a url type
        wsdl_file_url = urllib.pathname2url(wsdl_file_path)
        wsdl_url = urlparse.urljoin('file://', wsdl_file_url)
        client = Client(wsdl_url)
        if self.debug:
            client.set_options(location='https://wsbeta.fedex.com:443/web-services')
        else:
            client.set_options(location='https://gateway.fedex.com:443/web-services')
        
        return client
    
    def get_auth(self, client):
        auth = client.factory.create('WebAuthenticationDetail')
        auth.UserCredential.Key = self.credentials['key']
        auth.UserCredential.Password = self.credentials['password']
        print auth
        
        client_detail = client.factory.create('ClientDetail')
        client_detail.AccountNumber = self.credentials['account_number']
        client_detail.MeterNumber = self.credentials['meter_number']
        print client_detail
    
        return auth, client_detail
    
    def add_shipper(self, shipment, shipper):
        shipment.Shipper.Contact.PersonName = shipper.name
        shipment.Shipper.Contact.PhoneNumber = shipper.phone
        shipment.Shipper.Contact.EMailAddress = shipper.email
        shipment.Shipper.Address.StreetLines = [ shipper.address1, shipper.address2 ]
        shipment.Shipper.Address.City = shipper.city
        shipment.Shipper.Address.StateOrProvinceCode = shipper.state
        shipment.Shipper.Address.PostalCode = shipper.zip
        shipment.Shipper.Address.CountryCode = shipper.country
        shipment.Shipper.Address.Residential = shipper.is_residence
    
    def add_recipient(self, shipment, recipient):
        shipment.Recipient.Contact.PersonName = recipient.name
        shipment.Recipient.Contact.PhoneNumber = recipient.phone
        shipment.Recipient.Contact.EMailAddress = recipient.email
        shipment.Recipient.Address.StreetLines = [ recipient.address1, recipient.address2 ]
        shipment.Recipient.Address.City = recipient.city
        shipment.Recipient.Address.StateOrProvinceCode = recipient.state
        shipment.Recipient.Address.PostalCode = recipient.zip
        shipment.Recipient.Address.CountryCode = recipient.country
        shipment.Recipient.Address.Residential = recipient.is_residence
    
    def add_packages(self, client, shipment, service_type, packaging_type, packages):
        shipment.RateRequestTypes = 'ACCOUNT'
        shipment.ShipTimestamp = datetime.now()

        shipment.EdtRequestType = 'ALL'
        shipment.DropoffType = 'REGULAR_PICKUP'
        shipment.ServiceType = service_type
        
        shipment.PackagingType = packaging_type
        shipment.PackageDetail = 'INDIVIDUAL_PACKAGES'

        shipment.PackageCount = 0
        shipment.TotalWeight.Value = 0
        shipment.TotalWeight.Units = 'LB'
        for p in packages:
            package = client.factory.create('RequestedPackageLineItem')
            package.PhysicalPackaging = 'BOX'
            package.InsuredValue.Amount = p.value
            package.InsuredValue.Currency = 'USD'
            
            package.Weight.Units = 'LB'
            package.Weight.Value = p.weight
            
            package.Dimensions.Units = 'IN'
            package.Dimensions.Length = p.length
            package.Dimensions.Width = p.width
            package.Dimensions.Height = p.height
            
            if hasattr(p, 'require_signature') and p.require_signature != False:
               package.SpecialServicesRequested.SpecialServiceTypes.append('SIGNATURE_OPTION')
               if p.require_signature in ('ADULT', 'DIRECT', 'INDIRECT', 'NO_SIGNATURE_REQUIRED'):
                  package.SpecialServicesRequested.SignatureOptionDetail.OptionType = p.require_signature.upper()
                  # Indirect = $2.00, Direct = $3.25, Adult = $4.25
               else:
                  # Use indirect if not specified because it's the least expensive and should suffice for proof of delivery to address on CC or PayPal chargeback which is all that it should matter for
                  package.SpecialServicesRequested.SignatureOptionDetail.OptionType = 'INDIRECT'

            if hasattr(p, 'dry_ice_weight') and p.dry_ice_weight > 0:
                package.SpecialServicesRequested.SpecialServiceTypes.append('DRY_ICE')
                package.SpecialServicesRequested.DryIceWeight.Units = 'KG'
                package.SpecialServicesRequested.DryIceWeight.Value = p.dry_ice_weight

            shipment.RequestedPackageLineItems.append(package)
            shipment.PackageCount += 1
            shipment.TotalWeight.Value += p.weight
    
    def rate(self, packages, packaging_type, shipper, recipient):
        client = self.create_client('RateService_v9.wsdl')
        
        auth, client_detail = self.get_auth(client)
        client_detail.Region = 'US'
        
        trans = client.factory.create('TransactionDetail')
        
        version = client.factory.create('VersionId')
        version.ServiceId = 'crs'
        version.Major = '9'
        version.Intermediate = '0'
        version.Minor = '0'
        
        shipment = client.factory.create('RequestedShipment')
        
        self.add_shipper(shipment, shipper)
        self.add_recipient(shipment, recipient)
        service_type = None
        self.add_packages(client, shipment, service_type, packaging_type, packages)
        
        try:
            reply = client.service.getRates(auth, client_detail, trans, version, ReturnTransitAndCommit=True, RequestedShipment=shipment)

            logger.info(reply)

            if reply.HighestSeverity in [ 'ERROR', 'FAILURE' ]:
                raise FedexShipError(reply)
            elif reply.HighestSeverity == 'WARNING':
                # Check to see if this is a 'Service not available error'
                for notification in reply.Notifications:
                    if notification.Code == '556':
                        raise FedexError(notification.Message)
                logger.info(reply)
                
            response = { 'status': reply.HighestSeverity, 'info': list() }
            
            for details in reply.RateReplyDetails:
                delivery_day = 'Unknown'
                try:
                    delivery_day = details.DeliveryDayOfWeek
                except AttributeError as e:
                    pass
                response['info'].append({
                    'service': details.ServiceType,
                    'package': details.PackagingType,
                    'delivery_day': delivery_day,
                    'cost': details.RatedShipmentDetails[0].ShipmentRateDetail.TotalNetCharge.Amount,
                })
            
            return response
        except suds.WebFault as e:
            raise FedexWebError(e.fault, e.document)

    def label(self, packages, packaging_type, service_type, shipper, recipient, email_alert=None, evening=False, payment=None, delivery_instructions=''):
        client = self.create_client('ShipService_v9.wsdl')
        
        auth, client_detail = self.get_auth(client)
        
        trans = client.factory.create('TransactionDetail')
        
        version = client.factory.create('VersionId')
        version.ServiceId = 'ship'
        version.Major = '9'
        version.Intermediate = '0'
        version.Minor = '0'
        
        shipment = client.factory.create('RequestedShipment')

        shipment.CustomerSelectedActualRateType = 'PAYOR_ACCOUNT_SHIPMENT'
        
        if not payment:
            payment = { 'type': 'SENDER', 'account': self.credentials['account_number'] }
        shipment.ShippingChargesPayment.PaymentType = payment['type']
        shipment.ShippingChargesPayment.Payor.AccountNumber = payment['account']
        
        self.add_shipper(shipment, shipper)
        self.add_recipient(shipment, recipient)
        
        if email_alert:
            shipment.SpecialServicesRequested.SpecialServiceTypes.append('EMAIL_NOTIFICATION')
            shipment.SpecialServicesRequested.EMailNotificationDetail.AggregationType = 'PER_PACKAGE'
            for type, email in [ ('SHIPPER', shipper.email), ('RECIPIENT', recipient.email) ]:
                info = client.factory.create('EMailNotificationRecipient')
                info.EMailNotificationRecipientType = type
                info.EMailAddress = email
                info.Format = 'HTML'
                info.NotifyOnShipment = True
                info.Localization.LanguageCode = 'EN'
            
                shipment.SpecialServicesRequested.EMailNotificationDetail.Recipients.append(info)
        
        if evening:
            shipment.SpecialServicesRequested.SpecialServiceTypes.append('HOME_DELIVERY_PREMIUM')
            shipment.SpecialServicesRequested.HomeDeliveryPremiumDetail.HomeDeliveryPremiumType = 'EVENING'
        
        shipment.DeliveryInstructions = delivery_instructions
        
        shipment.LabelSpecification.LabelFormatType = 'COMMON2D'
        shipment.LabelSpecification.ImageType = 'PNG'
        shipment.LabelSpecification.LabelStockType = 'PAPER_4X6'
        shipment.LabelSpecification.LabelPrintingOrientation = 'BOTTOM_EDGE_OF_TEXT_FIRST'
        shipment.ErrorLabelBehavior = 'STANDARD'
        
        self.add_packages(client, shipment, service_type, packaging_type, packages)
        
        try:
            self.reply = client.service.processShipment(auth, client_detail, trans, version, shipment)
            logger.info(self.reply)

            if self.reply.HighestSeverity in [ 'ERROR', 'FAILURE' ]:
                raise FedexShipError(self.reply)
            elif self.reply.HighestSeverity == 'WARNING':
                logger.info(self.reply)
                
            response = {
                'status': self.reply.HighestSeverity,
                'shipments': list(),
                'international_document': {
                    'description': None,
                    'pdf': None
                }
            }

            for i in range(len(packages)):
                details = self.reply.CompletedShipmentDetail.CompletedPackageDetails[i]
                cost = 0
                try:
                    cost = details.PackageRating.PackageRateDetails[0].NetCharge.Amount
                except AttributeError as e:
                    pass
                info = {
                    'tracking_number': details.TrackingIds[0].TrackingNumber,
                    'cost': cost,
                    'label': binascii.a2b_base64(details.Label.Parts[0].Image),
                }
                response['shipments'].append(info)
            return response
            
        except suds.WebFault as e:
            raise FedexWebError(e.fault, e.document)