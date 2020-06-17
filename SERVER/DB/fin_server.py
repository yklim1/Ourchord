# 서버통합
import pymysql
import socketserver
import glob
import os
import tempfile
import sys

HOST = ''
BUFSIZE = 1048576
PORT = 9300  # 9330
suc = 's'
fail = 'f'
SPDF_DIR = '/home/ec2-user/Ourchord/PDF/'

connect = pymysql.connect(host="localhost",
                              port=3306,
                              user="사용자이름",
                              password="비번",
                              db="DB이름")

# cursor = connect.cursor(pymysql.cursors.DictCursor)
cursor = connect.cursor()


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('connect')
        
        display = self.request.recv(2048)

        tdata = display.split()  
        global impdata 
        print(tdata)  

        # ---------------------화면별 받은 정보 저장 이후 ---------------------
        # 3.로그인 화면(login) ex) "login, id, pwd"
        
        if (tdata[0] == 'login'):
            print("##로그인 정보를 확인 합니다.##\n\n")
            impdata = tdata[1]  # id는 중복되지 않으므로 id만 저장
            loginDB(tdata[1], tdata[2])

        # 4-1.회원가입:id 중복확인(checkid) ex) "checkid, id"
        if (tdata[0] == 'checkid'):
            print("##id 중복확인을 시작합니다.##\n\n")
            checkidDB(tdata[1])

        # 4-2. 회원가입:인증코드 버튼(Auth) ex) "Auth, username, id, pwd, email"
        if (tdata[0] == 'Auth'):
            print("##인증코드 버튼에서 회원가입 내용 저장을 시작합니다.##\n\n")
            # '4-3.'확인을 위해 현재 회원가입 중인 사용자의 id global 변수에 저장
            global regid
            regid = tdata[2]
            # 인증코드 저장은 '확인 버튼'에서 하는게 좋지 않을까 생각
            AuthDB(tdata[1], tdata[2], tdata[3], tdata[4])

        # 4-3. 회원가입:확인 버튼(checkAuth) ex) "checkAuth, (이메일로 보내진 인증코드)Auth, (사용자가 입력한 인증코드)checkAuth"
        if (tdata[0] == 'checkAuth'):
            print("##인증코드 확인을 시작합니다.##\n\n")
            checkAuthDB(regid, tdata[1], tdata[2])

        
        # ex) "register, username, id, pwd, email"
        '''if(tdata[0] == 'register'):
            print("##회원가입 내용 저장을 시작합니다.##\n\n")
            registerDB(tdata[1], tdata[2], tdata[3], tdata[4])'''

        # 5.서버에서 앱에 저장된 pdf 파일 받아서 저장(upload_folder)##############
        if (tdata[0] == 'upload_folder'):
            # server_pdf.py에서 작업
            print('------확인 해야댐------')
            print("##앱에 저장 된 pdf 파일을 서버에 저장합니다.##\n\n")
            pfile_name = self.request.recv(2048)  # pdf 이름 저장

            pfile_size = int.from_bytes(self.request.recv(4096), byteorder='big')

            if pfile_size == 0:
                print("안드에'" + pfile_name + "' 없음")
                return fail

            print("file name : " + pfile_name)
            print("size: %d" % pfile_size)
            print("\n(다운로드 시작)...")
            self.request.recv(bytes[255])

            nowdown_size = 0  # 다운로드 된 size

            with tempfile.NamedTemporaryFile(delete=False, dir=".") as f:
                temp_name = f.name
                while True:
                    if nowdown_size < pfile_size:
                        resp = self.request.recv(min(BUFSIZE, pfile_size - nowdown_size))
                        nowdown_size += len(resp)
                        # f.write(resp)
                        f.write(os.chdir(SPDF_DIR + pfile_name))
                        print("Download %.2f%%" % min(100, nowdown_size / pfile_size * 100))
                        sys.stdout.flush()
                    else:
                        self.request.recv(1)
                        print("다운로드 성공!\n")
                        break
            os.replace(temp_name, pfile_name)

        
        if (tdata[0] == 'conversion'):
            
            print("##조 변환과 미디 생성 알고리즘이 동작됩니다.##\n\n")
            import conversion

        
        if (tdata[0] == 'midiupload_folder'):
            print("##생성된 mid 파일을 앱으로 전송합니다.##\n\n")
            MID_DIR = '/home/ec2-user/Ourchord/MIDI/'
            
            mfile_list = glob.glob(MID_DIR)
            if len(mfile_list) != 1:
                print(MID_DIR + "파일이 없습니다.")
            else:
                file_list = glob.glob(MID_DIR + '*.mid')
                i = 0
                for i in range(len(file_list)):
                    print(i + 1, "번째", file_list[i])
                    # rb(read-binary), rt(read-text), wb, wt
                    sf = open(file_list[i], 'rb')
                    data = sf.read()  # mid 파일
                    print("전송 전 데이터: ", data)
                    # 전송할 파일 size
                    file_size = os.path.getsize(MID_DIR)
                    print("file_size: %d bytes" % file_size)

                    print(file_list[i] + " 전송시작")
                    self.request.sendall(data)
                    print(file_list[i] + " 전송완료")

        
        # ex) "find_id, username, email"
        
        if (tdata[0] == 'find_id'):
            print("##id를 찾습니다.##\n\n")

        # ex) "find_pw, id, email"
        '''if (tdata[0] == 'find_pw'):
            print("##pwd를 찾습니다.##\n\n")'''

        # 10.개인정보 수정화면(my)
        
        # ex) "my, username, id, email"
        if (tdata[0] == 'my'):
            print("##개인정보를 수정합니다.##\n\n")
            # 누구의 정보(impdata -> 현재 사용중인 사용자의 id)를
            # 어떻게 수정할지(tdata -> username, id, email)
            myDB(impdata, tdata[1], tdata[2], tdata[3])

        # +faq, notice 화면?


