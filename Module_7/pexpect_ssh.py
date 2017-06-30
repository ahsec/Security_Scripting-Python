#!/usr/bin/env python
import pexpect, sys

def printing(response):
  for line in response.split('\n'):
    print line

def automate_ssh(ipaddress):
#  ip = int(ipaddress)
  command = 'ssh userid@%s' %(ipaddress)
  ssh_newkey = 'Are you sure you want to continue connecting'
  p = pexpect.spawn(command)

  i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
  if i == 0:
    print '[+] Importing new SSH key'
    p.sendline('yes')
    i = p.expect([ssh_newkey, 'password:', pexpect.EOF])
  if i == 1:
    print '[+] Sending password'
    p.sendline('PASSWORD')
    j = p.expect(['#', '$', pexpect.EOF])
    print p.before
    if j == 0 or j == 1:
      print '[+] Issuing commands'
      p.sendline('pwd')
      k = p.expect(['#', '$', pexpect.EOF])
      print p.before
      print p.match
      print p.after

      if k == 0 or k == 1:
        print p.before
        print p.match
        print p.after
        printing(p.before)
        printing(p.after)
      else:
        print '[-] Issuing command failed'
    else:
      print '[-] Authentication failed'
  elif i == 2:
    print 'Key or connection timeout'

def usage():
  print """pexpect_ssh.py IP_Address
Starts a SSH connection to the SSH server running in the IP Address.
It sends "uname -a" and "ls -l" commands"""

def main():
  if len(sys.argv) < 2:
    usage()
  else:
    automate_ssh(sys.argv[1])

if __name__ == '__main__':
  main()
