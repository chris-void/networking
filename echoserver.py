#!/usr/bin/env python


import socket
import sys

host = '128.197.11.36'
backlog = 5

from echoserver_worker import ServerWorker

class Server:	
    def main(self):
        port = 0
        try:
            port = int(sys.argv[1])
        except:
            print "Usage: Server.py Server_port"
            port = 58909
            print "Choose default port (", port, ")"


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        s.bind((host,port))
        s.listen(backlog)

        while True:
            clientInfo = {}
            (newSocket, clientAddress) = s.accept()
            clientInfo['socket'] = (newSocket, clientAddress)
            ServerWorker(clientInfo).run()		

if __name__ == "__main__":
    (Server()).main()


