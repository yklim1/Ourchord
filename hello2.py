import cv2 as cv
import numpy as np
import copy
from matplotlib import pyplot as plt
from operator import itemgetter


img_rgb = cv.imread('.vscode\score4.png', 0) 
img_rgb1 = cv.imread('.vscode\score4.png', cv.COLOR_BGR2GRAY)
img_rgb2 = cv.imread('.vscode\score4.png', cv.COLOR_BGR2GRAY)
#img_gray = cv.cvtColor(img_rgb, cv.COLOR_BAYER_BG2GRAY)

lists = ['.vscode\mat2.png','.vscode\mat10.png','.vscode\mat3.png']

xylist=[]
xylist.append([])
i=0
for image in lists:
    template = cv.imread(image,0)
    w, h = template.shape[::-1]

    res = cv.matchTemplate(img_rgb1,template,cv.TM_CCOEFF_NORMED)
    #res = cv.matchTemplate(img_gray,template,cv.TM_CCORR)
    #res = cv.matchTemplate(img_gray,template,cv.TM_CCORR_NORMED)
    #res = cv.matchTemplate(img_gray,template,cv.TM_SQDIFF)
    #res = cv.matchTemplate(img_gray,template,cv.TM_SQDIFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb1, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
        #print(pt, (pt[0] + w, pt[1] + h))
        #print(pt[0])
        xylist[i].append(pt[0])
        xylist[i].append(pt[1])
        xylist.append([])
        i=i+1
#빈 리스트 삭제
del xylist[len(xylist)-1]

#x좌표로 정렬
xylist.sort(key=itemgetter(0))

#print(xylist)
num=len(xylist)
remlist=[]
k=0

#중복 좌표 추출
for i in range(len(xylist)-1):
    if abs(xylist[k][0]-xylist[i][0])>2:
        #print(k,i)
        for j in range(k,i+1):
            for z in range(j+1,i+1):
                if abs(xylist[j][1]-xylist[z][1])<6:
                    remlist.append(z)
                    #print(z)
        k=i


for i in range(len(xylist)-1):
    #print (xylist[i][1])
    if xylist[i][1]>=1650:
        remlist.append(i)
        #print(xylist[i][1])

remlist=list(set(remlist))
remlist.sort()
remnum=len(remlist)-1

#중복 좌표 제거
for i in range(remnum, 0, -1):
    del xylist[remlist[i]]

num = len(xylist)-1

for i in range(num):
    cv.rectangle(img_rgb2, (xylist[i][0],xylist[i][1]), (xylist[i][0] + 18, xylist[i][1] + 13), (0,0,255), 1)
    print(xylist[i][1])
'''
cv.rectangle(img_rgb2, (1747,1748), (1747 + 18, 1748 + 13), (255,0,255), 2)
cv.rectangle(img_rgb2, (1748,1801), (1748 + 18, 1801 + 13), (255,0,255), 2)
cv.line(img_rgb2, (0, 1748), (2000, 1748), (255, 0, 255), 2)
cv.line(img_rgb2, (1650, 0), (1650, 2000), (255, 0, 255), 2)
'''
#print(xylist)
'''
copylist=copy.deepcopy(xylist)
k=-1
dl=[]
num=len(copylist)
for i in range(0,len(copylist)-1):
    
    if i > k:
        while copylist[len(copylist)-1-i][0]-copylist[len(copylist)-2-k][0]<3:
            k=k+1
            if(k == len(copylist)-1):
                break
        #print(i,k)
        for t in range(i,k+1):
            for z in range(i+1,k+1):
                if 0<abs(copylist[len(copylist)-1-t][1]-copylist[len(copylist)-2-z][1])<3:
                    dl.append(len(copylist)-1-t)

#cv.imwrite('.vscode\sres.png',img_rgb1)
#cv.imshow('result', img_rgb1)



dl=list(set(dl))
x=len(xylist)-1
for i in dl:
    del xylist[x-i]


#print(xylist[1][1])

x=len(xylist)-1
#for i in range(x):
    #cv.rectangle(img_rgb2, (xylist[i][0],xylist[i][1]), (xylist[i][0] + 18, xylist[i][1] + 13), (0,0,255), 1)
    #print(xylist[0],xylist[1])
    #print(xylist, sep='\n')
    

    #if abs(copylist[len(copylist)-1-i][1]-copylist[len(copylist)-2-i][1])<3:
        #del xylist[len(copylist)-1-i]
            

#for i in xylist:
    #print(i)


'''
cv.imwrite('.vscode\sres.png',img_rgb1)
cv.imwrite('.vscode\sres2.png',img_rgb2)
cv.imshow('result2', img_rgb2)
cv.imshow('result1', img_rgb1)
cv.waitKey(0)
