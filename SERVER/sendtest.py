# logindb
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import os
from os.path import exists
import numpy as np
import socketserver

HOST = ''
PORT = 9300


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):

        print('connect')

        id = self.request.recv(2048)
        #id = self.recv(2048)
        print("id : ", id)  # ID 잘 들어왔는지 확인
        id = id.decode()
        idstr=id.split('-')
        print(idstr)
        print(idstr[0])
        print(idstr[1])
        print(idstr[2])
        #result = 'aaa'
        #print("보내기 시작")
        #self.request.send(b'aaa')
        #result.encode()

# 서버실행
def runServer():
    print('서버시작')
    try:
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        print("반복")
        server.serve_forever()
    except KeyboardInterrupt:
        print('파일 서버를 종료합니다')

runServer()

