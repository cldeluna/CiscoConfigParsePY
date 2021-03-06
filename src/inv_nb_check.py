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

    outtxtfilename = siteid + "-inv-nb-check.txt"
    outtextfile = os.path.join(nbdir,outtxtfilename)

    outtxtfh = open(outtextfile, "w")

    print "*** Output Text File: %s"%outtextfile

    print "DiData Inventory Workbook in use:, %s"%(inv)
    outtxtfh.write("DiData Inventory Workbook in use:, %s"%(inv))
    outtxtfh.write("\n")
    print "DiData Inventory Worksheet in use:, %s"%(ws.name)
    outtxtfh.write("DiData Inventory Worksheet in use:, %s"%(ws.name))
    outtxtfh.write("\n")
    print "Total number of rows in the Inventory Worksheet:, %d"%(ws.nrows)
    outtxtfh.write("Total number of rows in the Inventory Worksheet:, %d"%(ws.nrows))
    outtxtfh.write("\n")
    print "Total number of columns in the Inventory Worksheet:, %d"%(ws.ncols)
    outtxtfh.write("Total number of columns in the Inventory Worksheet:, %d"%(ws.ncols))
    outtxtfh.write("\n")
    print "Netbrain (NB) Output file directory:, %s"%(nbdir)
    outtxtfh.write("Netbrain (NB) Output file directory:, %s"%(nbdir))
    outtxtfh.write("\n")
    print "Site ID to search:, %s"%(siteid)
    outtxtfh.write("Site ID to search:, %s"%(siteid))
    outtxtfh.write("\n")
    print ("-")*80
    outtxtfh.write(("-")*80)
    outtxtfh.write("\n")
    print "Name, IP Address, Slot, Model, Filename, NB File Found"
    outtxtfh.write("Name, IP Address, Slot, Model, Filename, NB File Found")
    outtxtfh.write("\n")

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
            #if swfile in nbf:
 #               print "%s,%s,%s,%s,swfile,NB File Found"%(ws.cell_value(row_index,1),ws.cell_value(row_index,2),ws.cell_value(row_index,3),ws.cell_value(row_index,4))
                #print "**"
            #else:
            if swfile not in nbf:
                print "%s,%s,%s,%s,swfile,NB File NOT Found"%(ws.cell_value(row_index,1),ws.cell_value(row_index,2),ws.cell_value(row_index,3),ws.cell_value(row_index,4))
                outtxtfh.write("%s,%s,%s,%s,swfile,NB File NOT Found"%(ws.cell_value(row_index,1),ws.cell_value(row_index,2),ws.cell_value(row_index,3),ws.cell_value(row_index,4)))
                outtxtfh.write("\n")
            model = ws.cell_value(row_index,4)
            #print "Model: ", model
            #print "hostname: ", sw

            if "-ap" in sw and "AIR" not in str(model):
                #print "bad name"
                wrong_name_text = sw + "," + str(model) + "," + ws.cell_value(row_index,2)
                wrong_names.append(wrong_name_text)


    print ("-")*80
    outtxtfh.write(("-")*80)
    outtxtfh.write("\n")

    print str(siterows)
    outtxtfh.write(str(siterows))
    outtxtfh.write("\n")
    outtxtfh.write("\n")

    if len(wrong_names) > 0:
        print ' ****************** BAD AP Models ******************'
        outtxtfh.write(' ****************** BAD AP Models ******************')
        outtxtfh.write("\n")
        print 'hostname, model, IP Address'
        outtxtfh.write('hostname, model, IP Address')
        outtxtfh.write("\n")
        #print str(wrong_names)
        for line in wrong_names:
            print line
            outtxtfh.write(line)
            outtxtfh.write("\n")

    outtxtfh.close()


# Standard call to the main() function.
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print '\nUsage: inv_nb_check.py.py <siteid> <full path to inventory file> <full path to NB show command output directory>\nExample: python inv_nb_check.py "1389" "/Users/Claudia/Box Sync/Network Transformation/Inventory/DiData-inventory-2015-06-15.xlsx" "/Users/Claudia/Box Sync/Network Transformation/Sites/North America - Year One/1389-Ontario-CA-Solar/show_commands_detail_06.15.15"\nNote: Processing can take up to a minute!\n\n'
        sys.exit()
    else:
        main()

