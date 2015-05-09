#!/usr/bin/python
# get_vlans.py

__author__ = 'Claudia'

import sys

#raw_input("Press Return to continue...")

from ciscoconfparse import CiscoConfParse

config = CiscoConfParse(str(sys.argv[1]))
vl = config.find_all_children("^vlan")
lvl=len(vl)
for v in vl:
    print v
print ("Number of items in list: %s" % lvl)
print ("Vlans from config file: %s" % str(sys.argv[1]))
