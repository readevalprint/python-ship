# Fork of benweatherman / python-ship 
 * This fork aims at using non-SOAP xml interface to FedEx and UPS

#### Things that are working as of December 15, 2011
 * UPS address validation
 * UPS Rate Request
 * FedEx Rate Request
 * Handle FedEx soap:Fault error messages
 
#### Up next (in no particular order)
 * FedEx Pickup Request
 * UPS Label
 * FedEx Label
 * Test FedEx address validation and parse response 
 
#### Other notes
 * Should not require suds unless I made a mistake.
 * Might just work as is in Python 2.7
 * Request and Response times seem faster.  Probably tear down and creation of suds client. More likely my imagination.
 * XML interface generated with generateDS.py. (http://www.rexx.com/~dkuhlman/generateDS.html)

**ups_config and fedex_config need to be a dictionaries**

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

#### Test and Production Key information available at
* FedEx : http://www.fedex.com/us/developer/index.html
* UPS : http://www.ups.com/content/us/en/resources/techsupport/developercenter.html

You need a UPS and FedEx account to get the keys  
I don't use endicia for postage so haven't looked into the setup for it  