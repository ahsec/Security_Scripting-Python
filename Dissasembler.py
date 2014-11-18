#!/usr/bin/python
import pefile
import pydasm
import sys

# SPSE Module 6. Lesson 3. Exercise 1.
# Dissasembler that prints the first 200 bytes: HEX data and Dissasembled instructions
# ./Dissasembler.py EXE_File
# This script will dissasemble the first 200 bytes of the given EXE file


def dissasemble(filename):
  pe =  pefile.PE(filename)
  # Fetching Entry point header
  ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
  ep_ava = ep+pe.OPTIONAL_HEADER.ImageBase
  # Retrieve 200 bytes starting at the entry point 
  data = pe.get_memory_mapped_image()[ep:ep+200]
  offset = 0
  while offset < len(data):
    # Loop through the data and dissasemble
    i = pydasm.get_instruction(data[offset:], pydasm.MODE_32)
#    print hex(data[offset:]) +'    ' +  pydasm.get_instruction_string(i, pydasm.FORMAT_INTEL, ep_ava+offset)
    print pydasm.get_instruction_string(i, pydasm.FORMAT_INTEL, ep_ava+offset)
    offset += i.length

def usage():
  print """./Dissasembler.py EXE_File
This script will dissasemble the first 200 bytes of the given EXE file"""

def main():
  if len(sys.argv) < 2:
    usage()
  else:
    filename = sys.argv[1]
    dissasemble(filename)

if __name__ == '__main__':
  main()
