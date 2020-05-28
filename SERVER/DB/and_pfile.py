import socket
import argparse
import glob
import os
import sys

HOST = '-'
#BUFSIZE = 1048576
PORT = -
DIR = '/home/ec2-user/Ourchord/MIDI/14.mid'

def run_server(PORT, DIR):
    print("연결 대기상태..")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(1)
    except:
        print('연결안됨')
        return

    while True:
        try:
            conn, addr = sock.accept()
            print("연결됨")
            print(conn)
            print("전송할 파일" + DIR)

            file_list = glob.glob(DIR)
            if len(file_list) != 1:
                print(DIR + " 파일없음")
                conn.sendall(bytes([0]))
                continue
            else:
                file_size = os.path.getsize(DIR)
                print("file size: %d bytes" % file_size)
                conn.sendall((file_size).to_bytes(8, byteorder="big"))

            client_status = conn.recv(1)
            if client_status == bytes([255]):
                print(DIR + " 전송시작")
                with open(DIR, "rb") as f:
                    conn.sendfile(f)
                conn.sendall(bytes([255].encode()))
                print(DIR + " 전송완료")
                # conn.shutdown(SHUT_RDWR)
                conn.close()
                print("성공했으니 바로 종료합니다.")
                break
            else:
                print("실패")

        except KeyboardInterrupt:
            sys.exit(0)

run_server(PORT, DIR)
