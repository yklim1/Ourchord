#파일전송
import socket
import argparse
import os
import sys
import tempfile

HOST = ''
PORT = ''
FILE = ''

def run(HOST, PORT, FILE):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print('연결됨')
        except:
            print('연결안됨')
            return

        try:
            s.sendall(FILE.encode())
            file_size = int.from_bytes(s.recv(4096), byteorder="big")

            if file_size == 0:
                print("서버에'" + FILE + "' 없음")
                return

            print("file name : " + FILE)
            print("size : %d" % file_size)
            print("\n(다운로드 시작)...")
            s.sendall(bytes([255]))

            nowdown_size = 0
            downbuff_size = 1048576

            with tempfile.NamedTemporaryFile(delete=False, dir=".") as f:
                temp_name = f.name
                while True:
                    if nowdown_size < file_size:
                        # min(): downbuff_size/file_size - nowdown_size중 작은것
                        resp = s.recv(min(downbuff_size, file_size - nowdown_size))
                        nowdown_size += len(resp)
                        f.write(resp)
                        print("Download %.2f%%" % min(100, nowdown_size / file_size * 100))
                        sys.stdout.flush()
                    else:
                        s.recv(1)
                        print("다운로드 성공!\n")
                        break
            os.replace(temp_name, FILE)

        except ConnectionError:
            print("Error: connection closed")
        except OSError:
            print("Error: cannot write file")
        except:
            print("Error: bad response")

run(HOST, PORT, FILE)
