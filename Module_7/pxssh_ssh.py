#!/usr/bin/env python
import pxssh
import sys
'''
SPSE Module 7. Lesson 1
Automating ssh sessions using pxssh
'''
def send_command(session, command) :
    session.sendline(command)
    session.prompt()
    print session.before

def connect(host, user, passwd) :
    try :
        session = pxssh.pxssh()
        session.login(host, user, passwd)
        return session
    except :
        print '[-] Error connecting'
        exit(0)

def session_ssh(host, user, passwd, command):
  session = connect(host, user, passwd)
  send_command(session, command)

def usage():
  print """pxssh_ssh.py
        This script will connect to a ssh server HOST using the provided
        USER and PASSWD and will issue the command and show the result"""

def main():
  host = '192.168.1.7'
  user = 'root'
  passwd = 'openelec'
  command = 'uname -a'
  session_ssh(host, user, passwd, command)

if __name__ == '__main__':
  main()
