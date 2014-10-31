#!/usr/bin/python
import sys
from scapy.all import *

#######################################################################
# SPSE Module 3, Lesson 8. Ex. 3
# SYN scanner. 
# Usage: Scapy_SYN_scan.py IP_Address
# This script will perform a SYN scan of the ports [21,22,23,80,443] for the IP_Address
# Sample output: 
# ---------------------------------------------------------
# Received 7 packets, got 6 answers, remaining 0 packets
# Port: 21 - TCP flags: 20
# Port: 22 - TCP flags: 18
# - Port: 22 responded with flags: SA
# Port: 23 - TCP flags: 20
# Port: 80 - TCP flags: 18
# - Port: 80 responded with flags: SA
# Port: 56 - TCP flags: 20
# ---------------------------------------------------------
#######################################################################

def syn_scan(ip):
  ans, unans = sr(IP(dst = ip)/TCP(flags = 'S', dport = [21,22,23,80,56,443]), timeout = 2)
  for i in range (0,len(ans)-1):
    print 'Port: %s - TCP flags: %s' %(ans[i][1][TCP].sport, ans[i][1][TCP].flags)
    if ans[i][1][TCP].flags == 18:
      print '- Port: %s responded with flags: SA' %(ans[i][1][TCP].sport)

def usage():
  print """Usage: Scapy_SYN_scan.py IP_Address
This script will perform a SYN scan of the ports [21,22,23,80,443] for the IP_Address host"""

def main():
  if len(sys.argv) < 2:
    usage()
  else:
    ip = str.strip(sys.argv[1])
    syn_scan(ip)

if __name__ == '__main__':
  main()
