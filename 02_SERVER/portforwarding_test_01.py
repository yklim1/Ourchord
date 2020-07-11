from socket import *

bufsize = 1024
targetHost = ""
listenPort = 1123

def forward(data, port) :
    print "Forwarding : '%s' from  %s" % (data, port)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("localhost", port))
    sock.sendto(data, (targetHost, listenPort))

def listen(host, port) :
    listenSocket = socket(AF_INET, SOCK_DGRAM)
    listenSocket.bind((host, port))

    while True :
        data, addr = listenSocket.recvfrom(bufsize)
        forward(data, addr[1])
    
listen("localhost", listenPort)