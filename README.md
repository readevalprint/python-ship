Currently requires suds and suds must be patched to work with UPS.

Index: /suds/client.py
===================================================================
--- client.py	(revision 1741)
+++ client.py	(revision 1714)
@@ -631,8 +631,7 @@
             else:
                 soapenv = soapenv.plain()
             soapenv = soapenv.encode('utf-8')
-            context = plugins.message.sending(envelope=soapenv)
-            soapenv = context.envelope
+            plugins.message.sending(envelope=soapenv)
             request = Request(location, soapenv)
             request.headers = self.headers()
             reply = transport.send(request)
             
Working toward using non-SOAP interfaces for UPS and FedEx which should make it easier to setup.  XML interface generated with generateDS.py.

ups_config and fedex_config need to be a dictionaries

fedex_config = {
   'meter_number': 'FedEx Meter Number', 
   'password': 'FedEx API password', 
   'account_number': 'FedEx Account Number', 
   'key': 'FedEx API Key'
}
   
ups_config = {
   'username': 'UPS Online Username',
   'password': 'UPS Online Password', 
   'shipper_number': 'UPS Shipper Number',
   'access_license': 'UPS API License'
}

Test and Production Key information available at
FedEx : http://www.fedex.com/us/developer/index.html
UPS : http://www.ups.com/content/us/en/resources/techsupport/developercenter.html

* You need a UPS and FedEx account to get the keys
* I don't use endicia for postage so haven't looked into the setup for it