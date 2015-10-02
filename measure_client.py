#!/usr/bin/env python

import socket

HOST = '128.197.11.36'    # The remote host
PORT = 58909          # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send('Hello, world')
data = s.recv(1024)
s.close()

print 'Received From Server:', repr(data)


# Connection Setup Phase

## msg format:
## <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n


# Measurement Phase

## msg format:
## <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n

# Connection Termination Phase

## msg format:
## <PROTOCOL PHASE>\n
