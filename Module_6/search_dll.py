#!/usr/bin/python
import pefile
import sys
'''
# SPSE Module 6. Lesson 2. Reverse Engineering
# search_dll.py EXE_filename [dll_name]
# If no dll_name is provided, this script will list all the dll files
# imported by the EXE file provided. If a dll_name is provided, this script
# will look in the Executable for the provided dll and return True if present
# or False if not
'''
def search_dll(filename, dll_name):
  result = False
  dll_name = dll_name.lower()
  # Getting the list (by using the get_dlls function
  dll_list = get_dlls(filename)
  for entry in dll_list:
    # Compare lowercase input against lower case found,
    # If match result = True
    found = entry.lower()
    if found == dll_name:
      result = True
  print result

def get_dlls(filename):
  dll_list = []
  # Opening the exe file with the pefile library
  pe = pefile.PE(filename)
  for entry in pe.DIRECTORY_ENTRY_IMPORT:
    # Reading the dlls entries and saving the found files in the dll_list list
    dll_list.append(entry.dll)
  return dll_list

def print_dlls(filename):
  # We get the dll list from the get_dlls function
  dll_list = get_dlls(filename)
    # This section will format and print the output in a "nice" way
  if len(dll_list) > 0:
    string = 'List of DLL files imported by: %s' %(filename)
    print string
    print '-'*len(string)
    for entry in dll_list:
      print '+ %s' %(entry)
  else:
    print 'No DLL files were found in the %s' %(filename)

def usage():
 print """search_dll.py EXE_filename [dll_name]
       If no dll_name is provided, this script will list all the dll files
       imported by the EXE file provided. If a dll_name is provided,
       this script will look in the Executable for the provided dll and return
       True if present or False if not.
       """
def main():
  num_args = len(sys.argv)
  # At least 2 arguments must be provided
  if num_args < 2:
    usage()
  elif num_args == 2:
    # If only 2 args, we will print the dll files imported by this exe file
    filename = sys.argv[1]
    print_dlls(filename)
  else:
    # We will look for a particular dll file in the exe file
    filename = sys.argv[1]
    dll_name = sys.argv[2]
    search_dll(filename, dll_name)

if __name__ == '__main__':
  main()
