#!/usr/bin/python
import socket
import struct
import binascii

""" Simple packet sniffer that capture a packet of the for 0x0800
Prints the Ethernet and IP headers and exits

From the file "/usr/src/kernels/3.16.3-200.fc20.i686+PAE/include/uapi/linux/if_ether.h" 0x0800 means:
  define ETH_P_IP        0x0800          /* Internet Protocol packet     */
"""

def start_sniffer():
  # create a socket that will listen for 0x800 packets (IP packets)
  rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
  # Waits for a packet coming from the specified Socket
  pkt = rawSocket.recvfrom(2048)
  print '+[Packet captured]: ' + str(pkt) + '\n'

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
  
  ipHeader = pkt[0][14:34]
  ip_hdr = struct.unpack('>12s4s4s', ipHeader)
  print '+[IP Header (20 bytes)]: %s' %(str(ip_hdr))
  print '  -[Initial 12 bytes of the IP Header]: %s' %(str(ip_hdr[0]))
  print '  -[Source IP Address (4 bytes)]: %s' %(socket.inet_ntoa(ip_hdr[1]))
  print '  -[Destination IP Address (4 byte)]: %s' %(socket.inet_ntoa(ip_hdr[2]))

  # Initial part of the TCP Header
  tcpHeader = pkt[0][34:54]
  tcp_hdr = struct.unpack('!HH16s', tcpHeader)

def main():
  start_sniffer()

if __name__ == '__main__':
  main()
