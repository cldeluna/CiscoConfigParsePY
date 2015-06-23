#!/usr/bin/python -tt
# inv_diff.py
# Claudia
# PyCharm
__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "6/21/15  6:20 PM"
__copyright__ = "Copyright (c) 2015 Claudia de Luna"
__license__ = "Python"

import sys
import re
import os
import xlrd


# http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary
class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect
    def removed(self):
        return self.set_past - self.intersect
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


# Provided main() calls the above functions
def main():
    # Take path argument and list all text files
    """
    Description
    :return:
    """

    siteid=sys.argv[1]
    #siteid=1389

    invnew=sys.argv[2]
    #inv="/Users/Claudia/Box Sync/Network Transformation/Inventory/DiData-inventory-2015-06-15.xlsx"

    invsh="Chassis & Module"

    invold=sys.argv[3]
    #nbdir="/Users/Claudia/Box Sync/Network Transformation/Sites/North America - Year One/1389-Ontario-CA-Solar/show_commands_detail_06.15.15"

    siterows=0
    maxoldrows=0
    maxnewrows=0
    dnold=""
    dnnew=""
    dnmore=""
    dnless=""
    wsoldlist=[]
    wsolddict={}
    wsnewlist=[]
    wsnewdict={}



    wbnew = xlrd.open_workbook(invnew)
    wsnew = wbnew.sheet_by_name(invsh)

    wbold = xlrd.open_workbook(invold)
    wsold = wbold.sheet_by_name(invsh)

    print "New DiData Inventory Workbook in use:, %s"%(invnew)
    print "DiData Inventory Worksheet in use:, %s"%(wsnew.name)

    print "Old DiData Inventory Workbook in use:, %s"%(invold)
    print "DiData Inventory Worksheet in use:, %s"%(wsold.name)

    print "Total number of rows in the New Inventory Worksheet:, %d"%(wsnew.nrows)
    print "Total number of columns in the New Inventory Worksheet:, %d"%(wsnew.ncols)

    print "Total number of rows in the Old Inventory Worksheet:, %d"%(wsold.nrows)
    print "Total number of columns in the Old Inventory Worksheet:, %d"%(wsold.ncols)

    print "Site ID to search:, %s"%(siteid)
    print ("-")*80
    print "Name:,Notes, IP Address, Slot, Model, (muliple sets for a stack)"

    if wsold.nrows >= wsnew.nrows:
        maxrows=wsold.nrows
        wsmore=wsold
        wsless=wsnew
    else:
        maxrows=wsnew.nrows
        wsmore=wsnew
        wsless=wsold

    for row_index in range(wsold.nrows):
        if wsold.cell_value(row_index,6) == int(siteid):
            maxoldrows=maxoldrows+1
    for row_index in range(wsnew.nrows):
        if wsnew.cell_value(row_index,6) == int(siteid):
            maxnewrows=maxnewrows+1

    #print maxoldrows
    #print maxnewrows

    #Populate the Old Dictionary from the older file
    for oldrowi in range(wsold.nrows):
        if wsold.cell_value(oldrowi,6) == int(siteid):
            if wsold.cell_value(oldrowi,1) == wsold.cell_value(oldrowi-1,1):
                for i in range(2,5):
                    wsoldlist.append(wsold.cell_value(oldrowi, i))
                wsolddict[wsold.cell_value(oldrowi,1)]=wsoldlist
            else:
                wsoldlist=[]
                for i in range(2,5):
                    wsoldlist.append(wsold.cell_value(oldrowi, i))
                wsolddict[wsold.cell_value(oldrowi,1)]=wsoldlist

    #print wsolddict

    #for key,val in wsolddict.items():
        #print key, "==>",val
        #print "\n"
    #print str(len(wsolddict))



    #Populate the New Dictionary from the newer file
    for newrowi in range(wsnew.nrows):
        if wsnew.cell_value(newrowi,6) == int(siteid):
            if wsnew.cell_value(newrowi,1) == wsnew.cell_value(newrowi-1,1):
                for i in range(2,5):
                    wsnewlist.append(wsnew.cell_value(newrowi, i))
                wsnewdict[wsnew.cell_value(newrowi,1)]=wsnewlist
            else:
                wsnewlist=[]
                for i in range(2,5):
                    wsnewlist.append(wsnew.cell_value(newrowi, i))
                wsnewdict[wsnew.cell_value(newrowi,1)]=wsnewlist
    #print wsolddict

    #for key,val in wsnewdict.items():
        #print key, "==>",val
        #print "\n"
    #print str(len(wsnewdict))
    #print str(len(wsolddict))
    #print len(wsnewdict.keys())
    #print len(wsolddict.keys())
    #print wsnewdict.keys() == wsolddict.keys()

    #for oldkey in sorted(wsolddict):
        #print "%s: %s" %(oldkey, wsolddict[oldkey])

    #for newkey in sorted(wsnewdict):
        #print "%s: %s" %(newkey, wsnewdict[newkey])

    #mismatch_keys = [key for key in wsolddict if not key in wsnewdict or wsolddict[key] != wsnewdict[key]]
    #print "Mistmatched Keys"
    #print mismatch_keys
    #print "&&&&"
    #match = not bool(mismatch_keys)
    #for key in mismatch_keys:
        #print key
        #print "%s ==> %s" % (wsolddict[key],wsnewdict[key])

    diff=DictDiffer(wsolddict,wsnewdict)

    diff_added=diff.added()
    diff_removed=diff.removed()
    diff_changed=diff.changed()
    diff_unchanged=diff.unchanged()

    print "+"*80
    print "Added: %s, %d"%(diff_added,len(diff_added))
    if len(diff_added) > 0:
        for i in range(len(diff_added)):
            elem = diff_added.pop()
            if elem in wsolddict.keys():
                print "Old Data for %s:, %s"%(elem,wsolddict[elem])
            else:
                print "Old Data for %s:, does not exist!"%(elem)
            if elem in wsnewdict.keys():
                print "New Data for %s:, %s"%(elem,wsnewdict[elem])
            else:
                print "New Data for %s:, does not exist!"%(elem)
            #print "\n"
    print "+"*80
    print "-"*80
    print "Removed: %s, %d"%(diff_removed,len(diff_removed))
    if len(diff_removed) > 0:
        for i in range(len(diff_removed)):
            elem = diff_removed.pop()
            if elem in wsolddict.keys():
                print "Old Data for %s:, %s"%(elem,wsolddict[elem])
            else:
                print "Old Data for %s:, does not exist!"%(elem)
            if elem in wsnewdict.keys():
                print "New Data for %s:, %s"%(elem,wsnewdict[elem])
            else:
                print "New Data for %s:, does not exist!"%(elem)
            #print "\n"
    print "-"*80
    print "~"*80
    print "Changed: %s, %d"%(diff_changed, len(diff_changed))
    if len(diff_changed) > 0:
        for i in range(len(diff_changed)):
            elem = diff_changed.pop()
            lenold=len(wsolddict[elem])
            lennew=len(wsnewdict[elem])
            note="Old inventory record and new inventory record have same number of devices:," + str(lenold/3)
            if lenold > lennew:
                note="Old inventory record has " + str((lenold-lennew)/3) + " more devices than the new inventory record!"
            else:
                note="Old inventory record has " + str((lenold-lennew)/3) + " more devices than the new inventory record!"
            print "Old Data for %s:, %s, %s, "%(elem,note,wsolddict[elem])
            print "New Data for %s:, %s, %s, "%(elem,note,wsnewdict[elem])
            #print "\n"

    print "~"*80
    print "*"*80
    print "Unchanged: %s, %d"%(diff_unchanged, len(diff_unchanged))
    print "*"*80

# Standard call to the main() function.
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print '\nUsage: inv_diff.py.py <siteid> <full path to new inventory file> <full path to old inventory file>\nExample: python inv_nb_check.py "1389" "/Users/Claudia/Box Sync/Network Transformation/Inventory/DiData-inventory-2015-06-15.xlsx" "/Users/Claudia/Box Sync/Network Transformation/Inventory/DiData-inventory-2015-04-20.xlsx"\nNote: Processing can take up to a minute!\n\n'
        sys.exit()
    else:
        main()