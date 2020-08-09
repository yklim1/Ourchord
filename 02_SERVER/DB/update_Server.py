# demo 서버 통합
# eeexplanin.py 

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
#import multiprocessing
import threading

HOST = ''
BUFSIZE = 1048576
PORT =''
# /home/ec2-user/Ourchord/USER 에서 사용자 이름(id)만 구분하고 mid랑 pdf같이 저장하기
SPDF_DIR = '/home/ec2-user/Ourchord/USER/'

connect = pymysql.connect(host="",
                          port=,
                          user="",
                          password="",
                          db="")
# aws rds 에서 cursor(쿼리문에 의해서 반환되는 결과값을 저장하는 메모리 공간)얻기
# cursor = connect.cursor(pymysql.cursors.DictCursor)
cursor = connect.cursor()


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        #시작시간
        #start_time = time.time()
        print('connect')

        # 변수 모음
        # pName -> fileName
        # auth_tdata -> authData
        # impdata -> loginUserId
        # id -> userId :id 함수 있음
        class Variable:
            # p_dir -> userDir
            # f -> pdfContent
            # apdir -> pdfDir
            # pfile_name -> pdfName
            # test -> endRev
            # testdata  -> sendList
            # testlen -> midiFileLen
            # ttt -> sendMidi
            # p_files -> allMidiList
            allUserDir, userDir = None, None  # id별 디렉토리 경로
            pdfDir, pdfName, pdfContent, allPdfList = None, None, None, None  # 경로
            endRev = None
            sendList, midiFIleLen, sendMidi, allMidiList = None, None, None, None

        # ---------------------화면 바뀔때마다 MyTcpHandler실행---------------------
        # 화면 구분할 배열 선언: android에서 string으로 보내는걸 배열로 받아야함
        ##############1.화면 구분을 위함##############

        # pool
        #global pool # join, close
        #pool = multiprocessing.Pool(processes=2)

        checkpoint = "+"
        displayName = ""  # alldis -> displayName
        while (1):
            # print("시작")
            display = self.request.recv(4096)
            # print("display 값 :".display)
            if (display != 0):
                print("display값: ", display)
                display = display.decode()
                if (display.find(checkpoint) == -1):
                    displayName = displayName + display
                else:
                    Variable.endRev = display.split(checkpoint)  # test -> Variable.endRev
                    displayName = displayName + Variable.endRev[0]
                    break

        ##############2.displayName 배열에 저장##############
        print("배열 저장 전 displayName: ", displayName)
        tdata = displayName.split("-")  # 문자열 '스페이스'로 구분하여 리스트에 저장
        print("배열 저장 후 displayName: ", tdata)  # t(otal)data

        global loginUserId  # 로그인 성공한 id값 저장(impdata -> loginUserId)

        #pool.map()  # dict_math_display매핑 함수, 전달값
        ##############3.로그인 화면(Login)##############
        class Login:
            def login(self):
                print("##로그인 정보를 확인 합니다.##\n\n")
                loginUserId = tdata[1]  # loginUserId에 id값 저장
                loginDB(tdata[1], tdata[2], self)
                # print("로그인 화면 수행은 총 %s 초 걸렸습니다." % (time.time() - start_time))

        ##############4.회원가입 화면(Auth)##############
        class Auth:
            def id_check(self):  # 4-1.회원가입:id 중복확인(checkid)
                print("##id 중복확인을 시작합니다.##\n\n")
                checkidDB(tdata[1], self)
                # print("id 중복확인 수행은 총 %s 초 걸렸습니다." % (time.time() - start_time))

            def Auth(self):  # 4-2. 회원가입:인증코드 버튼(Auth)
                print("##인증코드 버튼에서 회원가입 내용 저장을 시작합니다.##\n\n")
                # '회원가입 완료'할때까지 DB에 접근하지 않기 위함
                global authData  # auth_tdata -> authData(회원가입 시, 입력한 정보 임시 저장 배열)
                authData = tdata

            def checkAuth(self):  # 4-3. 회원가입:확인 버튼(checkAuth)
                print("##인증코드 확인을 시작합니다.##\n\n")
                # checkAuthDB(authData[2], tdata[1])
                # 발급받은 인증번호(Auth 함수 실행시 authData 리스트에 저장) == 사용자가 입력한 인증번호
                if (authData[5] == tdata[1]):
                    print(loginUserId, "인증 성공")
                    self.request.send(b's')
                    # print("인증확인은 총 %s 초 걸렸습니다." % (time.time() - start_time))
                else:
                    print(loginUserId, "인증 실패")
                    self.request.send(b'f')
                    # print("인증확인은 총 %s 초 걸렸습니다." % (time.time() - start_time))

            def register(self):  # 4-4.회원가입 내용 저장 화면(register)
                print("##회원가입 내용 저장을 시작합니다.##\n\n")
                registerDB(authData[1], authData[2], authData[3], authData[4], authData[5])
                # print("회원가입 저장은 총 %s 초 걸렸습니다." % (time.time() - start_time))

        class Folder:
            def upload_folder(self):  # 5.서버로 pdf 파일 저장(upload_folder)
                print("##앱에 저장 된 pdf 파일을 서버에 저장합니다.##\n\n")

                # time.sleep(1)
                print("test 시작")
                # p_dir -> userDir
                # Variable.userDir = "/home/ec2-user/Ourchord/USER/"+impdata+"/"  # 미디 생성할 pdf 경로 저장
                Variable.userDir = "/home/ec2-user/Ourchord/USER/zjisuoo/"  # 미디 생성할 pdf 경로 저장
                files = [f for f in listdir(Variable.userDir) if isfile(join(Variable.userDir, f))]
                print("모든 PDF 파일리스트:", files)

                # pdf파일 확장자 한번 더 files에서 뽑아내고 for문으로 전송
                files = [i for i in files if i.find('.pdf') != -1]
                print("모든 PDF 파일리스트:", files)
                Variable.allMidiList = "-".join(files)  # p_files -> Variable.allMidiList

                Variable.midiFileLen = len(Variable.allMidiList)  # testlen -> Variable.midiFileLen
                print("pdf 파일 리스트 길이", Variable.midiFileLen)

                Variable.sendMidi = struct.pack('b', Variable.midiFileLen)
                # testnum = testlen.encode()
                self.request.send(Variable.sendMidi)

                # time.sleep(1)

                Variable.sendList = Variable.allMidiList.encode()  # testdata  -> Variable.sendList
                self.request.send(Variable.sendList)
                print("리스트 보내기 종료")

            def pName(self):
                # pName -> fileName
                fileName = ""  # 기존 파일 이름: pfile_name = tdata[1] -> pName
                while (1):
                    # print("line148 시작")
                    display = self.request.recv(4096)
                    # print("display 값 :".display)
                    if (display != 0):
                        print(display)
                        display = display.decode()
                        if (display.find(checkpoint) == -1):
                            fileName = fileName + display
                        else:
                            Variable.endRev = display.split(checkpoint)
                            fileName = fileName + Variable.endRev[0]
                            break
                    else:
                        print("나감")
                        break
                print(fileName)
                # fileName = tdata[1]

                # pfile_name = self.request.recv(2048)  # pdf 이름 저장
                # global pfile_name
                # pfile_name = tdata[1]  # pdf 이름 저장
                Variable.pdfName = fileName

                print("\n(다운로드 시작)...")

                global pdir
                # pdir = SPDF_DIR + impdata + "/"
                pdir = SPDF_DIR + "zjisuoo/"
                # pdf 폴더까지의 경로
                Variable.pdfDir = pdir + Variable.pdfName  # apdir -> pdfDir
                try:
                    # 디렉토리 없으면 생성
                    print("디렉토리 진행 시작 : ")
                    if not os.path.exists(pdir):  # 디렉토리 생성 o
                        print("디렉토리 생성 후 해당 디렉토리 아래 PDF 파일을 저장합니다.")
                        os.makedirs(pdir)
                        # sys.stdout = open(Variable.pdfDir, 'w')
                        Variable.pdfContent = open(Variable.pdfDir, 'wb')  # f -> Variable.pdfContent
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
                                    Variable.pdfContent.write(aa)
                                    Variable.pdfContent.close()
                                    print("종료")
                                    break
                                else:
                                    print("쓰기")
                                    Variable.pdfContent.write(resp)
                            else:
                                print("종료")
                                Variable.pdfContent.close()
                                break

                        sys.stdout.flush()

                    if os.path.isdir(pdir):  # 디렉토리 생성x
                        print("기존에 있는 디렉토리 이므로 해당 디렉토리 아래 PDF 파일을 저장합니다.")
                        Variable.pdfContent = open(Variable.pdfDir, 'wb')
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
                                    Variable.pdfContent.write(aa)
                                    Variable.pdfContent.close()
                                    print("종료")
                                    break
                                else:
                                    print("쓰기")
                                    Variable.pdfContent.write(resp)
                            else:
                                print("종료")
                                Variable.pdfContent.close()
                                break
                except OSError:
                    print('Error: create directory ' + Variable.pdfDir)

            def conversion(self):  # 6. 조 변환
                # /home/ec2-user/Ourchord/modify.py는 코드 실행 후, 서버에 mid저장까지
                print("##조 변환과 미디 생성 알고리즘이 동작됩니다.##\n\n")

                # mid 앱으로 보내기
                p = SPDF_DIR + "zjisuoo/" + tdata[3]

                pdfname = tdata[3].split(".pdf")

                print("PDF 이름만 뽑았습니다.: ", pdfname[0])

                # base_p = SPDF_DIR + impdata +"/" + "Base" + tdata[1] + "_" + pdfname[0] + ".mid"
                base_p = SPDF_DIR + "zjisuoo/" + "Base" + tdata[1] + "_" + pdfname[0] + ".mid"
                print("변환전 midi 경로:", base_p)

                # base_p = SPDF_DIR + impdata +"/" + "Change" + tdata[2] + "_" + pdfname[0] + ".mid"
                change_p = SPDF_DIR + "zjisuoo/" + "Change" + tdata[2] + "_" + pdfname[0] + ".mid"
                print("변환된 midi 경로:", change_p)

                # cob 로 전송 -> pdf경로를 보냄
                cob.midiMain(p, tdata[1], tdata[2])

                print("Base MIDI 파일을 앱으로 보냅니다.")

            def midiupload_folder(self):  # 7.서버에서 생성된 mid 파일 리스트와 파일을 앱으로 전송(midiupload_folder)
                print("##생성된 mid 파일을 앱으로 전송합니다.##\n\n")

                # time.sleep(1)
                print("test 시작")
                Variable.userDir = "/home/ec2-user/Ourchord/USER/zjisuoo/"  # 미디 생성할 pdf 경로 저장
                files = [f for f in listdir(Variable.userDir) if isfile(join(Variable.userDir, f))]
                print("모든 파일리스트:", files)

                # mid파일 확장자 한번 더 files에서 뽑아내고 for문으로 전송
                files = [i for i in files if i.find('.mid') != -1]
                print("모든 MIDI 파일리스트:", files)
                Variable.allMidiList = "-".join(files)

                Variable.midiFileLen = len(Variable.allMidiList)
                print("mid 파일 리스트 길이", Variable.midiFileLen)

                Variable.sendMidi = struct.pack('b', Variable.midiFileLen)  # ttt -> Variable.sendMidi
                # testnum = testlen.encode()
                self.request.send(Variable.sendMidi)

                # time.sleep(1)

                Variable.sendList = Variable.allMidiList.encode()
                self.request.send(Variable.sendList)
                print("리스트 보내기 종료")

        class Find:
            def find_id(self):  # 8.ID 찾기 화면(find_id)
                print("##id를 찾습니다.##\n\n")
                find_idDB(tdata[1], tdata[2], self)

            def find_pwd(self):  # 9.PWD 찾기 화면(find_pw)
                print("##pwd를 찾습니다.##\n\n")
                find_pwdDB()(tdata[1], tdata[2], self)

            def my(self):  # 10.개인정보 수정화면(my)
                print("## " + loginUserId + " 의 개인정보를 수정합니다.##\n\n")
                myDB(loginUserId, tdata[1], tdata[2], tdata[3], self)

        login = Login()
        auth = Auth()
        folder = Folder()
        find = Find()

        dis_login = threading.Thread(target=login.login)
        dis_id_check = threading.Thread(target=auth.id_check)
        dis_Auth = threading.Thread(target= auth.Auth)
        dis_chechAuth = threading.Thread(target=auth.checkAuth)
        dis_register = threading.Thread(target=auth.register)
        dis_upload_folder = threading.Thread(target=folder.upload_folder)
        dis_pName = threading.Thread(target=folder.pName)
        dis_conversion = threading.Thread(target=folder.conversion)
        dis_midiupload_folder = threading.Thread(target=folder.midiupload_folder)
        dis_find_id= threading.Thread(target=find.find_id)
        dis_find_pwd= threading.Thread(target=find.find_pwd)
        dis_my= threading.Thread(target=find.my)

        dict_math_display = { # 'NoneType' object is not callable--check하기
            'login': dis_login, # 'login' : login.login,
            'id_check': dis_id_check.start(), # 'id_check': auth.id_check,
            'Auth': dis_Auth.start(), # 'Auth': auth.Auth,
            'checkAuth': dis_chechAuth.start(), # 'checkAuth': auth.checkAuth,
            'register': dis_register.start(), # 'register': auth.register,
            'upload_folder': dis_upload_folder.start(), # 'upload_folder': folder.upload_folder,
            'pName': dis_pName.start(), # 'pName': folder.pName,
            'conversion': dis_conversion.start(), # 'conversion': folder.conversion,
            'midiupload_folder': dis_midiupload_folder.start(), # 'midiupload_folder': folder.midiupload_folder,
            'find_id': dis_find_id.start(), # 'find_id': find.find_id,
            'find_pwd': dis_find_pwd.start(), # 'find_pwd': find.find_pwd,
            'my': dis_my.start() # 'my': find.my
        }

        dict_math_display[tdata[0]]()  # 화면별 함수

