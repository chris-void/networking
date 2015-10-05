#!/usr/bin/env python

# Echo server program
import socket

HOST = '128.197.11.36'    # Symbolic name meaning the local host
PORT = 58909              # Arbitrary non-privileged port

# create a server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a port
serversocket.bind((HOST, PORT))
serversocket.listen(1) # ?

print "Server Started"

conn, addr = serversocket.accept()
print 'Connexcted by', addr

while 1:
    data = conn.recv(1024)
    if not data: break
    print "Data Received:", data
    conn.send(data)

conn.close()

# Connection Setup Phase

## msg format:
## <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n
msg1 = "'s' rtt <NUMBER OF PROBES> byte# <SERVER DELAY>\n" 
msg2 = "'s' tput"

# Measurement Phase

## msg format:
## <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n

# Connection Termination Phase

## msg format:
## <PROTOCOL PHASE>\n
