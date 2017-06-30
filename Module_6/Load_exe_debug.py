#!/usr/bin/env python
from pydbg import *
from pydbg.defines import *
from subprocess import call
import sys
dbg = pydbg()
'''
# SPSE Module 6. Lesson 4.
# Load an executable file especified from command line and debug it using
# pydbg, looking for buffer overflow errors. Sometimes on Windows it shows
# an error "Bind fails with error: 10048 "
# ToDo, figure out why ...
'''
def find_pid(dbg, filename):
  # SPlit the string using '/' as delimiter and selecting
  # the last resulting element
  process_name = filename.split('\\')[-1]
  process_name_l = process_name.lower()
  for (pid, proc_name) in dbg.enumerate_processes():
   # Using dbg we enumarate the processes and look for the filename
    if proc_name.lower() == process_name_l.strip():
      return pid
  return -1

def detect_overflow(dbg):
  if dbg.dbg.u.Exception.dwFirstChance:
    return DBG_EXCEPTION_NOT_HANDLED
  print 'Access Violation happened'
  print 'DBG context:'
  return DBG_EXCEPTION_NOT_HANDLED

def load_debug(filename):
  # First, we load the executable (filename)
  dbg.load(filename)
  # Now we get the PID associated to it
  pid = find_pid(dbg, filename)
  if pid == -1:
    print 'Process could not be found in memory'
    return -1
  print 'PID Of process is: -%i-' %(pid)
  # We attach to the process and Detect buffer overflows
  dbg.attach(int(pid))
  dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, detect_overflow)
  dbg.run()

def usage():
  print """Load_exe_debug.py FILENAME
        This script loads the executable file (FILENAME) and performs debugging
        activities on it once it is loaded on memory
        """
def main():
  if len(sys.argv) < 2:
    usage()
  else:
    filename = sys.argv[1]
    load_debug(filename)

if __name__ == '__main__':
  main()
