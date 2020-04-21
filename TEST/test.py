import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('.vscode\score4.png',cv2.COLOR_BGR2GRAY)
#blur = cv2.GaussianBlur(img, (3,3), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(gray, 200, 300, apertureSize = 3)

# 흑백 반전
dst = cv2.bitwise_not(gray)

# 커널 생성
kernel = np.ones((9,9),np.uint8)

# para1 : 이미지, para2 : 함수 이용, para3 : 커널
gradient = cv2.morphologyEx(dst, cv2.MORPH_GRADIENT, kernel)


closing = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

'''
ret, thresh1 = cv2.threshold(dst,127,255, cv2.THRESH_BINARY)

ret, thresh5 = cv2.threshold(gray,127,255, cv2.THRESH_TOZERO_INV)

titles =['BINARY','TOZERO_INV']
images = [thresh1,thresh5]

for i in range(2):
	plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
	plt.title(titles[i])
	plt.xticks([]),plt.yticks([])
'''

ret, th1 = cv2.threshold(dst,127,255,cv2.THRESH_BINARY)

thr3 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)



#plt.show()

#cv2.imshow('SCORE_EDGE', edges)
#cv2.imshow('RESULT', img)
#cv2.imshow('gray', gray)
#cv2.imshow('흑백', dst)
#cv2.imshow("gradient",gradient)
#cv2.imshow("gradient2",thr3)
cv2.imshow("closing",closing)
cv2.imwrite('.vscode\closingresult.png',closing)
cv2.waitKey()
cv2.destroyAllWindows()