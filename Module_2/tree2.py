#!/usr/bin/python
import os
import sys
'''
Script that emulates the functionality of the tree program in Linux
Tree is a recursive directory listing program that produces a depth indented
listing of files.
'''
# Variable to track how deep in a directory or sequence of directories we are at
depth = 0

# Recursive function
def walk(pth):
  global depth
  depth = depth + 1
  (base_path, dirs, files) = os.walk(pth).next()
  if dirs:
    for dir_index in dirs:
      if dir_index[0] != '.':
      # Doesn't include hidden directories
        print '--' * depth + dir_index
        walk(os.path.join(base_path, dir_index))
  for file_name in files:
      print '--' * depth + file_name
      depth = depth - 1

def main():
  rootdir = sys.argv[1]
  global depth
  walk(rootdir)

if __name__ == '__main__':
  main()
