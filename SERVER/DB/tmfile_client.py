#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TypeError: can only concatenate str (not "bytes") to str 수정
import socket
import cv2
import numpy

HOST = ''
PORT = ''

def getFileFromServer(filefile):
    data_transferred = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(filefile.encode())

        filefile = sock.recv(1024)
        print(filefile)
        if not filefile:
            print('파일 존재 x')
            return

        #with open('C:/testFile/soundtest/' + filefile, 'wb') as f:
        with open('C:/testFile/soundtest/' + filefile, 'wb') as f:
            try:
                #data = f.read(10240)
                while data:
                    f.write(data)
                    #f.write(data.encode('utf-8').strip()+"\n")
                    data_transferred += len(data)
                    data = sock.recv(1024)


            except Exception as e:
                print(e)

    print('파일 종료')


#filename = input('다운 로드 받을 파일 :')
#filename = '12.mid'
#getFileFromServer('12.mid')
getFileFromServer('ok.txt')

