#!/usr/bin/env python

import socket

HOST = '128.197.11.36'    # The remote host
PORT = 58909          # The same port as used by the server

##
# Connection Setup Phase
##
def connectionsetup(self, measure_type, msg_size):
    def __init__(self):
        PROTOCOL_PHASE = 's'
        MEASURE_TYPE = measure_type
        #PROBES
        MSG_SIZe = msg_size
        SERVER_DELAY = 0 # default

    # create a INET, STREAMing socket
    
    ##exception
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))      

    # connect established


s.send('Hello, world')
data = s.recv(1024)
s.close()

print 'Received From Server:', repr(data)


#
# <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n
#msg1 = "'s' rtt <NUMBER OF PROBES> byte# <SERVER DELAY>\n" 
#msg2 = "'s' tput"


# send probe msg to cal mean rtt and throughput
## 
# Measurement Phase
##
def measure(self):
    def __init__(self):
        PROTOCOL_PHASE = 'm'
    
## msg format:
## <PROTOCOL PHASE>< ><MEASUREMENT TYPE>< ><NUMBER OF PROBES>< ><MESSAGE SIZE>< ><SERVER DELAY>\n



##
# Connection Termination Phase
##
def connectionterminate(self):
    pass

## msg format:
## <PROTOCOL PHASE>\n
