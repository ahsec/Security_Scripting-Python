### Module 5

* Sock_Client.py

  Standard socks client that will be used to exploit an Echo server.
Target IP address and port to connect to are configurable.

* spse2.py

  Initial Immunity Debuger script. Uses the immlib library to get PID, name, Path
and services associated to a process.

* spse3.py

  Uses the immunity Debugger immlib library to obtain a list of processes and
print their information to the screen

* spse4.py

  Uses the Immunity Debugger library immlib to attach to a process and obtain
the following information of the modules in that process:
 1. Name
 2. Base address
 3. Size
 4. Entry point
 5. Version
