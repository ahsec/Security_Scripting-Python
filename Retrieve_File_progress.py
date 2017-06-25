#!/usr/bin/python
import sys
import urllib

###################################################
# SPSE Module 4. Lesson 1. Ex 1.
# File Retriever from a URL.
# It shows the progress and validates that the 
# file exists before retrieving it. Nice piece of work
###################################################

def show_progress(num_blks, blk_size, tot_size):
  # This function prints the progress of the transmission. It is being called from the urllib.urlretrieve function
  prog_bytes = num_blks * blk_size
  print '%s / %s [bytes]' %(prog_bytes, tot_size)

def get_code(url):
  # This function gets the HTTP code from trying to read the file in the URL
  # Will work to verify if the file exists
  tx = urllib.urlopen(url)
  code = tx.code
  return code
  
def get_file(url):
  # Run function to verify that the file exist.
  code = get_code(url)
  if code != 200:
    print "File doesn't exist, please verify your URL"
  else:
    # Gets the filename from the URL
    parts = parts = url.rsplit('/')
    name = parts[-1]
    # Retrieves the file from the URL using the function "show_progress" to show the progress, duh!
    filename, headers = urllib.urlretrieve(url,name , show_progress)
    print '+[Transfer finished]'
    print '+[File saved in]: %s' %(filename)

def usage():
  print """Usage: Retrieve_File_progress.py URL
This script will retrieve the file located in the URL and it will show the progress of such transmission
URL must be in the form http://any.com/file.pdf"""

def main():
  # Verify that there's a second argument before executing
  if len(sys.argv) < 2:
    usage()
  else:
    get_file(sys.argv[1])

if __name__ == '__main__':
  main()
