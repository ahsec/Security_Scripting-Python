#!/usr/bin/python
from scapy.all import *
"""
SPSE Module 03. Lesson 6. Exercise 1
Create an HTTP sniffer using Scapy.
It must print the HTTP headers and data in GET/POST
"""

def run_HTTP_Sniffer(interface, countn):
  while True:
    pkts = sniff(iface = interface  , count = countn, filter = 'port 80',
                 prn = lambda x: x.summary())
    if Raw in pkts[0]:
      print "###### Packet Load ######"
      print pkts[0].load

def main():
  # run_HTTP_Sniffer function receives interface name and number of packets
  # to sniff as arguments
  strings = run_HTTP_Sniffer('wlo2', 1)

if __name__ == '__main__':
  main()
