#!/usr/bin/python
import threading
import thread
import Queue
import time
from ftplib import FTP


# thread.allocate_Lock - Locks a thread until it finishes it's tasks, then it releases it's resources 
# and allows the program to terminate gracefully
gLock = thread.allocate_lock()

class WorkerThread(threading.Thread):
  """
  There are two ways to specify the activity: by passing a callable object to the constructor, 
  or by overriding the run() method in a subclass. No other methods (except for the constructor) 
  should be overridden in a subclass. In other words, only override the __init__() and run() 
  methods of this class.
  """

  def __init__(self, queue):
    threading.Thread.__init__(self)
    self.queue = queue

  def run(self):
    try:
      # Calling the lock for the threads here
      gLock.acquire()
#      print 'Inside worker thread'
      # In this section, different tasks can be added to be runned by the threads 
      while True:
        site = self.queue.get()
        ftp = FTP(host = site, timeout = .7)
        ftp.login()
        print """ ====================================================
Retrieving FTP DIR info from site:  %s
====================================================""" %(site)
        ftp.retrlines('LIST')
        print """ ====================================================
FTP List retrieved
===================================================="""
        ftp.quit()
        self.queue.task_done()
    except Exception as e:
      print 'Exception: %s' %(e)
    finally:
      # No matter what (Exception raised or not, the Lock gets released and all the 
      # resources asigned to it too.
      gLock.release()
      self.queue.task_done()

def get_ftp_list():
  ftp_list = []
  f_read = file('FTP_sites', 'r')
  ftp_list = f_read.readlines()
  return ftp_list

def main():
  # Make sure the queue gets filled before calling the workerTrhread method
  queue = Queue.Queue()
  ftp_list = get_ftp_list()
  for ftp_site in ftp_list:
    site = ftp_site[:-1]
    queue.put(site)
  for i in range(10):
#    print 'Creating Worker Thread: %d' %(i)
    worker = WorkerThread(queue)
    """
    A thread can be flagged as a "daemon thread". The significance of this flag is that
    the entire Python program exits when only daemon threads are left. The initial value
    is inherited from the creating thread. The flag can be set through the daemon property.
    """
    worker.setDaemon(True)
    """
    Once a thread object is created, its activity must be started by calling the thread's 
    start() method. This invokes the run() method in a separate thread of control.

    Note Daemon threads are abruptly stopped at shutdown. Their resources (such as open files, 
    database transactions, etc.) may not be released properly. If you want your threads to stop gracefully, 
    make them non-daemonic and use a suitable signalling mechanism such as an Event.
    """
    worker.start()
#    print 'WorkerThread %d Created!' %(i)


  """
  Other threads can call a thread's join() method. This blocks the calling thread until 
  the thread whose join() method is called is terminated
  """
  queue.join()
  print 'All tasks are over!'

#Standard Boilerplate
if __name__ == '__main__':
  main()
