# mfile/test.py
import pymysql
import socketserver
import glob
import os
from os import listdir #SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장
from os.path import isfile, join #SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장

SPDF_DIR = '/' # DIR-> SPDF_DIR
HOST = ''
BUFSIZE = 1048576
PORT = ''

connect = pymysql.connect()

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

        # ---------------------화면별 받은 정보 저장 이후 --------------------

##############7.서버에서 생성된 mid 파일 앱으로 전송(midiupload_folder)##############

        if (tdata[0] == 'folder'):
            print("##생성된 mid 파일을 앱으로 전송합니다.##\n\n")

            # 변환 전/변환 후 화면 구분
            # 'midiupload_folder-B or C' 받음
            # tdata[1] = 'B' /tdata[1] = 'C'

            while True:
                try:
                    # 디렉토리 내 파일 유무 확인
                    mfile_list = glob.glob(SPDF_DIR)  # SPDF_DIR -> pdir로 바꾸기
                    #conn = self.request()

                    if len(mfile_list) != 1:
                        print(SPDF_DIR + "파일이 없습니다.")
                        self.request.sendall(bytes[0])
                    else:
                        # SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장
                        # SPDF_DIR -> pdir로 바꾸기
                        files = [f for f in listdir(SPDF_DIR) if isfile(join(SPDF_DIR, f))]
                        print("모든 MIDI 파일리스트:", files)

                        # 안드로이드에서 upload_tab 클릭시 - 기존 MIDI 파일 전송
                        # 안드로이드에서 'B' 보내주기
                        if (tdata[1] == 'B'):  # 변환 전
                            # ex) 기존: A -> BaseA_12.mid
                            files = [i for i in files if i.find('Base') != -1]

                            # mid파일 확장자 한번 더 files에서 뽑아내고 for문으로 전송
                            files = [i for i in files if i.find('.mid') != -1]
                            print("변환 전 MIDI 파일리스트:", files)

                            for i in files:
                                # 파일 사이즈
                                # file_size = int.from_bytes(self.request.recv(BUFSIZE), byteorder="big")
                                file_fullpath = SPDF_DIR + i  # ex) USER/ 아래있는 MIDI 파일 경로 합친거 (/home/ec2-user/Ourchord/USER/12.mid)
                                # 'Base'문자열을 가진 '.mid'확장자파일만 전송
                                print("파일 경로입니다." + file_fullpath)
                                print("파일 이름" + i)

                                print("##전송할 데이터##")
                                f = open(file_fullpath, 'rb')
                                s = f.read()
                                print(s)

                                file_list = glob.glob(file_fullpath)  # glob모듈의 glob()
                                if len(file_list) != 1:
                                    print(i + " 파일없음")
                                    self.request.sendall(bytes([0]))
                                    continue
                                else:
                                    file_size = os.path.getsize(file_fullpath)
                                    print("file size: %d bytes" % file_size)

                                    # 파일 갯수 보내기
                                    self.request.sendall(len(files))
                                    # 파일 길이 보내기
                                    self.request.sendall(file_size)
                                    # 파일 이름 보내기
                                    self.request.sendall(i)

                                    # length=8:데이터길이
                                    # byteorder="big": 바이트 순서 빅엔디안
                                    self.request.sendall((file_size).to_bytes(length=8, byteorder="big"))

                                client_status = self.request.recv(1)
                                if client_status == bytes([255]):
                                    print(i + " 전송시작")
                                    with open(file_fullpath, "rb") as f:
                                        self.request.sendfile(f)
                                    self.request.sendall(bytes([255]))
                                    print(i + " 전송완료")
                                    print("성공했으니 바로 종료합니다.")
                                else:
                                    print("Client's Rejection")

                        # 안드로이드에서 midiupload_tab 클릭시 - 변환된 MIDI 파일 전송
                        # 안드로이드에서 'C' 보내주기
                        if (tdata[1] == 'C'):  # 변환 후
                            # ex) 변경: B -> ChangeB_12.mid
                            files = [i for i in files if i.find('Change') != -1]
                            files = [i for i in files if i.find('.mid') != -1]
                            print("변환 후 MIDI 파일리스트:", files)

                            # 'Change'문자열을 가진 '.mid'확장자파일만 전송
                            for i in files:
                                # 파일 사이즈
                                # file_size = int.from_bytes(self.request.recv(BUFSIZE), byteorder="big")
                                file_fullpath = SPDF_DIR + i  # ex) USER/ 아래있는 MIDI 파일 경로 합친거 (/home/ec2-user/Ourchord/USER/12.mid)
                                # 'Base'문자열을 가진 '.mid'확장자파일만 전송
                                print("파일 경로입니다." + file_fullpath)
                                print("파일 이름" + i)

                                print("##전송할 데이터##")
                                f = open(file_fullpath, 'rb')
                                s = f.read()
                                print(s)

                                file_list = glob.glob(file_fullpath)  # glob모듈의 glob()
                                if len(file_list) != 1:
                                    print(i + " 파일없음")
                                    self.request.sendall(bytes([0]))
                                    continue
                                else:
                                    file_size = os.path.getsize(file_fullpath)
                                    print("file size: %d bytes" % file_size)

                                    # 파일 갯수 보내기
                                    self.request.sendall(len(files))
                                    # 파일 길이 보내기
                                    self.request.sendall(file_size)
                                    # 파일 이름 보내기
                                    self.request.sendall(i)

                                    # length=8:데이터길이
                                    # byteorder="big": 바이트 순서 빅엔디안
                                    # 여기부터 진행이 안됨
                                    '''self.request.sendall((file_size).to_bytes(length=8, byteorder="big"))

                                client_status = self.request.recv(1)
                                if client_status == bytes([255]):
                                    print(i + " 전송시작")
                                    with open(file_fullpath, "rb") as f:
                                        self.request.sendfile(f)
                                    self.request.sendall(bytes([255]))
                                    print(i + " 전송완료")
                                    print("성공했으니 바로 종료합니다.")
                                else:
                                    print("Client's Rejection")'''

                except ConnectionError:
                    print("ConnectionError 발생")
                except OSError:
                    print("OSError 발생")
                except :
                    print("bad-requestError 발생")
                finally:
                    self.request.close()

def runServer():
    print('서버시작')
    try:
        # 1. 사용자가 화면 실행할때마다 MyTcpHandler함수에서 배열 update
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()

    except KeyboardInterrupt:
        print('서버를 종료합니다')

runServer()
