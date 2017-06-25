#!/usr/bin/env python
DESC = "SPSE Module 5 Lesson 3 Ex. 1"
import immlib
import getopt
import immutils
from immutils import *

CMD_DIR = "./PyCommands"

def writeFile(text):
  filename = "output.txt"
  FILE = open(filename, "a")
  FILE.write(text + "\n")
  FILE.close()

def main(args):
  imm = immlib.Debugger()
  imm.log("Writing to my log Window")
  imm.updateLog()
  
  td = imm.createTable("SPSE Course", ["PID", "Name", "Path", "Services"])
  writeFile("PID, Name, Path, Services")
  psList = imm.ps()
  for process in psList:
    td.add(0, [ str(process[0]), process[1], process[2], str(process[3])])
    writeFile("%s   %s   %s   %s" %(str(process[0]), process[1], process[2], str(process[3])))
  return "[+] Output on the status bar"