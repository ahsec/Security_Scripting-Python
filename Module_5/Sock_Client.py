#!/usr/bin/env python
import socket
import sys

repited = 200
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.connect((sys.argv[1], 10000))
buffer = 'A'*repited
print 'A times %i' %(repited)
sock.send(buffer)
sock.close()