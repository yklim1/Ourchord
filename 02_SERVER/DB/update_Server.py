# demo 서버 통합

import pymysql
import socketserver
import glob
import os
import sys
from os import listdir  # SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장
from os.path import isfile, join  # SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장
import time
import struct
import cob

HOST = ''
BUFSIZE = 1048576
PORT = 9300  # 9330
# /home/ec2-user/Ourchord/USER 에서 사용자 이름(id)만 구분하고 mid랑 pdf같이 저장하기
SPDF_DIR = '/home/ec2-user/Ourchord/USER/'

connect = pymysql.connect(host="ourchord.cwowchilkfpb.ap-northeast-2.rds.amazonaws.com",
                          port=3306,
                          user="ourchord",
                          password="IjDwDjKtU1-A",
                          db="OURCHORD")
# aws rds 에서 cursor(쿼리문에 의해서 반환되는 결과값을 저장하는 메모리 공간)얻기
# cursor = connect.cursor(pymysql.cursors.DictCursor)
cursor = connect.cursor()


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('connect')
        # ---------------------화면 바뀔때마다 MyTcpHandler실행---------------------
        # 화면 구분할 배열 선언: android에서 string으로 보내는걸 배열로 받아야함
        ##############1.화면 구분을 위함##############
        checkpoint = "+"
        alldis = ""
        while (1):
            # print("시작")
            display = self.request.recv(4096)
            # print("display 값 :".display)
            if (display != 0):
                print("display값: ", display)
                display = display.decode()
                if (display.find(checkpoint) == -1):
                    alldis = alldis + display
                else:
                    test = display.split(checkpoint)
                    alldis = alldis + test[0]
                    break

        ##############2.alldis값 배열에 저장##############
        print("배열 저장 전 alldis: ", alldis)
        tdata = alldis.split("-")  # 문자열 '스페이스'로 구분하여 리스트에 저장
        print("배열 저장 후 alldis: ", tdata)  # t(otal)data

        global impdata  # 로그인 성공한 id값 저장

        ##############3.로그인 화면(Login)##############
        class Login:
            def login(self):
                print("##로그인 정보를 확인 합니다.##\n\n")
                impdata = tdata[1]  # impdata에 id값 저장
                loginDB(tdata[1], tdata[2], self)

        ##############4.회원가입 화면(Auth)##############
        class Auth:
            def id_check(self): #4-1.회원가입:id 중복확인(checkid)
                print("##id 중복확인을 시작합니다.##\n\n")
                checkidDB(tdata[1], self)

            def Auth(self): #4-2. 회원가입:인증코드 버튼(Auth)
                print("##인증코드 버튼에서 회원가입 내용 저장을 시작합니다.##\n\n")
                # '회원가입 완료'할때까지 DB에 접근하지 않기 위함
                global auth_tdata # global: line81
                auth_tdata = tdata

            def checkAuth(self): #4-3. 회원가입:확인 버튼(checkAuth)
                print("##인증코드 확인을 시작합니다.##\n\n")
                # checkAuthDB(auth_tdata[2], tdata[1])
                # 발급받은 인증번호(Auth 함수 실행시 auth_tdata 리스트에 저장) == 사용자가 입력한 인증번호
                if (auth_tdata[5] == tdata[1]):
                    print(impdata, "인증 성공")
                    self.request.send(b's')
                else:
                    print(impdata, "인증 실패")
                    self.request.send(b'f')

            def register(self): #4-4.회원가입 내용 저장 화면(register)
                print("##회원가입 내용 저장을 시작합니다.##\n\n")
                registerDB(auth_tdata[1], auth_tdata[2], auth_tdata[3], auth_tdata[4], auth_tdata[5])

        class Folder:
            def upload_folder(self): #5.서버로 pdf 파일 저장(upload_folder)
                print("##앱에 저장 된 pdf 파일을 서버에 저장합니다.##\n\n")

                # time.sleep(1)
                print("test 시작")
                # p_dir = "/home/ec2-user/Ourchord/USER/"+impdata+"/"  # 미디 생성할 pdf 경로 저장
                p_dir = "/home/ec2-user/Ourchord/USER/zjisuoo/"  # 미디 생성할 pdf 경로 저장
                files = [f for f in listdir(p_dir) if isfile(join(p_dir, f))]
                print("모든 PDF 파일리스트:", files)

                # pdf파일 확장자 한번 더 files에서 뽑아내고 for문으로 전송
                files = [i for i in files if i.find('.pdf') != -1]
                print("모든 PDF 파일리스트:", files)
                p_files = "-".join(files)

                testlen = len(p_files)
                print("pdf 파일 리스트 길이", testlen)

                ttt = struct.pack('b', testlen)
                # testnum = testlen.encode()
                self.request.send(ttt)

                # time.sleep(1)

                testdata = p_files.encode()
                self.request.send(testdata)
                print("리스트 보내기 종료")

            def pName(self):
                pName = ""  # 기존 파일 이름: pfile_name = tdata[1] -> pName
                while (1):
                    # print("line148 시작")
                    display = self.request.recv(4096)
                    # print("display 값 :".display)
                    if (display != 0):
                        print(display)
                        display = display.decode()
                        if (display.find(checkpoint) == -1):
                            pName = pName + display
                        else:
                            test = display.split(checkpoint)
                            pName = pName + test[0]
                            break
                    else:
                        print("나감")
                        break
                print(pName)
                # pName = tdata[1]

                # pfile_name = self.request.recv(2048)  # pdf 이름 저장
                global pfile_name
                # pfile_name = tdata[1]  # pdf 이름 저장
                pfile_name = pName

                print("\n(다운로드 시작)...")

                global pdir
                # pdir = SPDF_DIR + impdata + "/"
                pdir = SPDF_DIR + "zjisuoo/"
                # pdf 폴더까지의 경로
                apdir = pdir + pfile_name
                try:
                    # 디렉토리 없으면 생성
                    print("디렉토리 진행 시작 : ")
                    if not os.path.exists(pdir):  # 디렉토리 생성 o
                        print("디렉토리 생성 후 해당 디렉토리 아래 PDF 파일을 저장합니다.")
                        os.makedirs(pdir)
                        # sys.stdout = open(apdir, 'w')
                        f = open(apdir, 'wb')
                        print('------여기부터 확인 해야댐------')

                        while (1):
                            resp = self.request.recv(4096)
                            if (resp != 0):
                                # f.write(resp)
                                print("쓰는중")
                                # print(resp)
                                a = len(resp)
                                if (resp[a - 1] == 43):
                                    print("if종료")
                                    aa = resp[0:a - 1]
                                    f.write(aa)
                                    f.close()
                                    print("종료")
                                    break
                                else:
                                    print("쓰기")
                                    f.write(resp)
                            else:
                                print("종료")
                                f.close()
                                break

                        sys.stdout.flush()

                    if os.path.isdir(pdir):  # 디렉토리 생성x
                        print("기존에 있는 디렉토리 이므로 해당 디렉토리 아래 PDF 파일을 저장합니다.")
                        f = open(apdir, 'wb')
                        while (1):
                            resp = self.request.recv(4096)
                            if (resp != 0):
                                # f.write(resp)
                                print("쓰는중")
                                # print(resp)
                                a = len(resp)
                                if (resp[a - 1] == 43):  # '+'
                                    print("if종료")
                                    aa = resp[0:a - 1]
                                    f.write(aa)
                                    f.close()
                                    print("종료")
                                    break
                                else:
                                    print("쓰기")
                                    f.write(resp)
                            else:
                                print("종료")
                                f.close()
                                break
                except OSError:
                    print('Error: create directory ' + apdir)

            def conversion(self): #6. 조 변환
                # /home/ec2-user/Ourchord/modify.py는 코드 실행 후, 서버에 mid저장까지
                print("##조 변환과 미디 생성 알고리즘이 동작됩니다.##\n\n")

                # mid 앱으로 보내기
                p = SPDF_DIR + "zjisuoo/" + tdata[3]

                pdfname = tdata[3].split(".pdf")

                print("PDF 이름만 뽑았습니다.: ", pdfname[0])

                #base_p = SPDF_DIR + impdata +"/" + "Base" + tdata[1] + "_" + pdfname[0] + ".mid"
                base_p = SPDF_DIR + "zjisuoo/" + "Base" + tdata[1] + "_" + pdfname[0] + ".mid"
                print("변환전 midi 경로:", base_p)

                # base_p = SPDF_DIR + impdata +"/" + "Change" + tdata[2] + "_" + pdfname[0] + ".mid"
                change_p = SPDF_DIR + "zjisuoo/" + "Change" + tdata[2] + "_" + pdfname[0] + ".mid"
                print("변환된 midi 경로:", change_p)

                # cob 로 전송 -> pdf경로를 보냄
                cob.midiMain(p, tdata[1], tdata[2])

                print("Base MIDI 파일을 앱으로 보냅니다.")

            def midiupload_folder(self): #7.서버에서 생성된 mid 파일 리스트와 파일을 앱으로 전송(midiupload_folder)
                print("##생성된 mid 파일을 앱으로 전송합니다.##\n\n")

                # time.sleep(1)
                print("test 시작")
                p_dir = "/home/ec2-user/Ourchord/USER/zjisuoo/"  # 미디 생성할 pdf 경로 저장
                files = [f for f in listdir(p_dir) if isfile(join(p_dir, f))]
                print("모든 파일리스트:", files)

                # mid파일 확장자 한번 더 files에서 뽑아내고 for문으로 전송
                files = [i for i in files if i.find('.mid') != -1]
                print("모든 MIDI 파일리스트:", files)
                p_files = "-".join(files)

                testlen = len(p_files)
                print("mid 파일 리스트 길이", testlen)

                ttt = struct.pack('b', testlen)
                # testnum = testlen.encode()
                self.request.send(ttt)

                # time.sleep(1)

                testdata = p_files.encode()
                self.request.send(testdata)
                print("리스트 보내기 종료")

        class Find:
            def find_id(self): #8.ID 찾기 화면(find_id)
                print("##id를 찾습니다.##\n\n")
                find_idDB(tdata[1], tdata[2], self)

            def find_pwd(self): #9.PWD 찾기 화면(find_pw)
                print("##pwd를 찾습니다.##\n\n")
                find_pwdDB()(tdata[1], tdata[2], self)

            def my(self): #10.개인정보 수정화면(my)
                print("## " + impdata + " 의 개인정보를 수정합니다.##\n\n")
                myDB(impdata, tdata[1], tdata[2], tdata[3], self)

        login = Login()
        auth = Auth()
        folder = Folder()
        find = Find()

        dict_math_display = {
            'login' : login.login,
            'id_check' : auth.id_check,
            'Auth' : auth.Auth,
            'checkAuth' : auth.checkAuth,
            'register' : auth.register,
            'upload_folder' : folder.upload_folder,
            'pName' : folder.pName,
            'conversion' : folder.conversion,
            'midiupload_folder' : folder.midiupload_folder,
            'find_id' : find.find_id,
            'find_pwd' : find.find_pwd,
            'my' : find.my
        }

        dict_math_display[tdata[0]]() #화면별 함수

