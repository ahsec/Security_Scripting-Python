
### Module 6

* Debug_connect.py  
  Binds to the process specified in the process_name and logs all the incoming
and outgoing connections started or received by it

* Dissasembler.py  
  Dissasembler that prints the first 200 bytes: HEX data and disassembled
instructions of an EXE file.

* Load_exe_debug.py  
  Load an executable file especified from command line and debug it using
pydbg, looking for buffer overflow errors.

* search_dll.py  
  syntax: ```search_dll.py EXE_filename [dll_name]```  
  If no dll_name is provided, this script will list all the dll files imported by the EXE file provided. If a dll_name is provided, this script will look in the Executable for the provided dll and return True if present or False if not
