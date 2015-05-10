
__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2015/05/05 21:57:19 $"
__copyright__ = "Copyright (c) 2015 Claudia de Luna"
__license__ = "Python"

# This script takes as input a directory which should have show commands including "show int status" output from one or more devices.

import os
import re
import sys

def countconnint(path):
    """
    Logic for counting connected interfaces

    """

    # Initialize Interface Type Counters
    TX=0
    SX=0
    LH=0
    FA=0
    FX=0
    CU=0


    total_files = 0
    print "Host," + "File, " + "Host," + "Subsystem,"+"Upgrade,"+ " Connected SX:, " + " Connected LH:, " + " Connected TX:, " + " Connected FA:, " + " Connected CU:, " + "Total Connected:, "
    # Iterate through all the files in the directory and count all "connected" connections by type
    for fn in os.listdir(path):
        if os.path.isfile(fn):
            #print (fn)
            lTX=0
            lSX=0
            lLH=0
            lCU=0
            lFX=0
            lFA=0
            lConnected=0
            NewModel=" "
            subsystem=" "
            #Open the file
            show = open(fn, "r")
            host = "not found"
            #print "LLLLLLLLLLLLLLLLLLLLLLLL"


            for line in show:
                #print line
                #Look for the hostname
                if re.match("^hostname(.*)", line):
                    host=line
                    host = host.rstrip()
                #print "@@@@@@@@Hostname " + host
                #Count only connected interfaces
                if re.match("(.*)connected(.*)",line):
                    lConnected=lConnected+1
                    if re.match("(.*)1000BaseSX(.*)", line):
                        #print "match" + line
                        lSX=lSX+1
                    #print host + " Number of SX Optics: " + str(SX)
                    if re.match("(.*)1000BaseLH(.*)", line):
                        #print "match" + line
                        lLH=lLH+1
                    #print "Number of LH Optics: " + str(LH)
                    if re.match("(.*)1000BaseT(.*)", line):
                        #print "match" + line
                        lTX=lTX+1
                    #print "Number of TX Optics: " + str(TX)
                    if re.match("(.*)100BaseT(.*)", line):
                        #print "match" + line
                        lFA=lFA+1
                    #print "Number of TX Optics: " + str(TX)
                    if re.match("(.*)100BaseF(.*)", line):
                        #print "match" + line
                        lFX=lFX+1
                    #print "Number of TX Optics: " + str(TX)
                    if re.match("(.*)CU(.*)", line):
                        #print "match" + line
                        lCU=lCU+1
                        #print "Number of CU Optics: " + str(CU)
            host1=host.split(" ")
            
            # If more than two fiber uplinks then execute the core/dist sizing code
            if lSX>2 or lLH>2:
                subsystem = "Possible Core or Distribution"

                # Port Count Logic
                # Option1 = 4500 with 32 ports
                # Option2 = 6880 with 2 modules and 48 ports
                # Option3 = 6880 with 3 modules and 64 ports
                # Option4 = 6880 with 4 moduels (maxed) and 80 ports
                # add 4 ports to total count to account for interlinks and keepalives
                opt1=32.0
                opt2=48.0
                opt3=64.0
                opt4=80.0
                NewModel=" "
                tports=lSX+lLH+lTX+lFA+lCU+3.0
                #print "Total New Ports: "+ str(tports)
                #print "Percentage1:"+str(((tports/opt1)*100))
                #print "Ratio1:"+str(((opt1-tports)/opt1)*100)
                #print "Evaluates to:"+str(((tports/opt1)*100)<=80.0)
                #print "Percentage2:"+str(((tports/opt2)*100))
                #print "Ratio2:"+str(((opt2-tports)/opt2)*100)
                #print "Evaluates to:"+str(((tports/opt2)*100)<=80.0)
                #print "Percentage3:"+str(((tports/opt3)*100))
                #print "Ratio3:"+str(((opt3-tports)/opt3)*100)
                #print "Evaluates to:"+str(((tports/opt3)*100)<=80.0)
                #print "Percentage4:"+str(((tports/opt4)*100))
                #print "Ratio4:"+str(((opt4-tports)/opt4)*100)
                #print "Evaluates to:"+str(((tports/opt4)*100)<=80.0)


                if (((opt1-tports)/opt1)*100)>20.0:
                    NewModel="Recommend New Model: Catalyst 4500X 32 SFP providing " + str((((opt1-tports)/opt1)*100)) + " percent growth capacity"
                elif (((opt2-tports)/opt2)*100)>20.0:
                    NewModel="Recommend New Model:Catalyst 6880X-LE + 2 Modules providing " + str((((opt2-tports)/opt2)*100)) + " percent growth capacity"
                elif (((opt3-tports)/opt3)*100)>20.0:
                    NewModel="Recommend New Model:Catalyst 6880X-LE + 3 Modules providing " + str((((opt3-tports)/opt3)*100)) + " percent growth capacity"
                elif (((opt4-tports)/opt4)*100)>20.0:
                    NewModel = "Recommend New Model:Catalyst 6880X-LE  4 Modules (Maxed) and not within 20 percent providing "	+ str((((opt4-tports)/opt4)*100)) + " percent growth capacity"
                else:
                    NewModel="Review Manually"

            print host1[1] +","+ fn + "," + host + ", "+ subsystem + "," + NewModel + "," + str(lSX) + "," +  str(lLH) + "," +  str(lTX) + "," +  str(lFA) + "," + str(lCU) + "," + str(lSX+lLH+lTX+lFA+lCU)
            #print fn + "," + host + " ,Number of LH Optics in this switch:, " + str(lLH)
            #print fn + "," + host + " ,Number of TX Optics in this switch:, " + str(lTX)
            #print fn + "," + host + " ,Number of CU Optics in this switch:, " + str(lCU)
            #print "LLLLLLLLLLLLLLLLLLLLLLLL"
            # close the file
            show.close()
        SX=SX+lSX
        LH=LH+lLH
        TX=TX+lTX
        FA=FA+lFA
        FX=FX+lFX
        CU=CU+lCU
        total_files = total_files +1

    print "*********************************"
    print fn
    print " TOTAL Number of SX Optics:, " + str(SX)
    print " TOTAL Number of LH Optics:, " + str(LH)
    print " TOTAL Number of TX Optics:, " + str(TX)
    print " TOTAL Number of 100BaseTX Optics:, " + str(FA)
    print " TOTAL Number of FX Optics:, " + str(FX)
    print " TOTAL Number of CU Optics:, " + str(CU)

    total_files = total_files +1

    print "Total Number of files in "+ path + " is, " + str(total_files)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "~" *79
        print 'Usage: conn_int.py <directory of show command output files>  '
        print 'Example:python /Users/Claudia/pyscripts/conn_int.py "/Users/Claudia/pyscripts/showcommandsv2"'
        print "~" *79
        sys.exit()
    else:
        fpath = sys.argv[1]
        if not os.path.exists(fpath):
            print "Could not locate folder of show commands. Please verify path."
            sys.exit()
        else:
            scfpath = ''
            for subdir, dirs, files in os.walk(fpath):
                for file in files:
                    if os.path.splitext(file)[1][1:] in ('txt'):
                        scfpath = os.path.join(subdir, file)
                        print "="* 79
                        print "\n \n Counting connected interfaces in ", scfpath
                        try:
                            countconnint(scfpath)
                        except:
                            print "Could not count connected interfaces in ", scfpath