# -------------------------------login DB 연동-------------------------------#
# -> sql 성공 시, id값 impdata 저장
def loginDB(uid, pwd, self):
    print('------loginDB 연동 완료------')

    sql = "SELECT EXISTS(SELECT *FROM USER WHERE ID=%s AND PWD=%s)"
    res = cursor.execute(sql, (uid, pwd))
    result = cursor.fetchone()  # fetchone(): 모든 데이터를 한번에 가져옴
    row_count = result[0]

    if (row_count > 0):
        connect.commit()
        print('정보있음')  # 정보 있음도 sql 문을 실행하고 결과값이 있을때 출력함
        print("로그인 성공한 사용자 ID: ", uid)
        impdata = uid  # 로그인이 성공하였으므로 impdata 변수에 저장
        self.request.send(b's')

    else:
        print('정보없음')
        self.request.send(b'f')

# -------------------------------checkid DB 연동-------------------------------#
def checkidDB(uid, self):
    print('------checkidDB 연동 완료------')

    sql = "SELECT EXISTS(SELECT ID FROM USER WHERE ID=%s)"
    cursor.execute(sql, uid)
    result = cursor.fetchone()
    row_count = result[0]
    # print(row_count)

    if (row_count > 0):
        connect.commit()
        print('id 중복o')  # id 중복 o 도 sql문을 실행하고 결과값이 있을때 출력함
        self.request.send(b'f')
    else:
        print('id 중복x')
        self.request.send(b's')

