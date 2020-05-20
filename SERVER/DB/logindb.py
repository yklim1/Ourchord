# logindb
import pymysql
import os
from os.path import exists
import numpy as np
import socketserver

HOST = ''
PORT = 9300


# 연결- 받아올꺼
class MyTcpHandler(socketserver.BaseRequestHandler):
    '''def init_base(self,base):
        self.base = base
    def init_change(self,change):
        self.change = change'''

    def handle(self):
        global username
        global id
        global pwd
        global cpwd
        global email
        print('연결됨')

        # username = self.request.recv(2048)
        username = self.recv(2048)
        print("username : ", username)  # username 잘 들어왔는지 확인
        username = username.decode()

        # id = self.request.recv(2048)
        id = self.recv(2048)
        print("id : ", id)  # id 잘 들어왔는지 확인
        id = id.decode()

        # pwd = self.request.recv(2048)
        pwd = self.recv(2048)
        print("pwd : ", pwd)  # pwd 잘 들어왔는지 확인
        pwd = pwd.decode()

        # cpwd = self.request.recv(2048)
        cpwd = self.recv(2048)
        print("cpwd : ", cpwd)  # cpwd 잘 들어왔는지 확인
        cpwd = cpwd.decode()

        # email = self.request.recv(2048)
        email = self.recv(2048)
        print("email : ", email)  # email 잘 들어왔는지 확인
        email = email.decode()

        # DB에 데이터 전송
        loginDB(username, id, pwd, cpwd, email)


# 예외처리(빈칸이 있는지)는 안드에서
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


# mysql연동
def loginDB(username, id, pwd, cpwd, email):
    connect = pymysql.connect(host="localhost",
                              port=3306,
                              user="사용자이름",
                              password="비번",
                              db="DB이름")

    # aws rds에서 커서 cursor얻기
    # cursor: DB에서 sql문장 수행역할하기 위함
    cursor = connect.cursor()

    # 집어넣기
    # USER 테이블에 새로운 회원가입 정보삽입
    print("USER 테이블 삽입시작")
    # sql = "INSERT INTO USER(USERNAME, ID, PWD, CPWD, EMAIL) values(%s %s %s %s %s)"
    cursor.execute("INSERT INTO USER(USERNAME, ID, PWD, CPWD, EMAIL) values(username, id, pwd, cpwd, email)")
    # cursor.commit()
    print("USER 테이블 삽입완료")
    print("--------------------------------------------")

    # USER 테이블 데이터 삽입 확인
    cursor.execute("SELECT *FROM USER")

    # result에 저장(데이터 패치)
    result = cursor.fetchall()
    print("USER 테이블 전체 조회")
    print(result)


runServer()
