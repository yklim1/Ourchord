import cv2
import numpy as np
import copy
import collections
from matplotlib import pyplot as plt
from operator import itemgetter

#복사
def binary_search_np(A, B):
    # assume A and B are numpy arrays
    idx2 = np.minimum(len(A) - 1, np.searchsorted(A, B)) 
    idx1 = np.maximum(0, idx2 - 1)
    idx2_is_better = np.abs(A[idx1] - B) > np.abs(A[idx2] - B)
    np.putmask(idx1, idx2_is_better, idx2)
    return A[idx1]


img = cv2.imread('.vscode\score4.png',cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img, (3,3), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 200, 300, apertureSize = 3)
minLineLength = 200
maxLineGap = 50
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
        #추출된 선간의 간격이 2이하일 때 하나 제거
        if ycounter[i]-item<3:
            y.remove(item)
    else:
        break
    i=i+1
i=1
for item in y:
    cv2.line(img, (0, item-1), (2000, item-1), (255, 0, 255), 2)
    print(f"{i}번째 : ", end=' ')
    print(item-1)
    i=i+1
gap= y[3]-y[2]
print(gap/2)


img_rgb = cv2.imread('.vscode\score4.png', 0) 
img_rgb1 = cv2.imread('.vscode\score4.png', cv2.COLOR_BGR2GRAY)
ret, dst = cv2.threshold(img_rgb1,100,255,cv2.THRESH_BINARY)
x = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
img_rgb2 = cv2.imread('.vscode\score4.png', cv2.COLOR_BGR2GRAY)
#img_gray = cv.cvtColor(img_rgb, cv.COLOR_BAYER_BG2GRAY)

lists = ['.vscode\solid-note.png','.vscode\quarter.png']

xylist=[]
xylist.append([])
i=0
for image in lists:
    template = cv2.imread(image,0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(x,template,cv2.TM_CCOEFF_NORMED) #0.6<x< 0.65
    #res = cv.matchTemplate(x,template,cv.TM_CCORR)
    #res = cv.matchTemplate(x,template,cv.TM_CCORR_NORMED) #0.73
    #res = cv.matchTemplate(x,template,cv.TM_SQDIFF)
    #res = cv.matchTemplate(x,template,cv.TM_SQDIFF_NORMED)
    threshold = 0.65
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb1, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
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
'''
for i in range(num):
    #testcopy = img_rgb.copy()
    cv2.rectangle(img_rgb2, (xylist[i][0],xylist[i][1]), (xylist[i][0] + 18, xylist[i][1] + 13), (0,0,255), 1)
    print(f"{m}번째 : ", xylist[i][0],xylist[i][1])
    #이미지 부분 저장
    #testcopy = img_rgb[xylist[i][1]:xylist[i][1]+18, xylist[i][0]:xylist[i][0]+13]
    #cv.imwrite(f'.vscode\stest{i}.png',testcopy)
    m=m+1

one=[]
two=[]
three=[]
four=[]
five=[]
six=[]
seven=[]
eight=[]
'''
checknum=0

onelist=[]
twolist=[]
threelist=[]
fourlist=[]
fivelist=[]
sixlist=[]
sevenlist=[]
eightlist=[]
ninelist=[]
tenlist=[]
elevenlist=[]
twelvelist=[]

for i in range(num):
    if(y[0]-30<xylist[i][1]<y[4]+30):
        onelist.append([])
        onelist[checknum].append(xylist[i][0])
        onelist[checknum].append(xylist[i][1])
        checknum=checknum+1
    checknum=0

    if(y[5]-30<xylist[i][1]<y[9]+30):
        twolist.append([])
        twolist[checknum].append(xylist[i][0])
        twolist[checknum].append(xylist[i][1])
        checknum=checknum+1
    checknum=0

    if(y[10]-30<xylist[i][1]<y[14]+30):
        threelist.append([])
        threelist[checknum].append(xylist[i][0])
        threelist[checknum].append(xylist[i][1])
        checknum=checknum+1 
    checknum=0

    if(y[15]-30<xylist[i][1]<y[19]+30):
        fourlist.append([])
        fourlist[checknum].append(xylist[i][0])
        fourlist[checknum].append(xylist[i][1])
        checknum=checknum+1    
    checknum=0

    if(y[20]-30<xylist[i][1]<y[24]+30):
        fivelist.append([])
        fivelist[checknum].append(xylist[i][0])
        fivelist[checknum].append(xylist[i][1])
        checknum=checknum+1
    checknum=0

    if(y[25]-30<xylist[i][1]<y[29]+30):
        sixlist.append([])
        sixlist[checknum].append(xylist[i][0])
        sixlist[checknum].append(xylist[i][1])
        checknum=checknum+1       
    checknum=0

    if(y[30]-30<xylist[i][1]<y[34]+30):
        sevenlist.append([])
        sevenlist[checknum].append(xylist[i][0])
        sevenlist[checknum].append(xylist[i][1])
        checknum=checknum+1    
    checknum=0

    if(y[35]-30<xylist[i][1]<y[39]+30):
        eightlist.append([])
        eightlist[checknum].append(xylist[i][0])
        eightlist[checknum].append(xylist[i][1])
        checknum=checknum+1     
    checknum=0

    if(y[40]-30<xylist[i][1]<y[44]+30):
        ninelist.append([])
        ninelist[checknum].append(xylist[i][0])
        ninelist[checknum].append(xylist[i][1])
        checknum=checknum+1      
    checknum=0

    if(y[45]-30<xylist[i][1]<y[49]+30):
        tenlist.append([])
        tenlist[checknum].append(xylist[i][0])
        tenlist[checknum].append(xylist[i][1])
        checknum=checknum+1       
    checknum=0

    if(y[50]-30<xylist[i][1]<y[54]+30):
        elevenlist.append([])
        elevenlist[checknum].append(xylist[i][0])
        elevenlist[checknum].append(xylist[i][1])
        checknum=checknum+1     
    checknum=0

    if(y[55]-30<xylist[i][1]<y[59]+30):
        twelvelist.append([])
        twelvelist[checknum].append(xylist[i][0])
        twelvelist[checknum].append(xylist[i][1])
        checknum=checknum+1      
    checknum=0


    print(f"{m}번째 : ", xylist[i][0],xylist[i][1])
    m=m+1

print(len(onelist))
print(len(twolist))
print(len(threelist))
print(len(fourlist))
print(len(fivelist))
print(len(sixlist))
print(len(sevenlist))
print(len(eightlist))
print(len(ninelist))
print(len(tenlist))
print(len(elevenlist))
print(len(twelvelist))

'''
cv2.imwrite('.vscode\sres.png',img_rgb1)
cv2.imwrite('.vscode\sres2.png',img_rgb2)
cv2.imwrite('.vscode\sres3.png',dst)
cv2.imshow('result2', img_rgb2)
cv2.imshow('result1', img_rgb1)
cv2.imshow('SCORE_EDGE', edges)
cv2.imshow('RESULT', img)
cv2.imwrite('.vscode\musicresult.png',img)

cv.waitKey(0)
'''



