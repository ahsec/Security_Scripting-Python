### Module 3

* CGI_Server.py

  Simple CGI server, uses the default CGIHTTPServer handler

* HTTPServer_example.py

  This example creates a simple HTTP Server that listens on port 10001.

* Raw_Socket.py

  Simple packet sniffer that capture a packet of the for 0x0800.

  Prints the Ethernet and IP headers and exits

  From the file

  "/usr/src/kernels/3.16.3-200.fc20.i686+PAE/include/uapi/linux/if_ether.h"
0x0800 is defined as:
  define ETH_P_IP        0x0800          /* Internet Protocol packet */

* Raw_Socket_Full.py

  Second version of the Simple packet sniffer (Raw_Socket.py) that capture a
packet of the form 0x0800 # IP packet
Prints the Ethernet and IP headers and exits.
This version adds information about the Ethernet, IP and TCP headers

  From the file
  /usr/src/kernels/3.16.3-200.fc20.i686+PAE/include/uapi/
  linux/if_ether.h" 0x0800 is defined as:  define ETH_P_IP        0x0800          /* Internet Protocol packet */

  For reference, [Size of data types in pyhton](https://docs.python.org/2/library/struct.html)

* Scapy_ARP_MiTM.py

  ARP Man In the middle tool.
This tool creates a MiTM by performing ARP spoofing.

* Scapy_DNS_Poison.py

  Demonstation of a DNS Poisoning attack.
The script captures a DNS request packet and replies to the requestor with
incorrect information, meaning:

 1. Sniff traffic to capture DNS requests
 2. Forge a response packet with some fake content in it
 3. Reply back with the forged response

  [Reference - Reliable DNS spoofing with Python](http://danmcinerney.org/reliable-dns-spoofing-with-python-scapy-nfqueue)

  Tested and verified using ettercap
ettercap --iface wlo2 -T -M arp:remote /192.168.1.1// /192.168.1.3//
Where 192.168.1.1 is the gateway and 192.168.1.3 is the victim

* Scapy_SYN_scan.py

  Simple SYN scanner using the scapy module.
This script will perform a SYN scan of the ports [21,22,23,80,443] for the
supplied IP_Address

  Sample output:
```
Received 7 packets, got 6 answers, remaining 0 packets
Port: 21 - TCP flags: 20
Port: 22 - TCP flags: 18
Port: 22 responded with flags: SA
Port: 23 - TCP flags: 20
Port: 80 - TCP flags: 18
Port: 80 responded with flags: SA
Port: 56 - TCP flags: 20
```
* Sniff_HTTP_scapy.py

  HTTP sniffer using Scapy.
Prints HTTP headers and data in GET/POST from captured packets

* Sniff_SSID_scapy.py

  A frequency sniffer that reads all the SSID beacons and prints the result.
Requires an interface in monitor mode (desirable to have is an interface
that can change frequencies)

* Sniffer_options.py

  Sniffer that receives arguments from the command line.
Based on the arguments it performs filtering.

* SocketServer_example.py

  SocketServer is an echo server. Receives data (a string) from a client and
replies back with the exact same string).
Makes use of the SocketServer library.
Only handles one connection at a time, so we will have to create another
multithreaded version of it

* SocketServer_threading.py

  The multithread version of SocketServer. Uses ThreadedTCPRequestHandler which
allows it to handle incoming connections through different threads.

* Spoof_ARP.py

  This code sends an ARP packet using the interface wlo2
The idea is to create spoof ARP packets and verify that this PoC works.

* TCP_echo_server_multiprocess.py

  Creates a "child" process from a "parent" process.
The chlid will process incoming connections, every time a connection is
created, the parent process will spawn a child (just like all parents do)

* TCP_echo_server.py

  Creates a listening socket.
Parameters that can be specified are, IP to listen to, Port, and number of
accepted connections.

* TCP_echo_server_threading.py

  Creates a thread and assigns tasks to that thread
In this case, this is a multithread echo server so it handles incoming
connections and replies back to incoming messages.
The socket definition and thread assignment happens in the main function.
