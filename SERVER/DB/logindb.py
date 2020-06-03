# 깃 업로드용 로그인db
import pymysql
import os
from os.path import exists
import numpy as np
import socketserver

HOST = ''
PORT = ''


# 연결- 받아올꺼
class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('연결됨')

        id = self.request.recv(2048)
        print("id : ", id)  # ID 잘 들어왔는지 확인
        id = id.decode()

        pwd = self.request.recv(2048)
        print("pwd : ", pwd)  # pwd 잘 들어왔는지 확인
        pwd = pwd.decode()

        # DB에 데이터 전송
        loginDB(id, pwd)

# 서버실행
def runServer():
    print('로그인 서버 시작')
    try:
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        # print("반복")
        server.serve_forever()
    except KeyboardInterrupt:
        print('파일 서버를 종료합니다')

    # -->and: 로그인 정보에 부합하는지
    # suc = 2 fail = 3
    def idCheck(result):
        if result == 2:
            return server.sendall(result)
        else:
            return server.sendall('fail')

# mysql연동
def loginDB(id, pwd):
    suc = 2
    fail = 3
    connect = pymysql.connect(host="localhost",
                              port=3306,
                              user="사용자이름",
                              password="비번",
                              db="DB이름")

    # aws rds에서 커서 cursor얻기
    cursor = connect.cursor()

    # ID중복검사
    if (cursor.execute("SELECT * FROM USER WHERE ID=id AND PWD=pwd")):
        # -->and
        return runServer.idCheck(suc)

    else:
        # -->and
        return runServer.idCheck(fail)

runServer()
