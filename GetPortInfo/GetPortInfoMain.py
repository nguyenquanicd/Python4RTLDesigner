#!/usr/bin/python3.6

#-------------------------------------------------------
# Author   : Quan Nguyen
# Date     : Aug.31.2021
# Function : Extract the input/output/inout ports of Verilog/System Verilog
#-------------------------------------------------------
# History:
#   Date        :
#   Person      :
#   Description :
#-------------------------------------------------------
#
#Python library
#
# System specific parameters and functions
import sys
#Logging facility for Python
import logging
#Basic date and time types
import datetime
#Portable password input
import getpass
#Miscellaneous operating system interfaces
import os
#Regular expression operations
import re
#User library
import GetPortInfoFunc
#
#Common information
#
print ("1. Get the common information")
UserName   = getpass.getuser()
WorkDir    = os.getcwd()
DateTime   = datetime.datetime.today() #yyyy-mm-dd hh:mm:ss.sssss
DateTime   = str(DateTime)
DateTime   = DateTime.split(".")
DateTime   = DateTime[0]
#
#Check arguments
#
print ("2. Check the arguments")
ArgvNum    = len(sys.argv)
ScriptName = sys.argv[0]
InputLink  = GetPortInfoFunc.argcheck(sys.argv)
InputFile  = InputLink.split('/')
InputFile  = InputFile[len(InputFile)-1]
#
#Create the log file
#
LogFile = "run.log"
if os.path.exists(LogFile):
    os.remove(LogFile)
logging.basicConfig(filename=LogFile, level=logging.INFO)
logging.info ("#----------------------------------------")
logging.info ("# User                : " + UserName)
logging.info ("# Working Dir         : " + WorkDir)
logging.info ("# Date and Time       : " + str(DateTime))
logging.info ("# Number of arguments : " + str(ArgvNum-1))
logging.info ("# Command             : " + str(sys.argv).replace("['", "").replace("']", ""))
logging.info ("#----------------------------------------")
#
#Analyze the input file
#
print ("3. Analyze the RTL file: " + InputLink)
RTLFileH   = open(InputLink, "r")
OutputLine = ["No.,Direction,Type,Width,Name"]
RowIndex   = 0
StartCommentBlock = 0
for line in RTLFileH:
    line = re.sub("//.*", "", line)
    line = re.sub("/\*.*\*/", " ", line)
    line = line.lstrip()
    if (re.search("^/\*", line)):
        StartCommentBlock = 1
    elif (StartCommentBlock == 1):
        if (re.search("\*/$", line)):
            StartCommentBlock = 0
    elif (re.search("^input ", line)
       or re.search("^output ", line)
       or re.search("^inout ", line)):
           line = re.sub("]", "] ", line)
           line = re.sub("\[", " [", line)
           line = re.sub("\s+", " ", line)
           line = re.sub("] \[", "][", line)
           line = re.sub("[,;]", "", line)
           line = line.rstrip()
           #
           CharArray = line.split(" ")
           FieldNum  = len(CharArray)
           if (FieldNum == 2): #<Direction><Port_name>
               line = re.sub(" ", ",,,", line)
           elif (FieldNum == 3): #<Direction>[<Type> | <Width>]<Port_name>
               if (re.search("\[", line)): #<Direction><Width><Port_name>
                   line = re.sub(" \[", ",,[", line)
               else: #<Direction><Type><Port_name>
                   EndOfLine = CharArray[FieldNum-1]
                   line = re.sub(EndOfLine, ("," + EndOfLine), line)
           #<Direction><Type><Width><Port_name>
           line = re.sub(" ", ",", line)
           RowIndex = RowIndex + 1
           OutputLine.append(str(RowIndex) + "," + line)
RTLFileH.close()
#
#Create the output file
#
OutputFile = InputFile + ".csv"
print ("4. Generate the output file: " + OutputFile)
OutputFileH = open(OutputFile, "w")
for line in OutputLine:
    OutputFileH.write(line + "\n")
OutputFileH.close()

print ("#----------------------------------------")
print ("#END of the script : ", ScriptName)
print ("#----------------------------------------")