# -------------------------------login DB 연동-------------------------------#
# -> sql 성공 시, id값 loginUserId 저장
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
        loginUserId = uid  # 로그인이 성공하였으므로 loginUserId 변수에 저장
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
def registerDB(username, userId, pwd, email, auth, self):
    print('------registerDB 연동 완료------')

    cursor.execute("SELECT * FROM USER")
    before = cursor.rowcount
    print('before: ', before)

    sql = "INSERT INTO USER(USERNAME, ID, PWD, EMAIL, AUTH) values(%s, %s, %s, %s, %s)"
    cursor.execute(sql, (username, userId, pwd, email, auth))

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
def conversionDB(loginUserId, basemidi_name, basemidi_path, conversionmidi_name, conversionmidi_path, self):
    print('------conversionDB 연동 완료------')

    cursor.execute("SELECT * FROM USER_SCORE_MIDI")
    before = cursor.rowcount
    print('before: ', before)

    sql = "SELECT EXISTS(SELECT *FROM USER_SCORE_MIDI WHERE MIDI_ID=%s AND BASEMIDI_NAME=%s AND CONVERSIONMIDI_NAME=%s)"
    cursor.execute(sql, (loginUserId, basemidi_name, conversionmidi_name))
    result = cursor.fetchone()  # fetchone(): 모든 데이터를 한번에 가져옴
    row_count = result[0]

    if (row_count > 0):  # 중복된 데이터는 삽입하지 않을꺼(try catch)
        print('기존에 있는 사용자: ' + loginUserId + 'MIDI 데이터 입니다.')
        # self.request.send(b'f')

    else:
        try:
            print('새로운 사용자: ' + loginUserId + ' MIDI 데이터를 삽입합니다.')
            sql = "INSERT INTO USER_SCORE_MIDI(MIDI_ID, BASEMIDI_NAME, BASEMIDI_PATH, CONVERSIONMIDI_NAME, CONVERSIONMIDI_PATH) values(%s, %s, %s, %s, %s)"
            cursor.execute(sql, (loginUserId, basemidi_name, basemidi_path, conversionmidi_name, conversionmidi_path))

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
        userId = cursor.fetchall()
        print("전처리 전: ", userId)

        # 전처리를 위한 문자열 배열로 저장
        userId = "".join(userId[0])
        print("전처리 후: ", userId)

        print('ID 찾기 성공')
        # return runServer.find_id(id) # ID 정보만 보내줌
        #########################여기는 s/f가 아니라 id값 전송해야함#########################
        self.request.send(userId)

    else:
        print('ID 찾기 실패')
        self.request.send(b'f')


# -------------------------------find_pw DB 연동-------------------------------#
def find_pwdDB(userId, email, self):
    print('------find_pwdDB 연동 완료------')

    sql = "SELECT EXISTS(SELECT PWD FROM USER WHERE ID=%s AND EMAIL=%s)"
    cursor.execute(sql, (userId, email))
    result = cursor.fetchone()
    row_count = result[0]
    # print(row_count)

    if (row_count > 0):
        connect.commit()
        sql = "SELECT PWD FROM USER WHERE ID=%s AND EMAIL=%s"
        cursor.execute(sql, (userId, email))
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
