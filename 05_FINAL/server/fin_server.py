# 서버통합: id는 내장함수이므로 uid로 수정하기
# 최종 -> 0701.py
# 계속 수정하는 파이썬코드
#### 사용자별 폴더추가 ####

import pymysql
import socketserver
import glob
import os
import tempfile
import sys
from os import listdir  # SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장
from os.path import isfile, join  # SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장

# import modify # modify.py import함

HOST = ''
BUFSIZE = 1048576
PORT = 9300  # 9330
suc = 's'
fail = 'f'
# /home/ec2-user/Ourchord/USER 에서 사용자 이름(id)만 구분하고 mid랑 pdf같이 저장하기
SPDF_DIR = ''

connect = pymysql.connect(host="localhost",
                              port=3306,
                              user="사용자이름",
                              password="비번",
                              db="DB이름")
# aws rds 에서 cursor(쿼리문에 의해서 반환되는 결과값을 저장하는 메모리 공간)얻기
# cursor = connect.cursor(pymysql.cursors.DictCursor)
cursor = connect.cursor()


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('connect')
        # ---------------------화면 바뀔때마다 MyTcpHandler실행---------------------
        # 화면 구분할 배열 선언: android에서 string으로 보내는걸 배열로 받아야함
        ##############1.화면 구분##############
        # display변수에 string으로 받기
        display = self.request.recv(2048)
        display = display.decode()

        display1 = self.request.recv(2048)
        display1 = display1.decode()

        alldis = display + display1

        ##############2.alldis값 배열에 저장##############
        print("배열 저장 전 alldis: ", alldis)
        tdata = alldis.split("-")  # 문자열 '스페이스'로 구분하여 리스트에 저장
        print("배열 저장 후 alldis: ", tdata)  # t(otal)data

        global impdata  # 로그인 성공한 id값 저장

        # ---------------------화면별 받은 정보 저장 이후 ---------------------
        ##############3.로그인 화면(login)##############
        # ex) "login, id, pwd"
        # !!!!!id 정보는 계속 가지고 가야함 -> 사용자 정보 수정/ pdf / mid 파일 제공 시 필요!!!!!
        if (tdata[0] == 'login'):
            print("##로그인 정보를 확인 합니다.##\n\n")
            loginDB(tdata[1], tdata[2], self)

        ##############4-1.회원가입:id 중복확인(checkid)##############
        # ex) "id_check, id"
        if (tdata[0] == 'id_check'):
            print("##id 중복확인을 시작합니다.##\n\n")
            checkidDB(tdata[1], self)

        ##############4-2. 회원가입:인증코드 버튼(Auth)##############
        # ex) "Auth, username, id, pwd, email, Auth(발급받은 인증코드)"
        if (tdata[0] == 'Auth'):
            print("##인증코드 버튼에서 회원가입 내용 저장을 시작합니다.##\n\n")
            # tdata 배열 데이터 그대로 auth_tdata 배열에 저장
            # -> '회원가입 완료'할때까지 DB에 접근하지 않기 위함
            global auth_tdata
            auth_tdata = tdata

            # 여기서는 따로 앱에 return 해주지 않아도 될듯
            # 인증코드 저장은 '회원가입 버튼'에서 하는게 좋지 않을까 생각
            # AuthDB(tdata[1], tdata[2], tdata[3], tdata[4], tdata[5])

        ##############4-3. 회원가입:확인 버튼(checkAuth)##############
        # ex) "checkAuth, (사용자가 입력한 인증코드)checkAuth"
        if (tdata[0] == 'checkAuth'):
            print("##인증코드 확인을 시작합니다.##\n\n")
            # checkAuthDB(auth_tdata[2], tdata[1])
            if (auth_tdata[5] == tdata[1]):  # 발급받은 인증번호 == 사용자가 입력한 인증번호
                print(impdata, "인증 성공")
                # return runServer.checkauth(suc)
                self.request.send(b's')
            else:
                print(impdata, "인증 실패")
                # return runServer.checkauth(fail)
                self.request.send(b'f')

        ##############4-4.회원가입 내용 저장 화면(register)##############
        # ex) "register"
        if (tdata[0] == 'register'):
            print("##회원가입 내용 저장을 시작합니다.##\n\n")
            registerDB(auth_tdata[1], auth_tdata[2], auth_tdata[3], auth_tdata[4], auth_tdata[5])

        ##############5.서버로 pdf 파일 받아서 저장(upload_folder)##############
        # ex) "upload_folder-pdf이름"
        if (tdata[0] == 'upload_folder'):
            print("##앱에 저장 된 pdf 파일을 서버에 저장합니다.##\n\n")
            # pfile_name = self.request.recv(2048)  # pdf 이름 저장
            global pfile_name
            pfile_name = tdata[1]  # pdf 이름 저장

            pfile_size = int.from_bytes(self.request.recv(4096), byteorder='big')

            if pfile_size == 0:
                print("안드에'" + pfile_name + "' 없음")
                self.request.send(b'f')
                # return fail

            print("file name : " + pfile_name)
            print("size: %d" % pfile_size)
            print("\n(다운로드 시작)...")
            self.request.recv(bytes[255])

            nowdown_size = 0  # 다운로드 된 size

            # pfile_name(ex)12.pdf) 저장할 디렉토리 경로 생성 -> 디렉토리 내 모든 pdf 파일을 불러올 때 사용하기 위함
            global pdir
            pdir = SPDF_DIR + impdata + "/"
            # pdf 폴더까지의 경로
            apdir = pdir + pfile_name
            try:
                # 디렉토리 없으면 생성
                if not os.path.exists(pdir):  # 디렉토리 생성 o
                    print("디렉토리 생성 후 해당 디렉토리 아래 PDF 파일을 저장합니다.")
                    os.makedirs(pdir)
                    # sys.stdout = open(apdir, 'w')
                    f = open(apdir, 'w')
                    print('------여기부터 확인 해야댐------')
                    if nowdown_size < pfile_size:
                        resp = self.request.recv(min(BUFSIZE, pfile_size - nowdown_size))
                        nowdown_size += len(resp)
                        # f.write(os.chdir(apdir)) # 파일 쓰기 작업 경로 변경(os.chdir)
                        f.write(apdir)
                        print("Download %.2f%%" % min(100, nowdown_size / pfile_size * 100))
                        sys.stdout.flush()
                    else:
                        self.request.recv(1)
                        print("다운로드 성공!\n")

                # DB 에도 impdata에 해당하는 id를 통해서 파일 경로(pdf: dir) 저장해
                # USER_SCORE_PDF 테이블에 저장 (PDF_ID(ID), PDF_NAME, PDF_PATH)
                upload_folderDB(impdata, pfile_name, apdir)

                if os.path.isdir(pdir):  # 디렉토리 생성x
                    print("기존에 있는 디렉토리 이므로 해당 디렉토리 아래 PDF 파일을 저장합니다.")
                    f = open(apdir, 'w')
                    print('------여기부터 확인 해야댐------')
                    if nowdown_size < pfile_size:
                        resp = self.request.recv(min(BUFSIZE, pfile_size - nowdown_size))
                        nowdown_size += len(resp)
                        # f.write(os.chdir(apdir)) # 파일 쓰기 작업 경로 변경(os.chdir)
                        f.write(apdir)
                        print("Download %.2f%%" % min(100, nowdown_size / pfile_size * 100))
                        sys.stdout.flush()
                    else:
                        self.request.recv(1)
                        print("다운로드 성공!\n")

                # USER_SCORE_PDF 테이블에 저장
                upload_folderDB(impdata, pfile_name, apdir)

            except OSError:
                print('Error: create directory ' + apdir)

        ##############6. 조 변환##############
        # ex) 'conversion-(박자)-기존 조-변환 조-pdf 이름(pfile_name변수에 저장되어 있음)'
        if (tdata[0] == 'conversion'):
            # /home/ec2-user/Ourchord/modify.py는 코드 실행 후, 서버에 mid저장까지
            print("##조 변환과 미디 생성 알고리즘이 동작됩니다.##\n\n")

            # PDF 폴더를 업로드 하는 과정에서 ID에 해당하는 디렉토리는 생성된 상태임: pdir(ex)home/ec2-user/Ourchord/USER/flottante)
            # modify.py로 전송: pdir, 기존 조, 변환 조, pfile_name에서 확장자 제외한 파일이름

            # 확장자를 제외한 파일 이름 저장하기 ex)12.pdf
            # fn = list(pfile_name)

            rpfile_name = "".join(pfile_name[0])

            for i in range(1, len(pfile_name) - 4, 1):
                rpfile_name = rpfile_name + "".join(pfile_name[i])

            print("modify.py에 전달해줄 PDF 이름만 뽑았습니다.: ", rpfile_name)

            # modify.py에서 해당 정보를 받는곳에 return
            # mid로 변환하는 cmid() 함수가 modify.py에 있다는 가정하에 전송함

            # modify.py로 전송: pdir, 박자, 기존 조, 변환 조, pfile_name에서 확장자 제외한 파일이름
            # modify.cmid(pdir, tdata[1], tdata[2], tdata[3], rpfile_name)

            # 박자 제외
            # modify.cmid(pdir, tdata[1], tdata[2], rpfile_name)

            # basemidi_name 만들기
            rpfile_name = str(rpfile_name)
            basemidi_name = ['Base', tdata[1], '_', rpfile_name, '.mid']
            basemidi_name = "".join(basemidi_name)
            print(basemidi_name)  # ex) 기존: A -> BA_12.mid

            # basemidi_path = pdir + basemidi_name or basemidi_path = pdir
            basemidi_path = pdir + basemidi_name

            # conversionmidi_name 만들기
            conversionmidi_name = ['Change', tdata[2], '_', rpfile_name, '.mid']
            conversionmidi_name = "".join(conversionmidi_name)
            print(conversionmidi_name)  # ex) 변경: B -> CB_12.mid

            conversionmidi_path = pdir + conversionmidi_name

            # MIDI_ID(impdata), BASEMIDI_NAME, BASEMIDI_PATH, CONVERSIONMIDI_NAME, CONVERSIONMIDI_PATH
            conversionDB(impdata, basemidi_name, basemidi_path, conversionmidi_name, conversionmidi_path, self)

        ##############7.서버에서 생성된 mid 파일 앱으로 전송(midiupload_folder)##############
        if (tdata[0] == 'midiupload_folder'):
            print("##생성된 mid 파일을 앱으로 전송합니다.##\n\n")

            # 테스트는 SPDF_DIR에 있는 12.mid/BB_12.mid/CB_result_6.mid 세개 구분해서 받아지는지

            # 변환 전/변환 후 화면 구분
            display = self.request.recv(2048)
            display = display.decode()
            print(display)

            mfile_list = glob.glob(SPDF_DIR)  # SPDF_DIR -> pdir로 바꾸기
            if len(mfile_list) != 1:
                print(SPDF_DIR + "파일이 없습니다.")

            else:
                # SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장
                # SPDF_DIR -> pdir로 바꾸기
                files = [f for f in listdir(SPDF_DIR) if isfile(join(SPDF_DIR, f))]
                print("모든 MIDI 파일리스트:", files)

                # 안드로이드에서 upload_tab 클릭시 - 기존 MIDI 파일 전송
                # 안드로이드에서 'B' 보내주기
                if (display == "B"):  # 변환 전
                    # ex) 기존: A -> BaseA_12.mid
                    files = [i for i in files if i.find('Base') != -1]

                    # mid파일 확장자 한번 더 files에서 뽑아내고 for문으로 전송
                    files = [i for i in files if i.find('.mid') != -1]
                    print("변환 전 MIDI 파일리스트:", files)

                    # 파일 사이즈
                    file_size = int.from_bytes(self.request.recv(BUFSIZE), byteorder="big")
                    file_fullpath = SPDF_DIR + files  # ex) USER/ 아래있는 MIDI 파일 경로 합친거 (/home/ec2-user/Ourchord/USER/12.mid)
                    # 'Base'문자열을 가진 '.mid'확장자파일만 전송
                    for i in files:
                        ########추가########
                        file_size = os.path.getsize(file_fullpath)
                        print("file size: %d bytes" % file_size)
                        # length=8:데이터길이
                        # byteorder="big": 바이트 순서 빅엔디안
                        self.request.sendall((file_size).to_bytes(length=8, byteorder="big"))

                        client_status = self.request.recv(1)
                        if client_status == bytes([255]):
                            print(files + " 전송시작")
                            with open(file_fullpath, "rb") as f:
                                self.request.sendfile(f)
                            self.request.sendall(bytes([255]))
                            print(files + " 전송완료")
                            print("성공했으니 바로 종료합니다.")
                            break
                        else:
                            print("Client's Rejection")

                # 안드로이드에서 midiupload_tab 클릭시 - 변환된 MIDI 파일 전송
                # 안드로이드에서 'C' 보내주기
                if (display == "C"):  # 변환 후
                    # ex) 변경: B -> ChangeB_12.mid
                    files = [i for i in files if i.find('Change') != -1]

                    files = [i for i in files if i.find('.mid') != -1]
                    print("변환 후 MIDI 파일리스트:", files)

                    # 'Change'문자열을 가진 '.mid'확장자파일만 전송
                    for i in files:
                        ########추가########
                        file_size = os.path.getsize(file_fullpath)
                        print("file size: %d bytes" % file_size)
                        # length=8:데이터길이
                        # byteorder="big": 바이트 순서 빅엔디안
                        self.request.sendall((file_size).to_bytes(length=8, byteorder="big"))

                        client_status = self.request.recv(1)
                        if client_status == bytes([255]):
                            print(files + " 전송시작")
                            with open(file_fullpath, "rb") as f:
                                self.request.sendfile(f)
                            self.request.sendall(bytes([255]))
                            print(files + " 전송완료")
                            print("성공했으니 바로 종료합니다.")
                            break
                        else:
                            print("Client's Rejection")

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
            myDB(impdata, tdata[1], tdata[2], tdata[3], self)


