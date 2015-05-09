#!/usr/bin/python
# get_ipints.py

__author__ = 'Claudia'

import sys

#raw_input("Press Return to continue...")

from ciscoconfparse import CiscoConfParse

config = CiscoConfParse(str(sys.argv[1]),factory=True)
vl = config.find_all_children("^vlan")
lvl=len(vl)
for v in vl:
    print v
print ("Number of items in list: %s" % lvl)
print ("Vlans from config file: %s" % str(sys.argv[1]))

raw_input("Press Return to continue to Router/SVI Section...")

int = config.find_objects_w_child(parentspec=r"^interface",childspec=r"ip address")
lint = len(int)
for i in int:
    print i

print ("Number of items in list: %s" % lint)
print ("Routed Interfaces from config file: %s" % str(sys.argv[1]))


raw_input("Press Return to continue to IP Section...")

ipint = config.find_interface_objects("^interface")
lipint = len(ipint)
for i in ipint:
    print i

print ("Number of items in list: %s" % lipint)
print ("IPs from config file: %s" % str(sys.argv[1]))

raw_input("Press Return to continue to Other IP Section...")

ipint2 = config.find_children_w_parents("^interface\s","ip address")
lipint2 = len(ipint2)
print ipint2
for i in ipint2:
    print i

print ("Number of items in list: %s" % lipint2)
print ("IPs from config file: %s" % str(sys.argv[1]))