# login DB 연동
def loginDB(uid, pwd):
    print('loginDB 연동 완료')

    sql = "SELECT EXISTS(SELECT *FROM USER WHERE ID=%s AND PWD=%s)"
    try:
        cursor.execute(sql, (uid, pwd))
        connect.commit()
        print('정보있음')
        return runServer.login(suc)

    except Exception as f:
        print(f)
        print('정보없음')
        return runServer.login(fail)


# checkid DB 연동
def checkidDB(uid):
    print('checkidDB 연동 완료')

    sql = "SELECT * FROM USER WHERE ID=%s"
    try:
        cursor.execute(sql, uid)
        connect.commit()
        print('id 중복o')
        return runServer.checkid(fail)

    except Exception as f:
        print(f)
        print('id 중복x')
        return runServer.checkid(suc)

# Auth DB 연동
def AuthDB(username, uid, pwd, email):
    print('AuthDB 연동 완료')

    # 인증코드는 아직 못받아서 Auth = ''
    sql = "INSERT INTO USER(USERNAME, ID, PWD, EMAIL, AUTH) values(%s, %s, %s, %s, '')"
    try:
        cursor.execute(sql, (username, uid, pwd, email))
        connect.commit()
        print('회원가입 중인 ', username, '정보 USER 테이블에 삽입성공')
        return runServer.auth(suc)

    except Exception as f:
        print(f)
        print('회원가입 중인 ', username, '정보 USER 테이블에 삽입실패')
        return runServer.auth(fail)

# checkAuth DB 연동
def checkAuthDB(regid, Auth, checkAuth):
    print('checkAuthDB 연동 완료')


    "UPDATE USER SET USERNAME=%s, ID=%s, EMAIL=%s WHERE ID=%s"
    sql = "UPDATE USER SET AUTH= %s WHERE(SELECT *FROM USER WHERE ID=%s)"
    cursor.execute(sql, (Auth, regid))

    sql1 = "SELECT EXISTS(SELECT *FROM USER WHERE AUTH= %s)"
    try:
        cursor.execute(sql1, checkAuth)
        connect.commit()
        print(regid, "인증 성공")
        return runServer.register(suc)

    except Exception as f:
        print(f)
        print(regid, "인증 실패")
        return runServer.register(fail)

# register DB 연동  -----
'''def registerDB(username, id, pwd, email):
    print('registerDB 연동 완료')


    if (cursor.execute("INSERT INTO USER(USERNAME, ID, PWD, EMAIL, AUTH) values(username, id, pwd, email)")):
        print('USER 테이블 삽입성공')
        return runServer.register(suc)
    else:
        print('USER 테이블 삽입실패')
        return runServer.register(fail)'''


# my DB 연동
def myDB(uid, username, rid, email):
    print('myDB 연동 완료')
    sql = "UPDATE USER SET USERNAME=%s, ID=%s, EMAIL=%s WHERE ID=%s"
    try:
        cursor.execute(sql, (username, uid, email, rid))
        connect.commit()
        print('USER 정보 수정성공')
        return runServer.my(suc)

    except Exception as f:
        print(f)
        print('USER 정보 수정실패')
        return runServer.my(fail)

# 서버연동
def runServer():
    print('서버시작')
    try:
        
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)

    except KeyboardInterrupt:
        print('서버를 종료합니다')

    def login(result):  # 로그인 정보 확인여부 앱으로 보내기
        return server.sendall(result)

    def checkid(result):  # id 중복 정보 확인여부 앱으로 보내기
        return server.sendall(result)

    def auth(result):  # 회원가입중인 사용자 데이터 삽입여부 앱으로 보내기
        return server.sendall(result)

    def checkauth(result):  # 인증코드 일치여부 앱으로 보내기
        return server.sendall(result)

    def register(result):  # 새로운 회원정보 등록여부 앱으로 보내기
        return server.sendall(result)

    def my(result):  # 사용자 정보 수정 성공여부 앱으로 보내기
        return server.sendall(result)



runServer()
