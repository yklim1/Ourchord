import cv2 as cv
import numpy as np
import copy
from matplotlib import pyplot as plt
from operator import itemgetter


img_rgb = cv.imread('.vscode\score4.png', 0) 
img_rgb1 = cv.imread('.vscode\score4.png', cv.COLOR_BGR2GRAY)
ret, dst = cv.threshold(img_rgb1,100,255,cv.THRESH_BINARY)
x = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
img_rgb2 = cv.imread('.vscode\score4.png', cv.COLOR_BGR2GRAY)
#img_gray = cv.cvtColor(img_rgb, cv.COLOR_BAYER_BG2GRAY)

lists = ['.vscode\solid-note.png','.vscode\quarter.png']
#lists = ['.vscode\half1.png']
#lists = ['.vscode\half-note-line.png']#잘못 뽑힘

xylist=[]
xylist.append([])
i=0
for image in lists:
    template = cv.imread(image,0)
    #ret1, dst1 = cv.threshold(template,100,255,cv.THRESH_BINARY)
    w, h = template.shape[::-1]

    res = cv.matchTemplate(x,template,cv.TM_CCOEFF_NORMED) #0.6<x< 4분음표 :0.65 2분음표 : 0.56<x<0.6
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

#print(xylist)
#x좌표로 정렬
#xylist.sort(key=itemgetter(0))

#m=1
#print(xylist)
num=len(xylist)
'''
for i in range(num):
    #cv.rectangle(img_rgb2, (xylist[i][0],xylist[i][1]), (xylist[i][0] + 18, xylist[i][1] + 13), (0,0,255), 1)
    print(f"{m}번째 : ", xylist[i][0],xylist[i][1])
    m=m+1
'''
remlist=[]
k=0

#중복 좌표 추출
#print(xylist)
'''
for i in range(len(xylist)-1):
    if abs(xylist[k][1]-xylist[i][1])>5:
        print(k,i)
        for j in range(k,i+1):
            for z in range(j+1,i+1):
                if abs(xylist[j][0]-xylist[z][0])<5:
                    remlist.append(z)
                    #print(z)
        k=i

for i in range(len(xylist)-1):
    #print (xylist[i][1])
    if xylist[i][1]>=1650:
        remlist.append(i)
        #print(xylist[i][1])
'''
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
    cv.rectangle(img_rgb2, (xylist[i][0],xylist[i][1]), (xylist[i][0] + 18, xylist[i][1] + 13), (0,0,255), 1)
    '''
    text = "좌표"
    font = cv.FONT_HERSHEY_DUPLEX
    red = (0, 0, 255)
    cv.putText(img_rgb2,text,(xylist[i][0],xylist[i][1]),fontScale=0.7, color=red, thickness=1)
    '''
    print(f"{m}번째 : ", xylist[i][0],xylist[i][1])
    m=m+1
'''
cv.rectangle(img_rgb2, (1747,1748), (1747 + 18, 1748 + 13), (255,0,255), 2)
cv.rectangle(img_rgb2, (1748,1801), (1748 + 18, 1801 + 13), (255,0,255), 2)
cv.line(img_rgb2, (0, 1748), (2000, 1748), (255, 0, 255), 2)
cv.line(img_rgb2, (1650, 0), (1650, 2000), (255, 0, 255), 2)
'''
#cv.line(img_rgb2, (362, 1420), (375, 1433), (255, 0, 255), 2)
#cv.line(img_rgb2, (1600, 0), (1600, 2000), (255, 0, 255), 2)
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
cv.imwrite('.vscode\sres3.png',dst)
cv.imshow('result2', img_rgb2)
cv.imshow('result1', img_rgb1)
cv.waitKey(0)
