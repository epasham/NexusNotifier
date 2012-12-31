#
# Python script to check if Google's Nexus 4 is in stock.
#
# Copyright (C) 2012 Bilal Akhtar <me@itsbilal.com>
# Licensed under the MIT License, see COPYING
#

import argparse
from datetime import datetime
import urllib2

LOGFILENAME="nexus.log"

# ArgParse part
parser = argparse.ArgumentParser(description="Check stock of a Nexus device on Google Play")

parser.add_argument("--model", type=int, nargs="?", default=4, help="The type of Nexus to search for (Enter 4 for Nexus 4, 7 for Nexus 7, etc)")
parser.add_argument("--storage", type=int, nargs="?", default=8, help="The storage size of the Nexus device you're searching for (enter 8 for 8GB, 16 for 16GB and so on)")

cmdargs = parser.parse_args()
NEXUS_TYPE          = cmdargs.model
NEXUS_STORAGE_SIZE  = "%dgb" % cmdargs.storage

try:
    response = urllib2.urlopen("https://play.google.com/store/devices/details?id=nexus_%d_%s" % (NEXUS_TYPE, NEXUS_STORAGE_SIZE))
    http = response.read()

    if http.find("Add to Cart") >= 0:
        logstring = "%s: FOUND: Add to Cart button detected on Google Play. Nexus %d %s is in stock." % (datetime.now(), NEXUS_TYPE, NEXUS_STORAGE_SIZE)
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

