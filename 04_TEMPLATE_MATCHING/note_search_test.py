import cv2 as cv
import numpy as np
import copy
from matplotlib import pyplot as plt
from operator import itemgetter

img_rgb = cv.imread('/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/score1.png', 0) 
img_rgb1 = cv.imread('/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/score1.png', cv.COLOR_BGR2GRAY)
ret, dst = cv.threshold(img_rgb1,100,255,cv.THRESH_BINARY)
x = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
img_rgb2 = cv.imread('/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/score1.png', cv.COLOR_BGR2GRAY)
#img_gray = cv.cvtColor(img_rgb, cv.COLOR_BAYER_BG2GRAY)

lists = ['/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/NOTE_B/TemplateMatch/tem_full/tem_full_1.png','/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/NOTE_B/TemplateMatch/tem_empty/tem_empty_1.png']

xylist=[]
xylist.append([])
i=0
for image in lists:
    template = cv.imread(image,0)
    w, h = template.shape[::-1]

    res = cv.matchTemplate(x,template,cv.TM_CCOEFF_NORMED) #0.6<x< 0.65
    #res = cv.matchTemplate(x,template,cv.TM_CCORR)
    #res = cv.matchTemplate(x,template,cv.TM_CCORR_NORMED) #0.73
    #res = cv.matchTemplate(x,template,cv.TM_SQDIFF)
    #res = cv.matchTemplate(x,template,cv.TM_SQDIFF_NORMED)
    threshold = 0.65
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

num=len(xylist)
remlist=[]
k=0

for i in range(len(xylist)-1):
    for j in range(i+1,len(xylist)-1):
        if abs(xylist[i][0]-xylist[j][0])<5 and abs(xylist[i][1]-xylist[j][1])<5 :
            remlist.append(i)

remlist=list(set(remlist))
remlist.sort()
remnum=len(remlist)-1

#중복 좌표 제거
for i in range(remnum, -1, -1):
    del xylist[remlist[i]]

num = len(xylist)-1
m=1

for i in range(num):
    testcopy = img_rgb.copy()
    cv.rectangle(img_rgb2, (xylist[i][0],xylist[i][1]), (xylist[i][0] + 18, xylist[i][1] + 13), (0,0,255), 1)
    print(f"{m}번째 : ", xylist[i][0],xylist[i][1])
    testcopy = img_rgb[xylist[i][1]:xylist[i][1]+18, xylist[i][0]:xylist[i][0]+13]
    cv.imwrite(f'/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/template_test/test/test{i}.png',testcopy)
    m=m+1

#복사
cv.imwrite('/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/template_test/result/result1.png',img_rgb1)
cv.imwrite('/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/template_test/result/result2.png',img_rgb2)
cv.imwrite('/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/template_test/result/result3.png',dst)
cv.imshow('result2', img_rgb2)
cv.imshow('result1', img_rgb1)
cv.waitKey(0)