# *모든 return값은 sql문 실행 시, (sql실행유무가 아닌)데이터가 존재 하면!*
# -------------------------------login DB 연동-------------------------------#
# -> sql 성공 시, id값 impdata 저장
def loginDB(uid, pwd, self):
    print('loginDB 연동 완료')

    sql = "SELECT EXISTS(SELECT *FROM USER WHERE ID=%s AND PWD=%s)"
    res = cursor.execute(sql, (uid, pwd))
    result = cursor.fetchone()  # fetchone(): 모든 데이터를 한번에 가져옴
    row_count = result[0]

    if (row_count > 0):
        connect.commit()
        print('정보있음')  # 정보 있음도 sql 문을 실행하고 결과값이 있을때 출력함
        print("로그인 성공한 사용자 ID: ", uid)
        impdata = uid  # 로그인이 성공하였으므로 impdata 변수에 저장
        # return runServer.login(suc)
        self.request.send(b's')

    else:
        print('정보없음')
        # return runServer.login(fail)
        self.request.send(b'f')


# -------------------------------checkid DB 연동-------------------------------#
def checkidDB(uid, self):
    print('checkidDB 연동 완료')

    sql = "SELECT EXISTS(SELECT ID FROM USER WHERE ID=%s)"
    cursor.execute(sql, uid)
    result = cursor.fetchone()
    row_count = result[0]
    # print(row_count)

    if (row_count > 0):
        connect.commit()
        print('id 중복o')  # id 중복 o 도 sql문을 실행하고 결과값이 있을때 출력함
        # return runServer.checkid(fail)
        self.request.send(b'f')
    else:
        print('id 중복x')
        # return runServer.checkid(suc)
        self.request.send(b's')


