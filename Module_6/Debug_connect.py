#!/usr/bin/env python
from pydbg import *
from pydbg.defines import *
import sys
dbg = pydbg()

def usage():
  print """Debug_connect ProcessName
This script will bind to the process specified in the process_name and
will log all the incoming and outgoing connections started/received by it"""

def send_bp(dbg):
  print 'Send() called!'
  print dbg.dump_context(dbg.context)
  return DBG_CONTINUE

def rcv_bp(dbg):
  print 'Receive() called!'
  print dbg.dump_context(dbg.context)
  return DBG_CONTINUE

def debug(pname):
  for (pid, name) in dbg.enumerate_processes():
    if name.lower() == pname.lower():
      dbg.attach(pid)

  rcv_api_addr = dbg.func_resolve("ws2_32", "recv")
  dbg.bp_set(rcv_api_addr, description = 'Recieve BreakPoint', handler = rcv_bp)
  send_api_addr = dbg.func_resolve("ws2_32", "send")
  dbg.bp_set(send_api_addr, description = 'Send BreakPoint', handler = send_bp)
  dbg.run()

def main():
  if len(sys.argv) < 2:
    usage()
  else:
    pname = sys.argv[1]
    debug(pname)

if __name__ == '__main__':
  main()
