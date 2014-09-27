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
    signal.alarm(5)


def main():
  args = sys.argv[1:]
  if not args:
    print """
Usage: FTP_server.py PORT
This program sets a server that listens on port PORT
"""

  else:
    HOST = 'localhost'
    PORT = int(args[0])

    # Create the server, binding to localhost on port PORT
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    # Set a 5-second alarm
    signal.alarm(5)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    
if __name__ == "__main__":
  main()