# -------------------------------register DB 연동-------------------------------#
def registerDB(username, id, pwd, email, auth, self):
    print('------registerDB 연동 완료------')

    cursor.execute("SELECT * FROM USER")
    before = cursor.rowcount
    print('before: ', before)

    sql = "INSERT INTO USER(USERNAME, ID, PWD, EMAIL, AUTH) values(%s, %s, %s, %s, %s)"
    cursor.execute(sql, (username, id, pwd, email, auth))

    cursor.execute("SELECT * FROM USER")
    after = cursor.rowcount
    print("after: ", after)

    if (before < after):
        connect.commit()
        print('USER 데이터 삽입 성공')
        self.request.send(b's')
    else:
        print('USER 데이터 삽입 실패')
        self.request.send(b'f')


# -------------------------------upload_folder DB 연동-------------------------------#
def upload_folderDB(pdf_id, pdf_name, pdf_path, self):
    print('------upload_folderDB 연동 완료------')

    cursor.execute("SELECT * FROM USER_SCORE_PDF")
    before = cursor.rowcount
    print('before: ', before)

    sql = "SELECT EXISTS(SELECT *FROM USER_SCORE_PDF WHERE PDF_ID=%s AND PDF_NAME=%s AND PDF_PATH=%s)"
    cursor.execute(sql, (pdf_id, pdf_name, pdf_path))
    result = cursor.fetchone()  # fetchone(): 모든 데이터를 한번에 가져옴
    row_count = result[0]

    if (row_count > 0):  # 중복o
        print('기존에 있는 upload_folder 데이터 입니다.')
        self.request.send(b'f')

    else:
        sql = "INSERT INTO USER_SCORE_PDF(PDF_ID, PDF_NAME, PDF_PATH) values(%s, %s, %s)"
        cursor.execute(sql, (pdf_id, pdf_name, pdf_path))

        cursor.execute("SELECT * FROM USER_SCORE_PDF")
        after = cursor.rowcount
        print("after: ", after)

        if (before < after):
            connect.commit()
            print('upload_folder 데이터 삽입 성공')
            self.request.send(b's')


