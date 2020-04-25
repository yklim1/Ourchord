#곰돌이 오선 좌표 323, 335, 349, 362, 375, 588, 600, 614, 626, 640, 856, 868, 882, 895, 907

import cv2
import numpy as np
import copy
from matplotlib import pyplot as plt
from operator import itemgetter

standard_detect_gap = 13

#음표 좌표 추출
def note_search(imgpath):
    #img_rgb = cv2.imread('.vscode\score4.png', 0) 

    stafflist = detect_staff(imgpath)
    reszie_rate=averge_rate_staff(stafflist)
    resize_img_path =resize_image(imgpath,reszie_rate)
    resize_stafflist = detect_staff(resize_img_path)

    img_rgb = cv2.imread(resize_img_path, 0) 
    img_rgb2 = cv2.imread(resize_img_path, 0)
    img_gray = cv2.imread(resize_img_path, cv2.COLOR_BGR2GRAY)
    
    lists = ['.vscode//qu1.png','.vscode//qu2.png','.vscode//qu3.png','.vscode//qu4.png','.vscode//qu5.png','.vscode//qu6.png','.vscode//ha1.png','.vscode//ha2.png','.vscode//ha3.png','.vscode//ha4.png']#나중 DB 경로로 수정
    
    xylist = template_note_list(resize_img_path,lists)

    #테스트 좌표
    #stafflist = [323, 335, 349, 362, 375, 588, 600, 614, 626, 640, 856, 868, 882, 895, 907]
    note_image(xylist,resize_stafflist,resize_img_path)
    


def template_note_list(imgpath, temlist):
    #img_rgb = cv.imread('.vscode\score4.png', 0) 
    img_rgb = cv2.imread(imgpath, 0) 
    img_gray = cv2.imread(imgpath, cv2.COLOR_BGR2BGRA)
    ret, dst = cv2.threshold(img_gray,100,255,cv2.THRESH_BINARY)
    #x = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
    img_rgb2 = cv2.imread(imgpath, cv2.COLOR_BGR2GRAY)

    lists = ['.vscode//qu1.png','.vscode//qu2.png','.vscode//qu3.png','.vscode//qu4.png','.vscode//qu5.png','.vscode//qu6.png','.vscode//ha1.png','.vscode//ha2.png','.vscode//ha3.png','.vscode//ha4.png']#나중 DB 경로로 수정

    xylist=[]
    xylist.append([])
    i=0
    for image in lists:
        template = cv2.imread(image,0)
        ret1, dst1 = cv2.threshold(template,100,255,cv2.THRESH_BINARY)
        #template_gray = cv.cvtColor(dst1,cv.COLOR_BGR2RGB)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(dst,template,cv2.TM_CCOEFF_NORMED) #0.6<x< 0.65
        #res = cv.matchTemplate(x,dst1,cv.TM_CCOEFF_NORMED) #0.6<x< 0.65 
        threshold = 0.65
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
            #print(pt, (pt[0] + w, pt[1] + h))
            #print(pt[0])
            xylist[i].append(pt[0])
            xylist[i].append(pt[1])
            xylist.append([])
            i=i+1
    #빈 리스트 삭제
    del xylist[len(xylist)-1]

    num=len(xylist)
    xylist.sort(key=itemgetter(1))
    remlist=[]
    k=0

    for i in range(len(xylist)-1):
        for j in range(i+1,len(xylist)-1):
        #for j in range(len(xylist)-1):
            if abs(xylist[i][0]-xylist[j][0])<5 and abs(xylist[i][1]-xylist[j][1])<5 :
                remlist.append(i)

    remlist=list(set(remlist))
    remlist.sort()
    remnum=len(remlist)-1

    #중복 좌표 제거
    for i in range(remnum, -1, -1):
        del xylist[remlist[i]]

    num = len(xylist)-1
    #y좌표를 오름차순으로 정렬
    xylist.sort(key=itemgetter(1))
    return xylist

