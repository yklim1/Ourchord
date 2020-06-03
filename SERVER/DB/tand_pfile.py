import socket
import os
import sys

HOST = ''
BUFSIZE = 1048576
PORT = -
DIR = '/home/ec2-user/Ourchord/MIDI/14.mid'
filename = "14.mid"

ADDR = (HOST,PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#연결
print('연결대기')
sock.bind(ADDR)
sock.listen(5)
conn, addr = sock.accept()
print('연결완료', addr)

f = open(DIR, 'rb') 
data = f.read()
print(data)
sdata = conn.sendall(data)
print(sdata)
f.flush()
f.close()

print('전송성공')
conn.close()
