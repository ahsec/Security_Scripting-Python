#!/usr/bin/python
import os
import socket
import sys

# This script creates a "child" process from a "parent" process. 
# The chlid process will process incoming connections, the parent creates child 
# by demand (like all parents do)

def child_process(client):
  print 'I am the child, my PID is: %d' %(os.getpid())
  print 'My parents PID is %d' %(os.getppid())

  try:
    client.send("\nSay something\n")
    data = 'dummie'
    while len(data):
      data = client.recv(2048)
      print 'Client sent: %s' %(data)
      client.send(data)
    print 'Client Exiting'
    client.close()
  finally:
    pass

def parent_process():
  print ' I am the parent, my PID is: %d' %(os.getpid())
  print ' I am about to get forked... just not yet, first we need an incmoing connection...'

  print "Creating Socket"
  try:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.bind(("0.0.0.0", 8000))
    tcpSocket.listen(10)
  except socket.error, msg:
    print "Failed to create socket. Error: " + str(msg[0])  + " , Error message " + str(msg[1])
    sys.exit()

  print "Socket Created"

  while True:
    print "Waiting for another connection"
    (client, (ip, port)) = tcpSocket.accept()
    print "Creating process for client IP " + str(ip) + " with client port " + str(port)
    #Start socket accept in a new thread
    child = os.fork()
    if child == 0:
      child_process(client)
    else:
      print 'This is the parent code'
      print 'My child has the PID %d' %(child)


def main():
  parent_process()

# Standard Boiler plate
if __name__ == '__main__':
  main()
