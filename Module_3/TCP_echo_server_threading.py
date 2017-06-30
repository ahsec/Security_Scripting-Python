import threading
import socket
import sys
'''
The process is: Cretae a thread, assign tasks to that thread (handling
incoming connections and reply back), In the main process, create the socket
and assign it to a thread
'''
class Thread(threading.Thread):
  # Creating a regular thread !!
  # asigning client and lock variables
  def __init__(self, client, lock):
    threading.Thread.__init__(self)
    self.client = client
    self.lock = lock

  def run(self):
    # This is the code that the thread will execute
    # Listen for connections, receives and sends data
    self.lock.acquire()
    try:
      self.client.send("\nSay something\n")
      data = "dummie"
      while len(data):
        data = self.client.recv(2048)
        print "Client sent: ",data
        self.client.send(data)
      print "Client Exiting"
      client.close()
    finally:
      self.lock.release()

print "Creating Socket"
try:
  tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcpSocket.bind(("0.0.0.0", 8000))
  tcpSocket.listen(10)
except socket.error, msg:
  print "Failed to create socket. Error: " + str(msg[0])  +\
        " , Error message " + str(msg[1])
  sys.exit()

print "Socket Created"

while True:
  print "Waiting for another connection"
  lock = threading.Lock()
  (client, (ip, port)) = tcpSocket.accept()
  print "Creating thread for " + str(ip) + " with port " + str(port)
  #Start socket accept in a new thread
  thread = Thread(client, lock)
  thread.setDaemon(True)
  thread.start()
