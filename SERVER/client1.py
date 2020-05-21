import socket

HOST = 'localhost'
PORT = 9300

def getFileFromServer(filename):
    data_transferred = 0

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT))
        sock.sendall(filename.encode())

        data = sock.recv(1024)
        print(data)
        if not data:
            print('파일 존재 x')
            return
        
        with open('C:/Users/USER/Desktop/ww/'+filename,'wb') as f:
            try:
                while data:
                    f.write(data)
                    data_transferred +=len(data)
                    data = sock.recv(1024)
                
            except Exception as e:
                print(e)
        
    print('파일 종료')

filename = input('다운 로드 받을 파일 :')
getFileFromServer(filename)