# -------------------------------conversion DB 연동-------------------------------#
def conversionDB(impdata, basemidi_name, basemidi_path, conversionmidi_name, conversionmidi_path, self):
    print('------conversionDB 연동 완료------')

    cursor.execute("SELECT * FROM USER_SCORE_MIDI")
    before = cursor.rowcount
    print('before: ', before)

    sql = "SELECT EXISTS(SELECT *FROM USER_SCORE_MIDI WHERE MIDI_ID=%s AND BASEMIDI_NAME=%s AND CONVERSIONMIDI_NAME=%s)"
    cursor.execute(sql, (impdata, basemidi_name, conversionmidi_name))
    result = cursor.fetchone()  # fetchone(): 모든 데이터를 한번에 가져옴
    row_count = result[0]

    if (row_count > 0):  # 중복된 데이터는 삽입하지 않을꺼(try catch)
        print('기존에 있는 사용자: ' + impdata + 'MIDI 데이터 입니다.')
        # self.request.send(b'f')

    else:
        try:
            print('새로운 사용자: ' + impdata + ' MIDI 데이터를 삽입합니다.')
            sql = "INSERT INTO USER_SCORE_MIDI(MIDI_ID, BASEMIDI_NAME, BASEMIDI_PATH, CONVERSIONMIDI_NAME, CONVERSIONMIDI_PATH) values(%s, %s, %s, %s, %s)"
            cursor.execute(sql, (impdata, basemidi_name, basemidi_path, conversionmidi_name, conversionmidi_path))

            cursor.execute("SELECT * FROM USER_SCORE_MIDI")
            after = cursor.rowcount
            print("after: ", after)

            if (before < after):
                connect.commit()
                print('MIDI 정보 데이터 삽입 성공')
                self.request.send(b's')
        except:
            print('conversionDB query 문 실행 실패')

