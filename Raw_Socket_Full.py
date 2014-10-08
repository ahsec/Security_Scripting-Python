#!/usr/bin/python
import socket
import struct
import binascii

""" Second version of the Simple packet sniffer that capture a packet of the for 0x0800
Prints the Ethernet and IP headers and exits. 
This version prints out more information about the Ethernet, IP and TCP headers

From the file "/usr/src/kernels/3.16.3-200.fc20.i686+PAE/include/uapi/linux/if_ether.h" 0x0003 means:
  define ETH_P_IP        0x0800          /* Internet Protocol packet     */   <<<< IPv4

Size of data types in pyhton:
  https://docs.python.org/2/library/struct.html
"""

def start_sniffer():
  # create a socket that will listen for 0x800 packets (IP packets)
  rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
  # Waits for a packet coming from the specified Socket
  pkt = rawSocket.recvfrom(2048)
  print '+[Packet captured]: ' + str(pkt) + '\n'
  # Calling each header Parser (Ethernet, IP and TCP)
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
  # Unpacking all the elements in the IP Header
  # IP version, IHL, ToS, Total Length, ID number, Flags, Fragment Offset, TTL, Protocol, Header Checksum, Source IP, Destination IP
  ip_hdr = struct.unpack('>ssHHsssHs4s4s', ipHeader)
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
  flags_and_off = binascii.b2a_hex(ip_hdr[4])
  flags_off_tuple = getBinRep(flags_and_off)
  flags = flags_off_tuple[0][2:5]
  flags = str(flags).rstrip('[]').replace(',','').replace('[','').replace('\'','').replace(' ','')
  offset = flags_off_tuple[0][5:]
  offset.append(flags_off_tuple[1][2:])
  offset = str(offset).rstrip('[]').replace(',','').replace('[','').replace('\'','').replace(' ','')
  print '  -[Flags (3 bits)]: %s ' %(flags)
  print '  -[Fragment offset (5 bits)]: %s' %(offset)
  print '  -[Time To Live TTL (1 byte) hex]: %s' %(binascii.b2a_hex(ip_hdr[5]))
  print '  -[Protocol (1 byte) hex]: %s' %(binascii.b2a_hex(ip_hdr[6]))
  print '  -[Header CheckSum (2 byte)]: %s' %(ip_hdr[7])
  # We use socket.inet_ntoa to convert from 32 bits notation to IP Address String 
  print '  -[Source IP Address (4 bytes)]: %s' %(socket.inet_ntoa(ip_hdr[9]))
  print '  -[Destination IP Address (4 bytes)]: %s' %(socket.inet_ntoa(ip_hdr[10])) + '\n'

def TCP_hdr_parser(pkt):
  # TCP Header. 20 bytes long
  tcpHeader = pkt[0][34:54]
  # First Unsigned short (H) is the source Port (2 bytes)
  # Second Unsigned short (H) is the destination Port (2 bytes)
  # The following I is for the sequence number (4 bytes)
  tcp_hdr = struct.unpack('>HHIIss6s', tcpHeader)
  print '+[TCP Header (20 bytes)]: %s' %str((tcp_hdr))
  print '  -[Source Port (2 bytes)]: %s' %(tcp_hdr[0])
  print '  -[Destination Port (2 bytes)]: %s' %(tcp_hdr[1])
  print '  -[Sequence Number (4 bytes)]: %s' %(tcp_hdr[2])
  print '  -[Acknowledgment Number (4 bytes)]: %s' %(tcp_hdr[3])
  # Data Offset 4 bits, Reserved (all zeros) 6 bits, Control bits 6 bits. Total 16 bits (ss)
  (dOffset, Rsvd, ctrl) = TCP_brk_options(tcp_hdr[4], tcp_hdr[5])
  print '  -[Data Offset (4 bits)]: %s 32 bit words or %s bytes' %(int(dOffset, base = 2), (int(dOffset, base = 2)*4))
  print '  -[Reserved (6 bits)]: %s' %(Rsvd)
  # Calling function "decode_ctrl_bits" to convert from bits to Flag names
  ctrl_names = decode_ctrl_bits(str(ctrl))
  print '  -[Control bits (6 bits)]: %s' %(ctrl_names)

def TCP_brk_options(part1, part2):
  # From 2 bytes (16 bits) we will get Data Offset(4 bits), Reserved Bits (6 bits) and Control bits (6 bits)
  bin1 = bin(int(binascii.b2a_hex(part1)))
#  bin1 = binascii.b2a_hex(part1)
  bin2 = bin(int(binascii.b2a_hex(part2)))
#  bin2 = binascii.b2a_hex(part2)
  # Calling function growBin to expand the size of the binary number to 10 characteres 
  part1 = growBin(bin1, 10)
  part2 = growBin(bin2, 10)
  # Breakin g the result (first part is Data offset)
  dOffset = part1[2:6]
  # Using rstrip to remove all the [],' characteres in the resulting string
  dOffset = str(dOffset).rstrip('[]').replace(',','').replace('[','').replace('\'','').replace(' ','')
  Rsvd = part1[6:]
  Rsvd.append(part2[2:4])
  Rsvd = str(Rsvd).rstrip('[]').replace(',','').replace('[','').replace('\'','').replace(' ','')
  ctrl = part2[4:]
  ctrl = str(ctrl).rstrip('[]').replace(',','').replace('[','').replace('\'','').replace(' ','')
  return (dOffset, Rsvd, ctrl)

def getBinRep(flags_and_off):
  part1 = flags_and_off[0]
  part2 = flags_and_off[1]
  bin1 = bin(int(part1))
  bin2 = bin(int(part2))
  if len(bin1) < 6:
    bin1 = growBin(bin1, 6)
  if len(bin2) < 6:
    bin2 = growBin(bin2, 6)
  return (bin1,bin2)

def growBin(binary, size):
  # Function to expand the size of a binary number to a size "size"
  # It adds zeros to the beginning of the string
  bin_list = []
  for b in binary:
    bin_list.append(b)
  while len(bin_list) < size:
    # Insert a 0 in the Second position (after the 0b characters)
    bin_list.insert(2,0)
  return bin_list

def decode_ctrl_bits(ctrl):
  # Decodes the 6 bits in the TCP header for the Control flags
  # Flags are (in order): URG, ACK, PSH, RST, SYN and FIN
  ctrl_names = []
  if ctrl[0] == '1' :
    ctrl_names.append('URG')
  if ctrl[1] == '1' :
    ctrl_names.append('ACK')
  if ctrl[2] == '1' :
    ctrl_names.append('PSH')
  if ctrl[3] == '1' : 
    ctrl_names.append('RST')
  if ctrl[4] == '1' :
    ctrl_names.append('SYN')
  if ctrl[5] == '1' :
    ctrl_names.append('FIN')
  return ctrl_names

def main():
  start_sniffer()

if __name__ == '__main__':
  main()