# -------------------------------register DB 연동-------------------------------#
def registerDB(username, id, pwd, email, auth, self):
    print('registerDB 연동 완료')

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
        # return runServer.register(suc)
        self.request.send(b's')
    else:
        print('USER 데이터 삽입 실패')
        # return runServer.register(fail)
        self.request.send(b'f')


# -------------------------------upload_folder DB 연동-------------------------------#
def upload_folderDB(pdf_id, pdf_name, pdf_path, self):
    print('upload_folderDB 연동 완료')

    cursor.execute("SELECT * FROM USER_SCORE_PDF")
    before = cursor.rowcount
    print('before: ', before)

    sql = "SELECT EXISTS(SELECT *FROM USER_SCORE_PDF WHERE PDF_ID=%s AND PDF_NAME=%s AND PDF_PATH=%s)"
    cursor.execute(sql, (pdf_id, pdf_name, pdf_path))
    result = cursor.fetchone()  # fetchone(): 모든 데이터를 한번에 가져옴
    row_count = result[0]

    if (row_count > 0):  # 중복o
        print('기존에 있는 upload_folder 데이터 입니다.')
        # return runServer.upload_folder(fail)
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
            # return runServer.upload_folder(suc)
            self.request.send(b's')


# -------------------------------conversion DB 연동-------------------------------#
def conversionDB(impdata, basemidi_name, basemidi_path, conversionmidi_name, conversionmidi_path, self):
    print('conversionDB 연동 완료')

    cursor.execute("SELECT * FROM USER_SCORE_MIDI")
    before = cursor.rowcount
    print('before: ', before)

    sql = "SELECT EXISTS(SELECT *FROM USER_SCORE_MIDI WHERE MIDI_ID=%s AND BASEMIDI_NAME=%s AND CONVERSIONMIDI_NAME=%s)"
    cursor.execute(sql, (impdata, basemidi_name, conversionmidi_name))
    result = cursor.fetchone()  # fetchone(): 모든 데이터를 한번에 가져옴
    row_count = result[0]

    if (row_count > 0):  # 중복o
        print('기존에 있는 MIDI 데이터 입니다.')
        # return runServer.conversion(fail)
        self.request.send(b'f')

    else:
        sql = "INSERT INTO USER_SCORE_MIDI(MIDI_ID, BASEMIDI_NAME, BASEMIDI_PATH, CONVERSIONMIDI_NAME, CONVERSIONMIDI_PATH) values(%s, %s, %s, %s, %s)"
        cursor.execute(sql, (impdata, basemidi_name, basemidi_path, conversionmidi_name, conversionmidi_path))

        cursor.execute("SELECT * FROM USER_SCORE_MIDI")
        after = cursor.rowcount
        print("after: ", after)

        if (before < after):
            connect.commit()
            print('MIDI 정보 데이터 삽입 성공')
            # return runServer.conversion(suc)
            self.request.send(b's')


