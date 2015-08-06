#!/usr/bin/python -tt
# inv_nb_check.py
# Claudia
# PyCharm
__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "6/21/15  12:17 PM"
__copyright__ = "Copyright (c) 2015 Claudia de Luna"
__license__ = "Python"

import sys
import re
import os
import xlrd


#def var(var1):


# Provided main() calls the above functions
def main():
    # Take path argument and list all text files
    """
    Description
    :return:
    """

    siteid=sys.argv[1]
    #siteid=1389

    inv=sys.argv[2]
    #inv="/Users/Claudia/Box Sync/Network Transformation/Inventory/DiData-inventory-2015-06-15.xlsx"

    invsh="Chassis & Module"

    nbdir=sys.argv[3]
    #nbdir="/Users/Claudia/Box Sync/Network Transformation/Sites/North America - Year One/1389-Ontario-CA-Solar/show_commands_detail_06.15.15"

    siterows=0
    not_only="No"

    nbfiles=os.listdir(nbdir)
    #print nbfiles
    #nbf=nbfiles.lower()
    nbf=[x.lower() for x in nbfiles]
    #print nbfiles
    #for file in nbfiles:
        #print file

    wb = xlrd.open_workbook(inv)
    ws = wb.sheet_by_name(invsh)

    wrong_names = []

    print "DiData Inventory Workbook in use:, %s"%(inv)
    print "DiData Inventory Worksheet in use:, %s"%(ws.name)
    print "Total number of rows in the Inventory Worksheet:, %d"%(ws.nrows)
    print "Total number of columns in the Inventory Worksheet:, %d"%(ws.ncols)
    print "Netbrain (NB) Output file directory:, %s"%(nbdir)
    print "Site ID to search:, %s"%(siteid)
    print ("-")*80
    print "Name, IP Address, Slot, Model, Filename, NB File Found"

    for row_index in range(ws.nrows):
        if ws.cell_value(row_index,6) == int(siteid):
            sw=(ws.cell_value(row_index,1))
            sw=sw.lower()
            swfile=sw+".txt"
            #print ws.cell_value(row_index,1)
            #print ws.cell_type(row_index,6)
            #print ws.cell_value(row_index,6)
            siterows=siterows+1
            #print sw
            #print swfile
            if swfile in nbf:
 #               print "%s,%s,%s,%s,swfile,NB File Found"%(ws.cell_value(row_index,1),ws.cell_value(row_index,2),ws.cell_value(row_index,3),ws.cell_value(row_index,4))
                print "**"
            else:
                print "%s,%s,%s,%s,swfile,NB File NOT Found"%(ws.cell_value(row_index,1),ws.cell_value(row_index,2),ws.cell_value(row_index,3),ws.cell_value(row_index,4))
            model = ws.cell_value(row_index,4)
            #print "Model: ", model
            #print "hostname: ", sw

            if "-ap" in sw and "AIR" not in str(model):
                #print "bad name"
                wrong_name_text = sw + "," + str(model) + "," + ws.cell_value(row_index,2)
                wrong_names.append(wrong_name_text)


    print ("-")*80
    print str(siterows)
    print ' ****************** BAD NAMES ******************'
    #print str(wrong_names)

    for line in wrong_names:
        print line



# Standard call to the main() function.
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print '\nUsage: inv_nb_check.py.py <siteid> <full path to inventory file> <full path to NB show command output directory>\nExample: python inv_nb_check.py "1389" "/Users/Claudia/Box Sync/Network Transformation/Inventory/DiData-inventory-2015-06-15.xlsx" "/Users/Claudia/Box Sync/Network Transformation/Sites/North America - Year One/1389-Ontario-CA-Solar/show_commands_detail_06.15.15"\nNote: Processing can take up to a minute!\n\n'
        sys.exit()
    else:
        main()

