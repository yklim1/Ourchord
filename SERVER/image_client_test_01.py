import socket
import cv2
import numpy

TCP_IP = '127.0.0.1'
TCP_PORT = 9305

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

#capture = cv2.VideoCapture(0)
image = cv2.imread('/Users/zjisuoo/Desktop/jenny.jpeg')
#ret, frame = capture.read()

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
result, imgencode = cv2.imencode('.jpeg', image, encode_param)
data = numpy.array(imgencode)
stringData = data.tostring()

sock.send(str(len(stringData)).ljust(16));
sock.send(stringData);
sock.close()

decimg=cv2.imdecode(data,1)
cv2.imshow('CLIENT',decimg)
cv2.waitKey(0)
cv2.destroyAllWindows() 
