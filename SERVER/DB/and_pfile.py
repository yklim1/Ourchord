#sand_pfile.py
import socket
import argparse
import glob
import os
import sys

HOST = ''
#BUFSIZE = 1048576
PORT = 
DIR = '/home/ec2-user/Ourchord/MIDI/14.mid'

def run_server(PORT, DIR):
    print("연결 대기중..")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #연결
        sock.bind((HOST, PORT))
        sock.listen(1)
        conn, addr = sock.accept()
        print('연결완료: ', addr)

        f = open(DIR, 'rb')
        data = f.read()
        print('보낼 데이터: ', data)
        s_data = conn.sendall(data)
        print('보낸 데이터: ', s_data)
        f.close()

    except:
        print("Error: bad request")

    print('전송성공 후 연결종료')
    conn.close()
run_server(PORT, DIR)
