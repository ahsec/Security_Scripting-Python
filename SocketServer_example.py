#!/usr/bin/python
import SocketServer

class EchoHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    print 'Got connection from: %s, port: %s' %(self.client_address)
    data = 'dummy'
    while len(data):
      data = self.request.recv(1024)
      print 'Client sent: %s' %(data)
      self.request.send(data)
    print 'Client left'

def server_set():
  serverAddr = ('0.0.0.0', 9000)
  server = SocketServer.TCPServer(serverAddr, EchoHandler)
  server.serve_forever()

def main():
  server_set()

if __name__ == '__main__':
  main()
