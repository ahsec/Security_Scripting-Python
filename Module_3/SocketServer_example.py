#!/usr/bin/python
import SocketServer
"""
SocketServer, echo server. Receives data (a string) from a client and
replies back with the exact same string)
Makes use of the SocketServer library, which makes programming servers and
clients easier !!!
Only handles one connection at a time, so we will have to create another
multithread version of it
"""
class EchoHandler(SocketServer.BaseRequestHandler):
  # EchoHandler method
  def handle(self):
    # Overriding the handle method in order to modify incoming data
    print 'Got connection from: %s, port: %s' %(self.client_address)
    data = 'dummy'
    while len(data):
      # Waits for data and prints it back
      data = self.request.recv(1024)
      print 'Client sent: %s' %(data)
      self.request.send(data)
    print 'Client left'

def server_set():
  # Setting up the server, IP address and port
  serverAddr = ('0.0.0.0', 9000)
  # Create SocketServer and set it to listen for incoming connections
  server = SocketServer.TCPServer(serverAddr, EchoHandler)
  server.serve_forever()

def main():
  server_set()

if __name__ == '__main__':
  main()
