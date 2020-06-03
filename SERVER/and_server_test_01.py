import socket
import time

host = '127.0.0.1'
port = 9300 # Arbitrary non-privileged port
 

server_sock = socket.socket(socket.AF_INET)
server_sock.bind((host, port))
server_sock.listen(1)

print("기다리는 중")
client_sock, addr = server_sock.accept()

print('Connected by', addr)

# 서버에서 "안드로이드에서 서버로 연결요청" 한번 받음
data = client_sock.recv(1024)
print(data.decode("utf-8"), len(data))

while(True):
    data2 = int(input("보낼 값 : "))
    #print(data2.encode())
    #client_sock.send(data)
    #client_sock.send(data2.to_bytes(4, byteorder='little'))
    i = 2

    # 값하나 보냄(사용자가 입력한 숫자)
    client_sock.send(data2.to_bytes(4, byteorder='little'))

    # 안드로이드에서 값 받으면 "하나받았습니다 : 숫자" 보낼 것 받음
    data = client_sock.recv(1024)
    print(data.decode("utf-8"), len(data))
    
    if(data2 == 99):
        break;

# 연결끊겠다는 표시 보냄
#i=99
#client_sock.send(i.to_bytes(4, byteorder='little'))
client_sock.close()
server_sock.close()