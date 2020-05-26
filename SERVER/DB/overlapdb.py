# 깃 업로드용 중복확인 db
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
        global username
        print('연결됨')

        # username = self.request.recv(2048)
        username = self.recv(2048)
        print("username : ", username)  # username 잘 들어왔는지 확인
        username = username.decode()

        # DB에 데이터 전송
        loginDB(username)

# DB에서 겹치는 ID가 있는지 확인(ID가 PRIMARY KEY)

# 서버실행
def runServer():
    print('로그인 서버 시작')

    try:
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        # print("반복")
        server.serve_forever()
    except KeyboardInterrupt:
        print('파일 서버를 종료합니다')

    # suc = 2 fail = 3
    def overlapCheck(result): 
        if result == 2:
            return server.sendall('suc')


# mysql연동
def loginDB(username):
    fail = 3
    suc = 2
    connect = pymysql.connect(host="localhost",
                              port=3306,
                              user="사용자이름",
                              password="비번",
                              db="DB이름")

    # aws rds에서 커서 cursor얻기
    cursor = connect.cursor()

    # ID중복검사
    if (cursor.execute("SELECT * FROM USER WHERE ID=id")):
        # -->and
        return runServer.overlapCheck(suc) 

    else:
        # -->and
        return runServer.overlapCheck(fail)

runServer()
