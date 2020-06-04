#s0605file.py
import socket
import os
import sys
import glob

HOST = ''
BUFSIZE = 1048576
PORT = 
DIR = '/home/ec2-user/Ourchord/MIDI/12.mid'

def run_server(PORT, DIR):
    print("연결 대기상태..")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(1)
        #conn, addr = sock.accept()
    except:
        print('연결안됨: +포트 사용 중인지 체크')
        return

    while True:
        try:
            conn, addr = sock.accept()
            print('연결완료: ', addr)
            print('보낼 데이터: ', DIR)

            # 파일 유무 체크
            file_list = glob.glob(DIR)
            if len(file_list) != 1:
                print(DIR + "파일없어")
                conn.sendall(bytes[0])
                continue
            else:
                f = open(DIR, 'rb')
                # file_size = os.path.getsize(DIR)
                data = f.read()  # mid파일
                print("전송 전 데이터: ", data)
                # 전송할 파일 size
                file_size = os.path.getsize(DIR)
                print("file_size: %d bytes" % file_size)

                #1
                #conn.sendall(file_size.to_bytes(length=8, byteorder="big"))# 여기까지 실행되고 멈춤

                print(DIR + " 전송시작")
                conn.sendall(data)
                #f.flush()
                #f.close()
                print(DIR + " 전송완료")
                print("성공했으니 바로 종료합니다.")

            '''with open(DIR, "rb") as fl:
                #2
                f1 = conn.sendall(fl)
                print("전송할 데이터: ", f1)
                f.flush()
                f.close()
                #conn.sendfile(fl)
                #conn.sendall(bytes([255]))
                print(DIR + "전송완료")
                print("성공했으니 바로 종료합니다.")'''
            #else:
                #print("Client's Rejection")

        except ConnectionError:
            print("Error: connection closed")
        except OSError:
            print("Error: cannot read file")
        except:
            print("Error: bad request")
        finally:
            try:
                conn.close()
            except:
                pass

run_server(PORT, DIR)
