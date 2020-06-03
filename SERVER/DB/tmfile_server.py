#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socketserver
from os.path import exists

HOST = ''
PORT = ''

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data_transferred = 0
        print('연결됨')
        filename = self.request.recv(1024).decode()
        #filename = '12.mid'
        print(filename)
        #filename = filename.decode()
        #print(filename)


        if not exists('/home/ec2-user/Ourchord/MIDI/' + filename):
        #if not exists(filename): #동일폴더
            print('못찾음')
            return

        print('전송 시작')
        print('/home/ec2-user/Ourchord/MIDI/', filename)
        with open('/home/ec2-user/Ourchord/MIDI/' + filename, 'rb') as f:
        #with open(filename, 'rb') as f: #동일폴더
            try:
                data = f.read(1024)
                while data:
                    data_transferred += self.request.send(data)
                    data = f.read(1024)

            except Exception as e:
                print(e)

            print('전송 완료')


def runServer():
    print('서버 시작')

    try:
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('파일 서버를 종료합니다')


runServer()
