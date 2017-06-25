#!/usr/bin/python
import os

# This script creates a "child" process from a "parent" process. It will print 
# each process ID and then exit

def child_process():
  print 'I am the child, my PID is: %d' %(os.getpid())

def parent_process():
  print ' I am the parent, my PID is: %d' %(os.getpid())
  print ' I am about to get forked... '
  # Here we will fork the parent process
  child = os.fork()
  if child == 0:
    child_process()
  elif child != 0:
    print 'This is the Parent code'
    print 'My child has the PID: %d' %(child)

def main():
  parent_process()



# Standard Boiler plate
if __name__ == '__main__':
  main()
