#!/usr/bin/python
# get_vlans.py

__author__ = 'Claudia'

import sys
total = len(sys.argv)
cmdargs = str(sys.argv)
print ("The total numbers of args passed to the script: %d " % total)
print ("Args list: %s " % cmdargs)
# Pharsing args one by one
print ("Script name: %s" % str(sys.argv[0]))
print ("First argument: %s" % str(sys.argv[1]))
#print ("Second argument: %s" % str(sys.argv[2]))
#print ("Third argument: %s" % str(sys.argv[3]))

raw_input("Press Return to continue...")

from ciscoconfparse import CiscoConfParse

config = CiscoConfParse(str(sys.argv[1]))
vl = config.find_all_children("^vlan")
lvl=len(vl)
for v in vl:
    print v
print ("Number of items in list: %s" % lvl)
print ("Vlans from config file: %s" % str(sys.argv[1]))