# -------------------------------find_id DB 연동-------------------------------#
def find_idDB(username, email, self):
    print('------find_idDB 연동 완료------')

    sql = "SELECT EXISTS(SELECT ID FROM USER WHERE USERNAME=%s AND EMAIL=%s)"
    cursor.execute(sql, (username, email))
    result = cursor.fetchone()
    row_count = result[0]
    # print(row_count)

    if (row_count > 0):
        connect.commit()
        sql = "SELECT ID FROM USER WHERE USERNAME=%s AND EMAIL=%s"
        cursor.execute(sql, (username, email))
        connect.commit()
        id = cursor.fetchall()
        print("전처리 전: ", id)

        # 전처리를 위한 문자열 배열로 저장
        id = "".join(id[0])
        print("전처리 후: ", id)

        print('ID 찾기 성공')
        # return runServer.find_id(id) # ID 정보만 보내줌
        #########################여기는 s/f가 아니라 id값 전송해야함#########################
        self.request.send(id)

    else:
        print('ID 찾기 실패')
        self.request.send(b'f')


# -------------------------------find_pw DB 연동-------------------------------#
def find_pwdDB(id, email, self):
    print('------find_pwdDB 연동 완료------')

    sql = "SELECT EXISTS(SELECT PWD FROM USER WHERE ID=%s AND EMAIL=%s)"
    cursor.execute(sql, (id, email))
    result = cursor.fetchone()
    row_count = result[0]
    # print(row_count)

    if (row_count > 0):
        connect.commit()
        sql = "SELECT PWD FROM USER WHERE ID=%s AND EMAIL=%s"
        cursor.execute(sql, (id, email))
        connect.commit()
        pwd = cursor.fetchall()
        print("전처리 전: ", pwd)

        # 전처리를 위한 문자열 배열로 저장
        pwd = "".join(pwd[0])
        print("전처리 후: ", pwd)

        print('PWD 찾기 성공')
        # return runServer.find_pwd(pwd)  # PWD 정보만 보내줌
        #########################여기는 s/f가 아니라 id값 전송해야함#########################
        self.request.send(pwd)

    else:
        print('PWD 찾기 실패')
        self.request.send(b'f')


# -------------------------------my DB 연동-------------------------------#
def myDB(uid, username, rid, email, self):
    print('------myDB 연동 완료------')
    # USER 테이블에서 id와 같은 id 찾고 해당 사용자 정보 수정하기

    sql = "SELECT EXISTS(SELECT *FROM USER WHERE ID=%s)"
    cursor.execute(sql, uid)
    result = cursor.fetchone()
    row_count = result[0]
    # print(row_count)

    if (row_count > 0):
        connect.commit()
        # connect.commit()
        print('##나의 정보를 수정합니다##')
        sql = "UPDATE USER SET USERNAME=%s, ID=%s, EMAIL=%s WHERE ID=%s"
        cursor.execute(sql, (username, rid, email, uid))
        connect.commit()
        print('USER 정보 수정성공')
        self.request.send(b's')

    else:
        print('USER 정보 수정실패')
        self.request.send(b'f')


# 서버연동
def runServer():
    print('서버시작')
    try:
        # 1. 사용자가 화면 실행할때마다 MyTcpHandler함수에서 배열 update
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()

    except KeyboardInterrupt:
        print('서버를 종료합니다')

runServer()
