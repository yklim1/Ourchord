#파일전송
import socket
import argparse
import glob
import os
import sys

PORT = ''
DIR = ''

def run_server(PORT, DIR):
    host = ''
    print("연결 대기상태..")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, PORT))
        sock.listen(1)
    except:
        print('연결안됨')
        return

    while True:
        try:
            conn, addr = sock.accept()
            file_name = conn.recv(4096).decode()
            file_fullpath = os.path.join(DIR, file_name)
            print("전송할 파일" + DIR + file_name)

            file_list = glob.glob(file_fullpath) #glob모듈의 glob()
            if len(file_list) != 1:
                print(DIR + file_name + " 파일없음")
                conn.sendall(bytes([0]))
                continue
            else:
                file_size = os.path.getsize(file_fullpath)
                print("file size: %d bytes" % file_size)
                #length=8:데이터길이
                #byteorder="big": 바이트 순서 빅엔디안
                conn.sendall((file_size).to_bytes(length=8, byteorder="big"))

            client_status = conn.recv(1)
            if client_status == bytes([255]):
                print(file_name + " 전송시작")
                with open(file_fullpath, "rb") as f:
                    conn.sendfile(f)
                conn.sendall(bytes([255]))
                print(file_name + " 전송완료")
                print("성공했으니 바로 종료합니다.")
                break
            else:
                print("Client's Rejection")

        except ConnectionError:
            print("Error: connection closed")
        except OSError:
            print("Error: cannot read file")
        except:
            print("Error: bad request")
        finally:
            try: conn.close()
            except: pass

run_server(PORT, DIR)
