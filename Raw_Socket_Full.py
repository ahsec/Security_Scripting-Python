#!/usr/bin/python
import socket
import struct
import binascii

""" Second version of the Simple packet sniffer that capture a packet of the for 0x0800
Prints the Ethernet and IP headers and exits. 
This version prints out more information about the Ethernet, IP and TCP headers

From the file "/usr/src/kernels/3.16.3-200.fc20.i686+PAE/include/uapi/linux/if_ether.h" 0x0003 means:
  define ETH_P_IP        0x0800          /* Internet Protocol packet     */   <<<< IPv4
"""

def start_sniffer():
  # create a socket that will listen for 0x800 packets (IP packets)
  rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
  # Waits for a packet coming from the specified Socket
  pkt = rawSocket.recvfrom(2048)
  print '+[Packet captured]: ' + str(pkt) + '\n'
  Ethernet_hdr_parser(pkt)
  IP_hdr_parser(pkt)
  TCP_hdr_parser(pkt)

def Ethernet_hdr_parser(pkt):
  # Ethernet Header is the first 14 bytes of the first part of the captured packet (Ethernet Header
  # IS always 14 bytes long
  ethernetHeader = pkt[0][0:14]
  # We break those 14 bytes into 3 arrays, first and second 6 bytes long and the last one 2 bytes long
  # All elements in Big Endian Notation
  eth_hdr = struct.unpack('>6s6s2s', ethernetHeader)
  print '+[Ethernet Header (14 bytes)]: %s' %(str(eth_hdr))
  # Converting from binary to hexadecimal in order to be more readable
  binascii.b2a_hex(eth_hdr[0])
  print '  -[Destination MAC Addr (6 bytes)]: %s' %(binascii.b2a_hex(eth_hdr[0]))
  print '  -[Source MAC Addr (6 bytes)]: %s' %(binascii.b2a_hex(eth_hdr[1]))
  print '  -[Ethernet Type (2 bytes)]: %s' %(binascii.b2a_hex(eth_hdr[2])) + '\n'

def IP_hdr_parser(pkt):
  # IP Header 20 bytes long
  ipHeader = pkt[0][14:34]
  ip_hdr = struct.unpack('>ssHHs5s4s4s', ipHeader)
  print '+[IP Header (20 bytes)]: %s' %(str(ip_hdr))
  # The first byte contains the IP version and the IHL (Internet Header Length), so we will split them 
  IPv_and_IHL = binascii.b2a_hex(ip_hdr[0])
  IPversion = IPv_and_IHL[0]
  IHL = IPv_and_IHL[1]
  # IHL in 32-bit words. Includes the length of any options fields and padding. Normal value is 5 (no options used)
  # (5 32-bit words = 5*4 = 20 bytes).
  print '  -[IP version (4 bits or 1/2 bytes)]: IPv%s' %(IPversion)
  print '  -[Header Length IHL (4 bits or 1/2 bytes)]: %s 32-bit words or %s bytes' %(IHL, (int(IHL)*4) )
  print '  -[Type of Service (1 byte)]: %s' %(str(ip_hdr[1]))
  print '  -[Total length in bytes (2 bytes)]: %s bytes' %(str(ip_hdr[2]))
  print '  -[Identification Number (2 bytes)]: %s ' %(str(ip_hdr[3]))
  # Flags use 3/8 of a byte and fragment offset 5/8 of a byte
  # We will read 1 byte, use the binary represantation and interpret from there
#  flags_and_off = binascii.a2b_hex(ip_hdr[4])
  flags_and_off = bin(int(ip_hdr[4])>>1)
#  flags = 
  print 'Flags and Offset %s or %s ' %(ip_hdr[4], binascii.b2a_hex(ip_hdr[4]))
  print '  -[Source IP Address (4 bytes)]: %s' %(socket.inet_ntoa(ip_hdr[6]))
  print '  -[Destination IP Address (4 bytes)]: %s' %(socket.inet_ntoa(ip_hdr[7])) + '\n'

def TCP_hdr_parser(pkt):
  # TCP Header. 20 bytes long
  tcpHeader = pkt[0][34:54]
  # First Unsigned short (H) is the source Port (2 bytes)
  # Second Unsigned short (H) is the destination Port (2 bytes)
  # The following HH is for the sequence number (4 bytes)
  tcp_hdr = struct.unpack('>HHHH12s', tcpHeader)
  print '+[TCP Header (20 bytes)]: %s' %str((tcp_hdr))
  print '  -[Source Port (2 bytes)]: %s' %(tcp_hdr[0])
  print '  -[Destination Port (2 bytes)]: %s' %(tcp_hdr[1])
  print '  -[Sequence Number (4 bytes)]: %s%s' %(tcp_hdr[2], tcp_hdr[3])

def main():
  start_sniffer()

if __name__ == '__main__':
  main()
