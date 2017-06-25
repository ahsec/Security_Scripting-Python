#!/usr/bin/python
import socket
import threading
import SocketServer
'''
Echo server that uses ThreadedTCPRequestHandler: Uses threads to handle
incoming connections. Can handle multiple connections at the same time
'''
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
  '''
  This is the thread code. It can be whatever you want, this section defines
  what are the threads going to do. (The main thread just creates 'child'
  threads.
  '''
  def handle(self):
    # In this case we just wait for data and return it to the client
    data = 'dummy'
    while len(data):
      data = self.request.recv(1024)
      print 'Client %s, sent: %s' %(self.client_address, data)
      cur_thread = threading.current_thread()
      self.request.sendall(data)
    print 'Client disconnected...'

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

def main():
  # Assigns an IP and a port to the server
  HOST, PORT = "0.0.0.0", 9000
  # Creates a Threaded TCP Server and sets it to listen for incoming connections
  server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
  ip, port = server.server_address

  # Start a thread with the server -- that thread will then start one
  # more thread for each request
  server_thread = threading.Thread(target=server.serve_forever)
  # Exit the server thread when the main thread terminates
  # server_thread.daemon = True
  server_thread.start()
  print 'Server loop running in thread: %s' %(server_thread.name)
  print 'Waiting for incoming connections...'

if __name__ == "__main__":
  main()
