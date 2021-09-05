#-------------------------------------------------------
# Author   : Quan Nguyen
# Date     : Aug.31.2021
# Function : Extract the input/output/inout ports of Verilog/System Verilog
#-------------------------------------------------------
import sys
import re
#User library
#
#Function
#
#Check the arguments
def argcheck(arg = sys.argv):
    ArgArray   = arg
    ScriptName = ArgArray[0]     #Get the script name
    ArgArray.pop(0) #Remove the script name
    if (len(ArgArray) == 0):
        print ("[Error] Please fill an RTL file")
        print ("Example: " + ScriptName + " Top.sv")
        sys.exit()
    elif ((ArgArray[0] == "-help") or (ArgArray[0] == "-h")):
        print ("Usage: " + ScriptName + " [RTL_file]")
        print ("Get the input, output, inout ports from a Verilog or SystemVerilog file")
        print ("Example: " + ScriptName + " Top.sv")
        sys.exit()
    elif not (re.search(".v$", ArgArray[0]) or re.search(".sv$", ArgArray[0])
            or re.search(".svh$", ArgArray[0])):
        print (ArgArray[0] + " is not a Verilog or System Verilog file")
        sys.exit()
    #Return the link of RTL file
    return ArgArray[0]

#-------------------------------------------------------
#END of file
#-------------------------------------------------------
