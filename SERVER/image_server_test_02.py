import socket
import argparse
import os
from os.path import exists

def run_server(port, directory) :
    host = ''

    with socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) as s :
        s.bind((host, port))
        s.listen(1)

        conn, addr = s.accept()
        fileName = conn.recv(1024)
        fileName =   fileName.decode()

        if not exists(directory + "/" +fileName) :
            msg = "error"
            conn.sendall(msg.encode())
            conn.close()
            return

        conn.sendall(getFIleeSize(fileName, directory).encode())

        reReady = conn.recv(1024)
        if reReady.decode()  == "ready" :
            conn.sendall(getFileData(fileName, directory).encode())
        conn.close()

def getFileSize(fileName, directory)  :
    fileSize = os.path.getsize(directory + "/" + fileName)
    return str(fileSize)

def getFileData(fileName, directory) :
    with open(directory + "/" + fileName, 'r', encoding = "UTF-8") as f :
        data = ""
        for line in f :
            data += line
        return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo server -p port -d directory")
    parser.add_argument('-p', help="port_number", required=True)
    parser.add_argument('-d', help="directory", required=True)

    args = parser.parse_args()
    run_server(port=int(args.p), directory=args.d)