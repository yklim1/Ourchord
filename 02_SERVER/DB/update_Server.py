# final demo 그대로

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
import multiprocessing

HOST = ''
BUFSIZE = 1048576
PORT =   # 9330
# /home/ec2-user/Ourchord/USER 에서 사용자 이름(id)만 구분하고 mid랑 pdf같이 저장하기
SPDF_DIR = ''
global auth_tdata
global impdata  # 로그인 성공한 id값 저장

connect = pymysql.connect(host="",
                          port=,
                          user="",
                          password="",
                          db="")
# aws rds 에서 cursor(쿼리문에 의해서 반환되는 결과값을 저장하는 메모리 공간)얻기
# cursor = connect.cursor(pymysql.cursors.DictCursor)
cursor = connect.cursor()



class MyTcpHandler(socketserver.BaseRequestHandler):
    def __init__(self, id, pwd):
        self.id = id
        self.pwd = pwd
    def handle(self):
        print('connect')
        # ---------------------화면 바뀔때마다 MyTcpHandler실행---------------------
        # 화면 구분할 배열 선언: android에서 string으로 보내는걸 배열로 받아야함
        ##############1.화면 구분##############
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
            # 튜닝음 재생할때 display 값: b'' 무한대출력

        ##############2.alldis값 배열에 저장##############
        print("배열 저장 전 alldis: ", alldis)
        tdata = alldis.split("-")  # 문자열 '스페이스'로 구분하여 리스트에 저장
        print("배열 저장 후 alldis: ", tdata)  # t(otal)data

        # global impdata  # 로그인 성공한 id값 저장

        # ---------------------화면별 받은 정보 저장 이후 ---------------------
        ##############3.로그인 화면(login)##############
        # ex) "login, id, pwd"
        # !!!!!id 정보는 계속 가지고 가야함 -> 사용자 정보 수정/ pdf / mid 파일 제공 시 필요!!!!!
        if (tdata[0] == 'login'):
            print("##로그인 정보를 확인 합니다.##\n\n")
            impdata = tdata[1]  # impdata에 id값 저장
            loginDB(tdata[1], tdata[2], self)

        ##############4-1.회원가입:id 중복확인(checkid)##############
        # ex) "id_check, id"
        if (tdata[0] == 'id_check'):
            print("##id 중복확인을 시작합니다.##\n\n")
            checkidDB(tdata[1], self)
            auth_tdata = tdata

        ##############4-4.회원가입 내용 저장 화면(register)##############
        # ex) "register"
        if (tdata[0] == 'register'):
            print("##회원가입 내용 저장을 시작합니다.##\n\n")
            registerDB(auth_tdata[1], auth_tdata[2], auth_tdata[3], auth_tdata[4], auth_tdata[5])

        ##############5.서버로 pdf 파일 저장(upload_folder)##############
        if (tdata[0] == 'upload_folder'):
            print("##앱에 저장 된 pdf 파일을 서버에 저장합니다.##\n\n")

            # time.sleep(1)
            print("test 시작")
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

            # 파일 이름 받기 --> t0해서 이름구분

        if (tdata[0] == 'pName'):
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
            # pfile_size = int.from_bytes(self.request.recv(4096), byteorder='big')

            # if pfile_size == 0:
            # print("안드에'" + pfile_name + "' 없음")
            # self.request.send(b'f')

            # print("file name : " + pfile_name)
            # print("size: %d" % pfile_size)
            print("\n(다운로드 시작)...")
            # self.request.recv(bytes[255])

            # nowdown_size = 0  # 다운로드 된 size

            # pfile_name(ex)12.pdf) 저장할 디렉토리 경로 생성 -> 디렉토리 내 모든 pdf 파일을 불러올 때 사용하기 위함
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
                    # if nowdown_size < pfile_size:
                    # resp = self.request.recv(min(BUFSIZE, pfile_size - nowdown_size))
                    # nowdown_size += len(resp)
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

                # DB 에도 impdata에 해당하는 id를 통해서 파일 경로(pdf: dir) 저장해
                # USER_SCORE_PDF 테이블에 저장 (PDF_ID(ID), PDF_NAME, PDF_PATH)
                # upload_folderDB(impdata, pfile_name, apdir)

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

        ############################6. 조 변환############################
        # ex) 'conversion-기존 조-변환 조-pdf 이름'
        if (tdata[0] == 'conversion'):
            # /home/ec2-user/Ourchord/modify.py는 코드 실행 후, 서버에 mid저장까지
            print("##조 변환과 미디 생성 알고리즘이 동작됩니다.##\n\n")

            # mid 앱으로 보내기
            p = SPDF_DIR + "zjisuoo/" + tdata[3]
            # tdata[3]은 pdf 이름 -> rpfile_name에 .pdf빼고 저장

            rpfile_name = ""
            # for i in range(0, len(pfile_name) - 4, 1):
            #    rpfile_name = rpfile_name + "".join(pfile_name[i])
            pdfname = tdata[3].split(".pdf")

            print("PDF 이름만 뽑았습니다.: ", pdfname[0])

            base_p = SPDF_DIR + "zjisuoo/" + "Base" + tdata[1] + "_" + pdfname[0] + ".mid"
            print("변환전 midi 경로:", base_p)

            change_p = SPDF_DIR + "zjisuoo/" + "Change" + tdata[2] + "_" + pdfname[0] + ".mid"
            print("변환된 midi 경로:", change_p)

            # cob 로 전송 -> pdf경로를 보냄
            cob.midiMain(p, tdata[1], tdata[2])

            print("Base MIDI 파일을 앱으로 보냅니다.")


        ##############7.서버에서 생성된 mid 파일 리스트와 파일을 앱으로 전송(midiupload_folder)##############
        # SPDF_DIR <-> pdir(/user id 까지) 로 바꾸기
        if (tdata[0] == 'midiupload_folder'):
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

            # midi안드로 보내기
            '''while True:
                try:
                    # 디렉토리 내 파일 유무 확인
                    print("try실행")
                    mfile_list = glob.glob(pdir) # pdir = SPDF_DIR + impdata + "/"
                    # conn = self.request()
                    print("file 읽기 종료")

                    if len(mfile_list) != 1:
                        print(pdir + "파일이 없습니다.")
                        self.request.sendall(bytes[0])
                    else:
                        # SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장
                        # SPDF_DIR -> pdir(SPDF_DIR + impdata)로 바꾸기
                        files = [f for f in listdir(pdir) if isfile(join(pdir, f))]
                        print("모든 MIDI 파일리스트:", files)

                        ########### 미디 리스트 전송(기존/변경 미디 모두 전송)
                        if (len(tdata) == 1):
                            files = [i for i in files if i.find('.mid') != -1]
                            print("변환 전 MIDI 파일리스트:", files)
                            file = "-".join(files)
                            # print("앱으로 보낼 정보 입니다: ", file)
                            # self.request.sendall(file.encode())  # 파일 리스트 안드로이드로 보내기
                            # print("조건에 부합하는 Change MIDI 파일리스트 전송 완료")

                            testlen = len(file)
                            print("pdf 파일 리스트 길이", testlen)

                            ttt = struct.pack('b', testlen)
                            # testnum = testlen.encode()
                            self.request.send(ttt)

                            time.sleep(1)

                            testdata = file.encode()
                            self.request.send(testdata)
                            print("리스트 보내기 종료")
                            #return file

                        ########### 지정 미디 파일 전송
                        else:
                            print("전송할 파일" + pdir)
                            print("##전송할 데이터##")
                            f = open(pdir, 'rb')
                            s = f.read()
                            print(s)

                            file_list = glob.glob(pdir)  # glob모듈의 glob()
                            if len(file_list) != 1:
                                print(pdir + " 파일없음")
                                self.request.sendall(bytes([0]))
                                continue
                            else:
                                file_size = os.path.getsize(pdir)
                                print("file size: %d bytes" % file_size)

                                # length=8:데이터길이
                                # byteorder="big": 바이트 순서 빅엔디안
                                self.request.sendall((file_size).to_bytes(length=8, byteorder="big"))

                            client_status = 'bytes([255])'
                            if client_status == 'bytes([255])':
                                print(pdir + " 전송시작")
                                with open(pdir, "rb") as f:
                                    self.request.sendfile(f)
                                self.request.sendall(bytes([255]))
                                print(pdir + " 전송완료")
                                print("성공했으니 바로 종료합니다.")
                                break

                except ConnectionError:
                    print("ConnectionError 발생")
                    break
                except OSError:
                    print("OSError 발생")
                    break
                except:
                    print("bad-requestError 발생")
                    break
                finally:
                    self.request.close()'''

            # # 현재 사용중인 사용자의 mid폴더(pdir)에 접근하여 모든 mid파일 보내기
            # mfile_list = glob.glob(pdir)
            # if len(mfile_list) != 1:
            #     print(pdir + "파일이 없습니다.")
            # else:
            #     # 방1) DB 접근 안하고 디렉토리 경로로 모든 MIDI 파일 전송
            #     file_list = glob.glob(pdir + '*.mid')
            #     i = 0
            #     for i in range(len(file_list)):
            #         print(i + 1, "번째", file_list[i])
            #         # rb(read-binary), rt(read-text), wb, wt
            #         sf = open(file_list[i], 'rb')
            #         data = sf.read()  # mid 파일
            #         print("전송 전 데이터: ", data)
            #         # 전송할 파일 size
            #         file_size = os.path.getsize(pdir)
            #         print("file_size: %d bytes" % file_size)
            #
            #         print(file_list[i] + " 전송시작")
            #         self.request.sendall(data)
            #         print(file_list[i] + " 전송완료")

        ##############8.ID 찾기 화면(find_id)##############
        # ex) "find_id, username, email"
        # 앱에서 이메일 보내는데 그 이메일에 담긴 id 내용은 서버에서 보내줘야하는거지
        if (tdata[0] == 'find_id'):
            print("##id를 찾습니다.##\n\n")

            find_idDB(tdata[1], tdata[2], self)

        ##############9.PWD 찾기 화면(find_pw)##############
        # ex) "find_pw, id, email"
        if (tdata[0] == 'find_pwd'):
            print("##pwd를 찾습니다.##\n\n")

            find_pwdDB()(tdata[1], tdata[2], self)

        ##############10.개인정보 수정화면(my)##############
        # ex) "my, username, id, email"
        if (tdata[0] == 'my'):
            print("##개인정보를 수정합니다.##\n\n")
            # 누구의 정보(impdata -> 현재 사용중인 사용자의 id)를
            # 어떻게 수정할지(tdata -> username, id, email)
            print(impdata)
            myDB(impdata, tdata[1], tdata[2], tdata[3], self)

# *모든 return값은 sql문 실행 시, (sql실행유무가 아닌)데이터가 존재 하면!*
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

#my = MyTcpHandler(socketserver.BaseRequestHandler) #https://wikidocs.net/1740
my = MyTcpHandler('zjisuoo', '1234') #https://wikidocs.net/1740

# 서버연동
def runServer():
    print('서버시작')
    try:
        # 1. 사용자가 화면 실행할때마다 MyTcpHandler함수에서 배열 update
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
        process = multiprocessing.Process(target=my.handle())
        process.start()
        process2 = multiprocessing.Process(target=my.handle())
        process2.start()

    except KeyboardInterrupt:
        print('서버를 종료합니다')

if __name__=="__main__":
    runServer()
