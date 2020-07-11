# mid구분
import socketserver
import glob
import os
from os import listdir #SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장
from os.path import isfile, join #SPDF_DIR 디렉토리 내 파일 리스트 리스트로 저장


HOST = ''
PORT = 9300
BUFSIZE = 1048576

SPDF_DIR = '/home/ec2-user/Ourchord/USER/'
# pdir = SPDF_DIR + impdata + "/"
# pdir: /home/ec2-user/Ourchord/USER/flottante/

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):

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
            if(display == "B"): #변환 전
            # ex) 기존: A -> BaseA_12.mid
                files = [i for i in files if i.find('Base') != -1]

                # mid파일 확장자 한번 더 files에서 뽑아내고 for문으로 전송
                files = [i for i in files if i.find('.mid') != -1]
                print("변환 전 MIDI 파일리스트:", files)

                # 파일 사이즈
                file_size = int.from_bytes(self.request.recv(BUFSIZE), byteorder="big")
                file_fullpath = SPDF_DIR + files # ex) USER/ 아래있는 MIDI 파일 경로 합친거 (/home/ec2-user/Ourchord/USER/12.mid)
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
            if(display == "C"): #변환 후
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

def run_server():
    print('서버시작')
    try:
        # 1. 사용자가 화면 실행할때마다 MyTcpHandler함수에서 배열 update
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()

    except KeyboardInterrupt:
        print('서버를 종료합니다')

run_server()