# -------------------------------find_id DB 연동-------------------------------#
def find_idDB(username, email, self):
    print('find_idDB 연동 완료')

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
        # return runServer.find_id(fail)
        self.request.send(b'f')


# -------------------------------find_pw DB 연동-------------------------------#
def find_pwdDB(id, email, self):
    print('find_pwdDB 연동 완료')

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
        # return runServer.find_pwd(fail)
        self.request.send(b'f')


# -------------------------------my DB 연동-------------------------------#
def myDB(uid, username, rid, email, self):
    print('myDB 연동 완료')
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
        # return runServer.my(suc)
        self.request.send(b's')

    else:
        print('USER 정보 수정실패')
        # return runServer.my(fail)
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

    # def login(result):  # 로그인 정보 확인여부 앱으로 보내기
    #     return server.sendall(result)
    #
    # def checkid(result):  # id 중복 정보 확인여부 앱으로 보내기
    #     return server.sendall(result)
    #
    # #def auth(result):  # 회원가입중인 사용자 데이터 삽입여부 앱으로 보내기
    # #    return server.sendall(result)
    #
    # def checkauth(result):  # 인증코드 일치여부 앱으로 보내기
    #     return server.sendall(result)
    #
    # def register(result):  # 새로운 회원정보 등록여부 앱으로 보내기
    #     return server.sendall(result)
    #
    # def upload_folder(result): # PDF 파일 정보 데이터 삽입여부 앱으로 보내기
    #     return server.sendall(result)
    #
    # def conversion(result): # MIDI 파일 정보 데이터 삽입여부 앱으로 보내기
    #     return server.sendall(result)
    #
    # def find_id(result): # 사용자 ID 정보 앱으로 보내기
    #     return server.sendall(result)
    #
    # def find_pwd(result): # 사용자 PWD 정보 앱으로 보내기
    #     return server.sendall(result)
    #
    # def my(result):  # 사용자 정보 수정 성공여부 앱으로 보내기
    #     return server.sendall(result)


runServer()
