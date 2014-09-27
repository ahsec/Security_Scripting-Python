#!/usr/bin/python
import sys
import SocketServer
import signal

class MyTCPHandler(SocketServer.BaseRequestHandler):

  """
  The RequestHandler class for our server.

  It is instantiated once per connection to the server, and must
  override the handle() method to implement communication to the
  client.
  """

  def handle(self):
    # self.request is the TCP socket connected to the client
    self.data = self.request.recv(1024).strip()
    print "{} wrote:".format(self.client_address[0])
    print self.data
    # just send back the same data, but upper-cased
    self.request.sendall(self.data.upper())
    # Second call of the signal.alarm method. Re-sets the timeout counter to the original timeout value
    # Terminates the server if no connection is received in TIMEOUT seconds
    signal.alarm(timeout)

def create_server(HOST, PORT, timeout):
  # Create the server, binding to localhost on port PORT
  server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
  # First call to the signal.alarm method, Terminates the server if no connection is received in TIMEOUT seconds
  signal.alarm(timeout)
  # Activate the server; this will keep running until you interrupt the program with Ctrl-C
  server.serve_forever()

def main():
  args = sys.argv[1:]
  if len(args) < 2:
    print """
Usage: FTP_server.py PORT TIMEOUT
This program sets a server that listens on port PORT, if no connection is received in TIMEOUT seconds the server will be terminated
"""

  else:
    HOST = 'localhost'
    PORT = int(args[0])
    global timeout
    timeout = int(args[1])
    create_server(HOST, PORT, timeout)

# Standard Boiler Plate    
if __name__ == "__main__":
  main()

