#!/usr/bin/python
import socket
import string

def start_tcp_echo_server():
  '''
  Create socket and define socket parameters: IP to listen to, Port,
  number of accepted connections (even though it doesn respond more than 1
  client at a time
  '''
  global tcpSocket
  tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcpSocket.bind(("0.0.0.0", 8000))
  tcpSocket.listen(2)
  print 'Waiting for a client...'

  # client will be called by the method stop_tcp_echo_server method, therefore,
  # will need it to be a global variable
  global client
  # tcpSocket.accept will accept connections and return:
  # a socket assigned to client, the client IP address (client_ip) and the
  # client port number (client_port)
  (client, (client_ip, client_port)) = tcpSocket.accept()
  print 'Recieved connection from: ', client_ip
  print 'Starting ECHO output...'

  data = 'dummy'
  while len(data):
    # While client is sending data, the server will return
    # the same (echo server)
    data = client.recv(2048)
    print 'Client sent: ', data
    if string.strip(data) == 'die server, die':
      # If client sends the string 'die server, die', server and client
      # will be terminated
      client.send('Terminating connection and server')
      data = ''
    client.send(data)

def stop_tcp_echo_server():
  # Closes client connection and terminates the server.
  # client and tcpSocket are global variables
  print 'Closing connection...'
  client.close()
  print 'Shutting down server...'
  tcpSocket.close()

def main():
  # Start and terminate the server once we receive the "die server, die" string
  start_tcp_echo_server()
  stop_tcp_echo_server()

# Standard boilerplate
if __name__ == '__main__':
  main()
