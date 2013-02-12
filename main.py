#
# Python script to check if Google's Nexus 4 is in stock.
#
# Copyright (C) 2012 Bilal Akhtar <me@itsbilal.com>
# Licensed under the MIT License, see COPYING
#

import argparse
from datetime import datetime
from email.mime.text import MIMEText
import smtplib
import urllib2

LOGFILENAME="nexus.log"

# ArgParse part
parser = argparse.ArgumentParser(description="Check stock of a Nexus device on Google Play")

parser.add_argument("--model", type=int, nargs="?", default=4, help="The type of Nexus to search for (Enter 4 for Nexus 4, 7 for Nexus 7, etc)")
parser.add_argument("--storage", type=int, nargs="?", default=8, help="The storage size of the nexus device you're searching for (enter 8 for 8gb, 16 for 16gb and so on)")
parser.add_argument("--email", type=str, nargs="?", default="", help="The e-mail address to which an e-mail should be sent if the Nexus is in stock")
parser.add_argument("--wireless-dock", action="store_true", help="Search for stock of the Nexus 4 Wireless charging dock")

cmdargs = parser.parse_args()
NEXUS_TYPE          = cmdargs.model
NEXUS_STORAGE_SIZE  = "%dgb" % cmdargs.storage
email_address       = cmdargs.email
wireless_dock       = cmdargs.wireless_dock

try:
    gplay_url = "https://play.google.com/store/devices/details?id=nexus_%d_%s" % (NEXUS_TYPE, NEXUS_STORAGE_SIZE)

    if wireless_dock:
        gplay_url = "https://play.google.com/store/devices/details?id=nexus_4_wireless_charger"
        NEXUS_TYPE = 4
        NEXUS_STORAGE_SIZE = "Wireless Charger"

    response = urllib2.urlopen(gplay_url)
    http = response.read()

    if http.find("Add to Cart") >= 0:
        logstring = "%s: FOUND: Add to Cart button detected on Google Play. Nexus %d %s is in stock." % (datetime.now(), NEXUS_TYPE, NEXUS_STORAGE_SIZE)

        if len(email_address) > 0:
            # Send mail
            msg = MIMEText("Nexus %d %s IS IN STOCK! \n\n Get it now! %s" % (NEXUS_TYPE, NEXUS_STORAGE_SIZE, gplay_url))
            msg['Subject'] = "Nexus %d in stock" % NEXUS_TYPE
            msg['From'] = email_address
            msg['To'] = email_address
            smtp = smtplib.SMTP("localhost")
            smtp.sendmail(email_address, email_address, msg.as_string())
            smtp.quit()
        
    elif http.find("Sold out") >= 0:
        logstring = "%s: Nexus %d %s is out of stock and sold out" % (datetime.now(), NEXUS_TYPE, NEXUS_STORAGE_SIZE)
    else:
        logstring = "%s: Not sure about stock status, Nexus %d %s is most probably out of stock" % (datetime.now(), NEXUS_TYPE, NEXUS_STORAGE_SIZE)

except (urllib2.HTTPError):
    logstring = "%s: Google Play returned HTTP 404. Are you searching for a valid Nexus device?" % datetime.now()

print logstring

logfile = open(LOGFILENAME, "a")
logfile.write(logstring+"\n")
logfile.close()

