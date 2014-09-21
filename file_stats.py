#!/usr/bin/python
import os
import sys


# Exercise number 2 of the SecurityTube Python Scripting Expert.
# For any given filename list out all the stats related to the file 
# such as size, creation time, etc

def print_stats(filename):
  last_access_t = os.path.getatime(filename)
  last_modif_t = os.path.getmtime(filename)
  size = os.path = os.path.getsize(filename)
  print 'Filename: ' + filename 
  print 'Time of Last Access: ' + str(last_access_t)
  print 'Time of Last Modification: ' + str(last_modif_t)
  # Convert size from blocks to Kilobytes
  print 'Size of the file: ' + str(size * .0043716) + 'K'


def main():
  args = sys.argv[1:]
  if not args:
    print """Usage: file_stats.py filename 
file_stats.py will print the statistics of a given file filename"""
  else:
    print_stats(args[0])

# Standard boiler plate
if __name__ == '__main__':
  main()
