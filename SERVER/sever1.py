import socketserver
from os.path import exists

HOST = ''
PORT = 9300
#//home//ec2-user//test//socket_test//test.txt
class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data_transferred = 0
        print('연결됨')
        filename = self.request.recv(1024)
        #print(filename)
        filename = filename.decode()
        #print(filename)
        
        if not exists('/home/ec2-user/Ourchord/PDF/'+filename):
            print('못찾음')
            return
        
        print('전송 시작')
        print('/home/ec2-user/Ourchord/PDF/',filename)
        with open('/Ourchord/PDF/'+filename, 'rb') as f:
            try:
                data = f.read(1024)
                while data:
                    data_transferred += self.request.send(data)
                    data=f.read(1024)

            except Exception as e:
                print(e)

            print('전송 완료')

def runServer():
    print('서버 시작')

    try:
        server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('파일 서버를 종료합니다')


runServer()