#
# Python script to check if Google's Nexus 4 is in stock.
#
# Copyright (C) 2012 Bilal Akhtar <me@itsbilal.com>
# Licensed under the MIT License, see COPYING
#

from datetime import datetime
import urllib2

NEXUS_TYPE=4               # Change this to 7 for Nexus 7, or 10 for Nexus 10
NEXUS_STORAGE_SIZE="8gb"   # Set storage size for desired Nexus here
LOGFILENAME="nexus.log"

response = urllib2.urlopen("https://play.google.com/store/devices/details?id=nexus_%d_%s" % (NEXUS_TYPE, NEXUS_STORAGE_SIZE))
http = response.read()

if http.find("Add to Cart") >= 0:
    logstring = "%s: FOUND: Add to Cart button detected on Google Play. Nexus %d %s is in stock." % (datetime.now(), NEXUS_TYPE, NEXUS_STORAGE_SIZE)
elif http.find("Sold out") >= 0:
    logstring = "%s: Nexus %d %s is out of stock and sold out" % (datetime.now(), NEXUS_TYPE, NEXUS_STORAGE_SIZE)
elif http.find("requested URL was not found") >= 0:
    logstring = "%s: Google Play returned HTTP 404. Are you searching for a valid Nexus device?" % datetime.now()
else:
    logstring = "%s: Not sure about stock status, Nexus %d %s is most probably out of stock" % (datetime.now(), NEXUS_TYPE, NEXUS_STORAGE_SIZE)

print logstring

logfile = open(LOGFILENAME, "a")
logfile.write(logstring+"\n")
logfile.close()

