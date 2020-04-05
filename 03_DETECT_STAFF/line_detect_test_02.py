#png 파일에서 오선 추출하기 
import cv2
import numpy as np
import collections
#from itertools import groupby, repeat, chain

def binary_search_np(A, B):
    # assume A and B are numpy arrays
    idx2 = np.minimum(len(A) - 1, np.searchsorted(A, B)) 
    idx1 = np.maximum(0, idx2 - 1)
    idx2_is_better = np.abs(A[idx1] - B) > np.abs(A[idx2] - B)
    np.putmask(idx1, idx2_is_better, idx2)
    return A[idx1]



img = cv2.imread('C:/testFile/linetest/138289/138289-4.png',cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img, (3,3), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #배경이 투명에서 다시 흰색으로 변환
edges = cv2.Canny(gray, 200, 250, apertureSize = 3) #악보 반쪽만 오선 추출되는거 해결
minLineLength = 50
maxLineGap = 100
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
ytest=[]
ycounter=[]
n=1
i=1
if lines is not None:
   for line in lines:
        x1, y1, x2, y2 = line[0]
        if y2-y1 == 0:
            ytest.append(y1)

container = collections.Counter(ytest)
for z in ytest:
    for k,v in container.items():
        #cv2.line(img, (0, k), (2000, k), (255, 0, 255), 2)
        #중복된 y좌표 선 개수 1개 초과할 때 즉, 2개 이상일 때
        if(v>1):
            #cv2.line(img, (0, k), (2000, k), (255, 255, 255), 2)
            ycounter.append(k)

ycounter = list(set(ycounter))
ycounter.sort()
#print(ycounter)
y=ycounter[:]
num=len(ycounter)
#print(num)
for item in ycounter:
    if i != num:
        #print(ycounter[i])
        #print(item)
        
        if ycounter[i]-item<21: 
            y.remove(item)
    else:
        break
    i=i+1
i=1
for item in y:
    cv2.line(img, (0, item-1), (4000, item-1), (255, 0, 255), 2)
    print(f"{i}번째 : ", end=' ')
    print(item-1)
    i=i+1
gap= y[3]-y[2]
print(gap/2)
#x=[40,100,180,230]
#notey=[128,140,141,159.5]



'''
            if 0<abs(z-k)<8:
                n=0
    
    if n!=0:
        ycounter.append(k)
        cv2.line(img, (0, k), (2000, k), (255, 0, 255), 2)
        n=1
'''




    
cv2.imshow('SCORE_EDGE', edges)
cv2.imshow('RESULT', img)
cv2.imwrite('C:/testFile/linetest/138289/138289-4check.png',img)
cv2.waitKey()
cv2.destroyAllWindows()
