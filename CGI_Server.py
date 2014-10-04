#!/usr/bin/python
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()    # Enables CGI error reporting

# Simple CGI server, uses the default CGIHTTPServer handler

def start_cgi_server():
  # Define a regular HTTP Server but ...
  server = BaseHTTPServer.HTTPServer
  # The handler is the CGI Handler GENIUS !!
  handler = CGIHTTPServer.CGIHTTPRequestHandler
  server_address = ('', 10001)
  # Directory for CGI scripts (from the current directory)
  handler.cgi_directories = ['/cgi']
  # Go get them CGI Server !!
  httpd = server(server_address, handler)
  httpd.serve_forever()

def main():
  start_cgi_server()

if __name__ == '__main__':
  main()
