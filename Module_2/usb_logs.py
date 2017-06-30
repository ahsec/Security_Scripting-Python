#!/usr/bin/python

import sys
""" 
This pyhton script reads all the messages from the /var/log/messages
files and prints out the messages related to usb
"""

def get_log_messages(string):
  # This function opens the file /var/log/messages with reading permissions
  # and looks for a string in it, such string will be passed in the args
  try:
    filed = open("/var/log/messages", 'r')
    list_lines = filed.readlines()
    for line in list_lines:
      if string in line or str.lower(string) in line:
        print line
  except IOError as detail:
    print "Error trying to read file: /var/log/messages: -> " + str(detail)


def main():
  args = sys.argv[1:]

  if not args:
    print """Usage: python usb_logs.py string
Where string is the string to look for in the /var/log/messages log file """
  else:
    get_log_messages(args[0])


# Default boiler plate for main
if __name__ == '__main__':
  main()