def note_image(xylist,stafflist,image_path):

    img_rgb = cv2.imread(image_path, 0) 
    #테스트 오선 없는 것
    #img_white = cv2.imread('.vscode/whiteimg.png',0)
    num = len(xylist)-1
    #y좌표를 오름차순으로 정렬
    xylist.sort(key=itemgetter(1))
    m=1
    print(stafflist)
    staffnum = int(len(stafflist)/5)
    updownlist = []
    #밑에 음표 자르는 부분 def 로 변환 필요
    for i in range(num):
        #testcopy = img_rgb.copy()
        for j in range(0,staffnum*2):
            if(j%2 == 0):
                if(xylist[i][1]<stafflist[5*int(j/2)+2]):
                    updownlist.append("down")
                    print(f"{m}번째 : ", xylist[i][0],xylist[i][1], updownlist[i])
                    #cv2.rectangle(img_rgb2, (xylist[i][0]-2,xylist[i][1]-3), (xylist[i][0] + 31, xylist[i][1] + 60), (0,0,255), 1)
                    testcopy = img_rgb[xylist[i][1]-3:xylist[i][1]+60, xylist[i][0]-2:xylist[i][0]+31]
                    cv2.imwrite(f'.vscode\ee\down\{i}.png',testcopy)
                    break
            else:
                if(xylist[i][1]<stafflist[5*int(j/2)+4]+20):
                    updownlist.append("up")
                    print(f"{m}번째 : ", xylist[i][0],xylist[i][1], updownlist[i])
                    #cv2.rectangle(img_rgb2, (xylist[i][0]-2,xylist[i][1]-48), (xylist[i][0] + 31, xylist[i][1] + 15), (0,0,255), 1)
                    testcopy = img_rgb[xylist[i][1]-48:xylist[i][1]+15, xylist[i][0]-2:xylist[i][0]+31]
                    cv2.imwrite(f'.vscode\ee//up\{i}.png',testcopy)
                    break
        #cv.rectangle(img_rgb2, (xylist[i][0]-2,xylist[i][1]-48), (xylist[i][0] + 31, xylist[i][1] + 15), (0,0,255), 1)
        #print(f"{m}번째 : ", xylist[i][0],xylist[i][1], updownlist[i])
        #testcopy = img_rgb[xylist[i][1]:xylist[i][1]+18, xylist[i][0]:xylist[i][0]+13]
        #cv2.imwrite(f'.vscode\stest{i}.png',testcopy) #추후 DB저장으로 수정
        m=m+1

    print("갯수", len(updownlist))
    cv2.waitKey(0)

# 오선 비율 확인
def averge_rate_staff(stafflist):
    gaplist=[]

    for i in range(int(len(stafflist)/5)):
        for j in range(4):
            #print((staff[5*i+j+1],staff[5*i+j]))
            gaplist.append((stafflist[5*i+j+1]-stafflist[5*i+j]))

    print(gaplist)
    averagegap = sum(gaplist)/len(gaplist)
    #averagegap = round(averagegap,3)
    print(averagegap)
    rate = standard_detect_gap/averagegap
    round(rate,3)

    return rate

# 오선 좌표구하는 함수, 입력 값 : 이미지 경로 , 출력 값 : 오선 좌표 리스트
def detect_staff(imagepath):
    img = cv2.imread(imagepath,cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #테스트용인 곰세마리는 임계값 230으로 해야 다 뽑힌다. 그래서 230으로 테스트
    ret, dst = cv2.threshold(gray, 230,255,cv2.THRESH_BINARY)#ret에는 임계값이 저장
    height, width = gray.shape

    ylist=[0 for _ in range(height)]#이미지 높이 만큼 값 0을 가진 리스트 생성 => ylist[높이만큼 개수] = [0]

    for i in range(height):#y좌표
        for j in range(width):#x좌표
            px = dst[i,j]
            if(px==0):
                ylist[i] +=1

    staff=[]#오선 좌표
    for i in range(len(ylist)):
        if(ylist[i]>width*0.8):#이미지 크기의 너비의 80%이상일 때 오선으로 간주

            staff.append(i)

    removelsit=[]#제거할 원소 자리
    #중복 제거 2픽셀이하로 가까우면 제거 리스트에 들어간다.
    for i in range(len(staff)-1):
        if(staff[i+1]-staff[i]<3):
            removelsit.append(i)

    for i in range(len(removelsit)-1, -1, -1):#내림차순한 이유는 오름차순으로 제거하면 삭제되면서 정확한 데이터가 삭제가 안된다.
        del staff[removelsit[i]]
    
    return staff

def resize_image(imgpaht, rate):
    img_source = cv2.imread(imgpaht,0)
    resize_img_path = '.vscode//resizeaa.png'
    #이미지 변환
    img_result = cv2.resize(img_source, None, fx=rate, fy=rate, interpolation = cv2.INTER_CUBIC)
    #cv2.imshow("x2", img_result)
    cv2.imwrite(resize_img_path,img_result)
    
    return resize_img_path


'''
#오선과 오선 사이 중간값 구하는 것, 활용할지는 보류
checkrange = []
for i in range(1,staffnum):
    checkrange.append(int((stafflist[5*i]+stafflist[5*i-1])/2))
print(checkrange)
checkrangenum = int(len(checkrange))
''' 

#main

imgpath = '.vscode//18-1.png'
note_search(imgpath)

#note_search(imgpath)
