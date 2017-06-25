#!/usr/bin/python
from scapy.all import *

""" SPSE Module 3. Lesson 6. Exercise 2
A network sniffer that reads all the SSID beacons prints the result """
# Requires an interface in monitor mode (not required but better if you have it is an interface 
# that could be changing frequencies 

def start_SSID_sniffer():
  print """############################################################
                           SSID List
############################################################"""
  ssid_list = []
  while True:
    # That is the name of the interface that my Alfa card gets ...
    pkt = sniff(iface = 'wlp0s19f2u2', count = 1)
    # Verifying that the packet received has a Beacon info in it
    if Dot11Beacon in pkt[0] :
      if pkt[0].info not in ssid_list:
        ssid_list.append(pkt[0].info)
        print pkt[0].info

def main():
   start_SSID_sniffer()

if __name__ == '__main__':
  main()
