#!/usr/bin/python
from StringIO import StringIO      # To redirect the Standard output to a variable
import Raw_Socket_Full
import sys

def sniff_filtered(filter_tuple):
  # From the arguments received we are trying to figure out what exactly the user wants to filter
  # Options are either source or destination ports with a port number
  source_dest = filter_tuple[0]
  port = filter_tuple[1]
  str_to_filter = ''
  if source_dest == 's':
    str_to_filter = '-[Source Port (2 bytes)]: '
  elif source_dest == 'd':
    str_to_filter = '-[Destination Port (2 bytes)]: '
  str_to_filter = str_to_filter + str(port)
  
  # We are expecting to receive some errors ... -_-
  try:
    # Store the reference, in case you want to show things again in standard output
    old_stdout = sys.stdout
    # This variable (result) will store everything that is sent to the standard output
    result = StringIO()
    sys.stdout = result
    # Doing some fancy stuff -- Starting the sniffer (output will be redirected)
    Raw_Socket_Full.start_sniffer()
    # Redirect again the std output to screen
    sys.stdout = old_stdout
    result_value = result.getvalue()
  #  print '---- Full output: %s ' %(result_value)
    if result_value.find(str_to_filter) > 0:
      print result_value
  except Exception as error:
    print(error)
    print 'Terinating Sniffer'
    return -1
    exit
  
def main():
  args = sys.argv[1:]
  filter_tuple = ()
  if not args:
    print 'Usage: Sniffer_options.py [s Source Port number to filter by |d Destination Port number to filter by]'
    return 0 
    exit
  else:
    if args[0] == 's' or args[0] == 'd':
     filter_tuple = (args[0], int(args[1]))
    else:
      print 'Usage: Sniffer_options.py [s Source Port number to filter by |d Destination Port number to filter by]'
      return 0
      exit
  # We are running the Sniffer FOREVER !!!
  # Or until we receive a Ctrl + C ...
  while True:
    print sniff_filtered(filter_tuple)
    
if __name__ == '__main__':
  main()
