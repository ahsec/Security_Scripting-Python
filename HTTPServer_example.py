#!/bin/usr/python
import SimpleHTTPServer
import SocketServer

""" SPSE Module 3. Simple HTTP Server.
This example creates a simple HTTP Server that listens on port 10001.
"""

class HTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  # This section defines an HTTP Request Handler, not using the default "SimpleHTTPServer.SimpleHTTPRequestHandler"
  # at least, not yet
  def do_GET(self):
    # The "special" thing about this handler is that it recognizes when there is an '/admin' in the URL
    # and retrieves a "special" page for the super sleek admin
    # This is done by overwriting the do_GET method
    if self.path == '/admin':
      self.wfile.write('Admin Page')
      self.wfile.write(self.headers)
    else:
      # If the '/admin' is not in the URL it calls the default HTTP Handler:
      # SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET
      SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

def start_http_server():
  # This is just creating the server with the necessary parameters
  PORT = 10001
  IP_Addr = '0.0.0.0'
  Handler = HTTPRequestHandler
  httpd = SocketServer.TCPServer((IP_Addr, PORT), Handler)
  httpd.serve_forever()

def main():
  start_http_server()

if __name__ == '__main__':
  main()
