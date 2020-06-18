from __future__ import division
from pyknon.genmidi import Midi
from pyknon.music import NoteSeq, Note, Rest

import cv2
import numpy as np
import copy
from matplotlib import pyplot as plt
from operator import itemgetter
import pdb
import fitz

standard_detect_gap = 13

### 찾기 시작 함수


def note_search(imgpath):
    #img_rgb = cv2.imread('.vscode\score4.png', 0) 
    
    #테스트 조 설정
    base='C'
    change='C'

    #transegap : 조 변환 gap, stafflist : 기존 악보의 오선 좌표, reszie_rate : 기존 악보 오선과 탬플릿 매칭 오선 좌표 비율, resize_img_path : 리사이즈 된 악보 이미지
    #resize_stafflist : 리사이즈 된 악보의 오선 좌표, divideimglist : 악보 오선 별 로 자른 이미지 리스트

    # 조 변환 gap 구하는 함수
    # 입력 값 : 기존 조(코드), 변환 조(코드)      
    # 출력 값 : 두 조의 갭
    transegap = transpose(base,change)

    # 오선 좌표구하는 함수     
    # 입력 값 : 이미지 경로      
    # 출력(리턴) 값 : 오선 좌표 리스트
    stafflist = detect_staff(imgpath)

    # 오선 비율 구하는 함수      
    # 입력 값 : 오선 좌표 리스트      
    # 출력(리턴) 값 : 오선 비율 -> 오선 비율을 찾아 악보 이미지 크기 조정 후 탬플릿 매칭 이는 탬플릿 매칭 정확도 올리기 위한 작업
    reszie_rate=averge_rate_staff(stafflist)

    # 악보 리사이즈 함수     
    # 입력 값 : 악보 이미지,비율    
    # 출력(리턴) 값 : 리사이즈 된 이미지
    resize_img_path =resize_image(imgpath,reszie_rate)

    # 오선 좌표구하는 함수       
    # 입력 값 : 이미지 경로       
    # 출력(리턴) 값 : 오선 좌표 리스트
    # 리사이즈 된 오선 좌표
    resize_stafflist = detect_staff(resize_img_path)

    # 악보 오선으로 이미지 자르기 -> ex) 첫번째 오선 이미지, 두번째 오선 이미지 ...
    # 입력 값 : 리사이즈 된 악보 이미지, 리사이즈 된 오선 리스트
    # 출력 값 : 분류 된 오선 이미지
    divideimglist = dividescore(resize_img_path,resize_stafflist)

    # 이미지 및 설정
    notelists = ['.vscode//qu1.png','.vscode//qu2.png','.vscode//qu3.png','.vscode//qu4.png','.vscode//qu5.png','.vscode//qu6.png','.vscode//ha1.png','.vscode//ha2.png','.vscode//ha3.png','.vscode//ha4.png']#나중 DB 경로로 수정
    eightrest=['.vscode//eightrest.png']
    quarterrest=['.vscode//quarterrest.png']
    halfrest=['.vscode//halfrest.png']
    wholerest=['.vscode//wholerest.png']


    notevalue = '음표'
    eightvalue = 1/8
    quartervalue = 1/4
    halfvalue = 1/2
    wholevalue = 1

    #자른 오선 이미지의 오선 좌표
    divide_stafflist = [40,53,66,79,92]
    alllist = []

    for i in range(len(divideimglist)):
        # 이어져 있는 8,16음표 찾기
        # 입력 값 : 자른 오선 이미지
        # 출력 값 : 8, 16음표인 x 좌표
        checklinklist = checklink(divideimglist[i])

        # 탬플릿 매칭
        # 입력 값 : 오선으로 자른 이미지, 탬플릿 매칭할 이미지, 설정 값
        # 출력 값 : x,y좌표
        xylist = template_note_list(divideimglist[i],notelists,notevalue)

        #박자 딥러닝 하기전 테스트
        #여기다 박자 딥러닝 시킨거 해서 insert
        for a in range(len(xylist)):
            xylist[a].append(1/4)
        
        xylist.sort(key=itemgetter(0))

        # 박자 변환
        # 입력 값 : 음표 리스트, 8,16 음표의 x좌표 리스트
        # 출력 값 : 변환된 리스트
        
        chxylist = change_tempolist(xylist,checklinklist)

        #쉼표 좌표 찾기
        eightlist = template_note_list(divideimglist[i],eightrest,eightvalue)
        #print("8분 : ",eightlist)  
        quarterlist = template_note_list(divideimglist[i],quarterrest,quartervalue)
        #print("4분 : ",quarterlist)
        halflist = template_note_list(divideimglist[i],halfrest,halfvalue)
        #print("2분 : ",halflist)
        wholelist = template_note_list(divideimglist[i],wholerest,wholevalue)
        #print("온 : ",wholelist)

        #쉼표 리스트
        restlist = eightlist+quarterlist+halflist+wholelist
        #xylist.sort()
        #restlist.sort()

        #음계 추출-> y좌표를 가지고 음계 값 설정
        # 입력 값 : 자른 이미지의 오선 y좌표, 음표
        # 출력 값 : 음계가 insert 된 list
        scale_note_list = note_scale(divide_stafflist,chxylist)
        note_list = scale_note_list + restlist
        
        # 오선 순서
        for xy in range(len(note_list)):
            note_list[xy].append(i)

        note_list.sort(key=itemgetter(0))
        alllist = alllist + note_list

    #음계 체인지
    # 입력 값 : 음표 리스트, 바꿀 조 갭
    # 리턴 값 : 음계 변환 된 리스트
    change_list=changescale(alllist,transegap)

    # 화음 리스트 찾기
    # 입력 값 : 음표 리스트
    # 리턴 값 : 화음 정보 추가된 리스트 -> 리스트 정보 [x,y,박자,음계,오선번째,화음정보]  -> 화음정보 1이면 기본, 2이상 이면 그 수만큼의 개수, 0이면 제외 
    harmolist = harmonysearch(change_list)

    # midi 생성
    # 입력 값 : 음표 리스트
    # 리턴 값 : midi
    midicreate(harmolist)


##########      def 모음    ###################


#pdf to png
def pdftopng(pdfpath):

    #pdffile = ".vscode//12.pdf"
    doc = fitz.open(pdfpath)
    zoom=3
    for i in range(len(doc)):
        page = doc.loadPage(i)
        mat = fitz.Matrix(zoom, zoom)
        pix = page.getPixmap(matrix = mat)
        output = f".vscode//outfile{i}.png"
        pix.writePNG(output)
        
    return len(doc)



#가존 코드와 바꿀 코드의 차이
def transpose(base, change):
    if base == 'C':
        base = 1
    elif base == 'C#':
        base = 2
    elif base == 'D':
        base = 3
    elif base == 'D#':
        base = 4
    elif base == 'E':
        base = 5
    elif base == 'F':
        base = 6
    elif base == 'F#':
        base = 7
    elif base == 'G':
        base = 8
    elif base == 'G#':
        base = 9
    elif base == 'A':
        base = 10
    elif base == 'A#':
        base = 11
    elif base == 'B':
        base = 12
    else:
        print("잘못 입력 하셨습니다.")

    if change == 'C':
        change = 1
    elif change == 'C#':
        change = 2
    elif change == 'D':
        change = 3
    elif change == 'D#':
        change = 4
    elif change == 'E':
        change = 5
    elif change == 'F':
        change = 6
    elif change == 'F#':
        change = 7
    elif change == 'G':
        change = 8
    elif change == 'G#':
        change = 9
    elif change == 'A':
        change = 10
    elif change == 'A#':
        change = 11
    elif change == 'B':
        change = 12
    else:
        print("잘못 입력 하셨습니다.")
    gap = change - base
    return gap

# 오선 좌표구하는 함수, 입력 값 : 이미지 경로 , 출력 값 : 오선 좌표 리스트
def detect_staff(imagepath):
    img = cv2.imread(imagepath,cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #테스트용인 곰세마리는 임계값 230으로 해야 다 뽑힌다. 그래서 230으로 테스트
    ret, dst = cv2.threshold(gray, 220,255,cv2.THRESH_BINARY)#ret에는 임계값이 저장
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

# 오선 비율 확인
def averge_rate_staff(stafflist):
    gaplist=[]

    for i in range(int(len(stafflist)/5)):
        for j in range(4):
            gaplist.append((stafflist[5*i+j+1]-stafflist[5*i+j]))

    #print(gaplist)
    averagegap = sum(gaplist)/len(gaplist)
    #print(averagegap)
    rate = standard_detect_gap/averagegap
    round(rate,3)

    return rate

#악보 이미지 리사이즈
def resize_image(imgpaht, rate):
    img_source = cv2.imread(imgpaht,0)
    resize_img_path = '.vscode//resizeaa.png'
    #이미지 변환
    img_result = cv2.resize(img_source, None, fx=rate, fy=rate, interpolation = cv2.INTER_CUBIC)
    cv2.imwrite(resize_img_path,img_result)
    
    return resize_img_path


#악보 오선으로 이미지 자르기
def dividescore(resize_img_path,resize_stafflist):
    copylist=[]

    img_rgb = cv2.imread(resize_img_path, 0) 
    img_rgb2 = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2RGB)
    img_gray = cv2.imread(resize_img_path, cv2.COLOR_BGR2GRAY)
    w,h = img_gray.shape[::-1]

    for i in range(int(len(resize_stafflist)/5)):
        img_copy = img_rgb2.copy() 
        img_copy = img_rgb2[resize_stafflist[i*5]-40:resize_stafflist[i*5+4]+40,0:w-1]
        img_copy= cv2.cvtColor(img_copy,cv2.COLOR_BGR2GRAY)
        copylist.append(img_copy)
    
    return copylist


# 이어져 있는 8,16음표 찾기
def checklink(divide_img):
    #img_rgb = cv2.imread(divide_img, 0) 
    #img_rgb2 = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2RGB)
    #img_gray = cv2.imread(divide_img, cv2.COLOR_BGR2GRAY)
    w,h = divide_img.shape[::-1]
    #print(w,h)

    kernel_size_row = 4
    kernel_size_col = 4
    kernel = np.ones((4, 4), np.uint8)
    alllist = []
    #print(resize_stafflist)
    #copylist = []
    dilate_image = cv2.dilate(divide_img, kernel, iterations=1)
    ret, dst = cv2.threshold(dilate_image, 180,255,cv2.THRESH_BINARY)#ret에는 임계값이 저장
    #copylist.append(dst)
    #copylist.append(dilate_image)
    #cv2.imshow("test",dst)
    #cv2.waitKey()
    test_w,test_h = dst.shape[::-1]
    #print(test_w,test_h)
    eightlist=[]
    eightlist.append([])
    n=0

    #8분16분 음표 좌표 모두 찾기
    for t_h in range(test_h):       
        for t_w in range(test_w):
            c=1
            k=1
            t=0
            px = dst[t_h,t_w]
            if(px==0):
                #print(px)
                while(c==1):
                    npx=dst[t_h+t,t_w+k]
                    #print(npx)
                    if(npx==0):
                        k=k+1
                    else:
                        if(dst[t_h+3,t_w+k] == 0):
                            t=t+3
                        elif(dst[t_h-3,t_w+k] == 0):
                            t=t-3
                        else:
                            ck=0
                            if(k>23):
                                #cv2.line(img_copy2,(t_w,t_h),(t_w+k,t_h),(0,0,255),1) 
                                eightlist[n].append(t_w)
                                eightlist[n].append(t_w+k)
                                eightlist[n].append(t_h)
                                eightlist.append([])
                                n=n+1
                            break
        
    del eightlist[len(eightlist)-1]
    #eightlist=list(set(eightlist))

    #정렬
    eightlist.sort(key=itemgetter(2))
    eightlist.sort(key=itemgetter(1))
    eightlist.sort(key=itemgetter(0))
        
    #필터링 구현 중

    testremove = []
    testremove2 = []
    for i in range(len(eightlist)-1):
        for j in range(i+1,len(eightlist)):
            if(abs(eightlist[i][0] - eightlist[j][0])<6 and abs(eightlist[i][2] - eightlist[j][2])<6 and abs(eightlist[i][0]-eightlist[i][1]) <= abs(eightlist[j][0]-eightlist[j][1])):
                testremove.append(i)
                break

    testremove.sort()
    #print(testremove)
    for i in reversed(range(len(testremove))):
        del eightlist[testremove[i]]

    #print("eightlist : ",eightlist)
    #print("eightlist 갯수: ",len(eightlist))
    for i in range(len(eightlist)-1):
        for j in range(i+1,len(eightlist)):
            if(abs(eightlist[i][0] - eightlist[j][0])<6 and abs(eightlist[i][2] - eightlist[j][2])<6 and abs(eightlist[i][0]-eightlist[i][1]) >= abs(eightlist[j][0]-eightlist[j][1])):
                testremove2.append(j)
                break
    #print("testremove2",testremove2)
    #print("testremove2 갯수 ",len(testremove2))
    testremove2.sort()
    for i in reversed(range(len(testremove2))):
        #print(testremove2[i])
        del eightlist[testremove2[i]]

    #print(len(eightlist))
    #print(eightlist)

    #img_copy2 = cv2.cvtColor(divide_img,cv2.COLOR_BGR2RGB)
    for i in range(len(eightlist)):
        eightlist[i][0] = eightlist[i][0] - 20
        eightlist[i][1] = eightlist[i][1] + 10
        #cv2.line(img_copy2,(eightlist[i][0]-20,eightlist[i][2]),(eightlist[i][1],eightlist[i][2]),(0,0,255))
        alllist.append(eightlist[i])

    del eightlist
    
    #cv2.imshow("test",img_copy2)
    #cv2.waitKey()
    
    return alllist


# 탬플릿 매칭
def template_note_list(divide_img, temlist,divide):
    

    #img_rgb = cv.imread('.vscode\score4.png', 0) 
    #img_rgb = cv2.imread(imgpath, 0) 
    #img_gray = cv2.imread(imgpath, cv2.COLOR_BGR2BGRA)
    ret, dst = cv2.threshold(divide_img,100,255,cv2.THRESH_BINARY)
    #x = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
    img_rgb2 = cv2.cvtColor(divide_img, cv2.COLOR_RGB2BGR)

    if(divide == '음표'):
        threshold = 0.68
    elif(divide == 1):
        threshold = 0.9
    elif(divide == 1/2):
        threshold = 0.9
    elif(divide == 1/4):
        threshold = 0.75
    elif(divide == 1/8):
        threshold = 0.8
        
    xylist=[]
    xylist.append([])
    i=0
    for image in temlist:
        template = cv2.imread(image,0)
        ret1, dst1 = cv2.threshold(template,100,255,cv2.THRESH_BINARY)
        #template_gray = cv.cvtColor(dst1,cv.COLOR_BGR2RGB)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(dst,template,cv2.TM_CCOEFF_NORMED) #0.6<x< 0.65
        #res = cv.matchTemplate(x,dst1,cv.TM_CCOEFF_NORMED) #0.6<x< 0.65 
        #threshold = 0.68
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):

            #테스트 확인용
            #cv2.rectangle(img_rgb2, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
            #cv2.line(img_gray,(pt[0],pt[1]),(pt[0]+10,pt[1]),(0,0,255),1)
            #print(pt, (pt[0] + w, pt[1] + h))
            #print(pt[0])

            xylist[i].append(pt[0])
            xylist[i].append(pt[1])
            if(divide != '음표'):
                xylist[i].append(divide)
                xylist[i].append('Rest')
            xylist.append([])
            i=i+1
    #빈 리스트 삭제
    del xylist[len(xylist)-1]

    num=len(xylist)
    xylist.sort(key=itemgetter(1))#y좌표 정렬
    remlist=[]
    k=0

    for i in range(len(xylist)-1):
        for j in range(i+1,len(xylist)):
        #for j in range(len(xylist)-1):
            if abs(xylist[i][0]-xylist[j][0])<5 and abs(xylist[i][1]-xylist[j][1])<5 :
                remlist.append(i)
    #if abs(xylist[len(xylist)-1][0]-xylist[len(xylist)][0])<5 and abs(xylist[len(xylist)-1][1]-xylist[len(xylist)][1])<5 :
        #remlist.append(i)
    
    #오선 위에 있는 값 제거
    '''
    for i in range(len(xylist)):
        if(xylist[i][1]<2*stafflist[0]-stafflist[4]):
            remlist.append(i)
    '''
    

    remlist=list(set(remlist))
    remlist.sort()
    remnum=len(remlist)-1

    #중복 좌표 제거
    for i in range(remnum, -1, -1):
        del xylist[remlist[i]]

    num = len(xylist)-1
    #y좌표를 오름차순으로 정렬
    xylist.sort(key=itemgetter(1))
    
    #테스트 확인
    '''
    stave = ['.vscode//stave1.png','.vscode//stave2.png','.vscode//stave3.png','.vscode//stave4.png']
    stavelist =[]
    stavelist.append([])
    i=0
    for image in stave:
        template = cv2.imread(image,0)
        ret1, dst1 = cv2.threshold(template,100,255,cv2.THRESH_BINARY)
        #template_gray = cv.cvtColor(dst1,cv.COLOR_BGR2RGB)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(dst,template,cv2.TM_CCOEFF_NORMED) #0.6<x< 0.65
        #res = cv.matchTemplate(x,dst1,cv.TM_CCOEFF_NORMED) #0.6<x< 0.65 
        #threshold = 0.68
        loc = np.where( res >= 0.85)
        for pt in zip(*loc[::-1]):

            #테스트 확인용
            cv2.rectangle(img_rgb2, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            #print(pt)
            #print(stavelist)
            #print(i)
            stavelist[i].append(pt[0])
            stavelist[i].append(pt[1])
            stavelist.append([])
            i=i+1
    #빈 리스트 삭제
    del stavelist[len(stavelist)-1]
    '''

    #cv2.imshow("result",img_rgb2)
    #cv2.imwrite('.vscode//stavetest.png',img_rgb2)
    #cv2.waitKey()
    
    #print(xylist)

    return xylist


#8,16 박자 변환
def change_tempolist(notelist, chlist):
    #print("notelist : ",notelist)

    #print("확인 : ",chlist)
    #print("수 : ",len(chlist))
    for s in range(len(chlist)-1):
        if(chlist[s+1][0]-chlist[s][0]<3):
            chlist[s].append(1/16)
            if(chlist[s+1][1]-chlist[s][1]<3):
                chlist[s+1].append(1/16)
            else:
                chlist[s+1].append(1/8)
        else:
            chlist[s].append(1/8)
            #print(s,len(chlist)-1)
            if(s==len(chlist)-2):
                chlist[s+1].append(1/8)

    

    for i in reversed(range(len(chlist))):
        for x in range(len(notelist)):
            if(chlist[i][0]<notelist[x][0]<chlist[i][1]):
                notelist[x][2]=chlist[i][3]

    #print("change_list : ",chlist)
    print("notelist : ",notelist)

    return notelist

    
        
    



#음계 설정
def note_scale(staff_list,notelist):
    i=0
    gap=6.5
    #print(staff_list)
    #scale_list = []
    #print(staff_list)
    #print(notelist)
    #print(start_list)
    #print(len(start_list))

    for y in range(len(notelist)):
        if(staff_list[i]-gap*4.5<notelist[y][1]<staff_list[i]-gap*3.5):
            notelist[y].insert(4,23)#멜로디 시 B5

        elif(staff_list[i]-gap*3.5<notelist[y][1]<staff_list[i]-gap*2.5):
            notelist[y].insert(4,21)#멜로디 라 A5

        elif(staff_list[i]-gap*2.5<notelist[y][1]<staff_list[i]-gap*1.5):
            notelist[y].insert(4,19)#멜로디 솔 G5

        elif(staff_list[i]-gap*1.5<notelist[y][1]<staff_list[i]-gap/2):
            notelist[y].insert(4,17)#멜로디 파 F5

        elif(staff_list[i]-gap/2<notelist[y][1]<staff_list[i]+gap/2):
            #print("1미",notelist[y][1],staff_list[5*i])
            #scale_list.append("1미")
            notelist[y].insert(4,16)#멜로디 미 E5
        
        elif(staff_list[i]+gap/2<notelist[y][1]<staff_list[i+1]-gap/2):
            #print("1레",notelist[y][1],staff_list[5*i]+gap)
            #scale_list.append("1레")
            notelist[y].insert(4,14)#멜로디 레 D5

        elif(staff_list[i+1]-gap/2<notelist[y][1]<staff_list[i+1]+gap/2):
            #print("1도",notelist[y][1],staff_list[5*i+1])
            #scale_list.append("1도")
            notelist[y].insert(4,12) #멜로디 도 C5

        elif(staff_list[i+1]+gap/2<notelist[y][1]<staff_list[i+2]-gap/2):
            #print("2시",notelist[y][1],staff_list[5*i+1]+gap)
            #scale_list.append("2시")
            notelist[y].insert(4,11)#멜로디 시 B4

        elif(staff_list[i+2]-gap/2<notelist[y][1]<staff_list[i+2]+gap/2):
            #print("2라",notelist[y][1],staff_list[5*i+2])
            #scale_list.append("2라")
            notelist[y].insert(4,9)#멜로디 라 A4

        elif(staff_list[i+2]+gap/2<notelist[y][1]<staff_list[i+3]-gap/2):
            #print("2솔",notelist[y][1],staff_list[5*i+2]+gap)
            #scale_list.append("2솔")
            notelist[y].insert(4,7)#멜로디 솔 G4

        elif(staff_list[i+3]-gap/2<notelist[y][1]<staff_list[i+3]+gap/2):
            #print("2파",notelist[y][1],staff_list[5*i+3])
            #scale_list.append("2파")
            notelist[y].insert(4,5)#멜로디 파 F4

        elif(staff_list[i+3]+gap/2<notelist[y][1]<staff_list[i+4]-gap/2):
            #print("2미",notelist[y][1],staff_list[5*i+3]+gap)
            #scale_list.append("2미")
            notelist[y].insert(4,4)#멜로디 미 E4

        elif(staff_list[i+4]-gap/2<notelist[y][1]<staff_list[i+4]+gap/2):
            #print("2레",notelist[y][1],staff_list[5*i+4])
            #scale_list.append("2레")
            notelist[y].insert(4,2)#멜로디 레 D4

        elif(staff_list[i+4]+gap/2<notelist[y][1]<staff_list[i+4]+gap*1.5):
            #print("2도",notelist[y][1],staff_list[5*i+4]+gap)
            #scale_list.append("2도")
            notelist[y].insert(4,0)#멜로디 도 C4
        
        elif(staff_list[i+4]+gap*1.5<notelist[y][1]<staff_list[i+4]+gap*2.5):
            notelist[y].insert(4,-1)#멜로디 시 B3
        
        elif(staff_list[i+4]+gap*2.5<notelist[y][1]<staff_list[i+4]+gap*3.5):
            notelist[y].insert(4,-3)#멜로디 라 A3
        
        elif(staff_list[i+4]+gap*3.5<notelist[y][1]<staff_list[i+4]+gap*4.5):
            notelist[y].insert(4,-5)#멜로디 솔 G3

        else:
            notelist[y].insert(4,"미확인")
    
    return notelist

# 음계 변환
def changescale(scalelist,transgap):
    
    for i in range(len(scalelist)):
        scalelist[i].append(1)
        if(scalelist[i][3]!='Rest'):
            #print(scalelist[i][3])
            scalelist[i][3]=scalelist[i][3]+transgap
            
    #print(scalelist)
    return scalelist

#화음 체크
def harmonysearch(notelist):

    for i in range(len(notelist)):
        num = 1

        if(notelist[i][5] == 0):
            continue
        
        for ck in range(1,5):
            
            if(i+ck >= len(notelist)-1):
                if(notelist[i+ck-1][5] != 1):
                    notelist[i+ck][5] = 0
                    break
                
                else:
                    break
            
            if(abs(notelist[i][0]-notelist[i+ck][0])<3):
                num = num + 1
                notelist[i][5]=num
                notelist[i+ck][5]=0
                
            else:
                notelist[i][5] = num
                break
    #print(notelist)
    return notelist


#midi 생성
def midicreate(notelist):
    #change_list=[8,5,6,'Rest',1,3]
    #tempo_list=[1/2,1/2,1/4,1/4,1/2,1/2]
#0  1  2  3  4  5  6  7  8  9  10  11
#C  C# D  D# E  F  F# G  G# A  A#  B

    NoteList = []
    #print(notelist)
    for i in range(len(notelist)):
        #print(notelist[i][2],notelist[i][3],notelist[i][5])
        if(notelist[i][3]=='Rest'):
            chord = Rest(notelist[i][2])
        elif(notelist[i][5]==0):
            continue
        elif(notelist[i][5]==2):
            chord = NoteSeq([Note(notelist[i][3],dur=notelist[i][2]),Note(notelist[i+1][3],dur=notelist[i][2])])
        elif(notelist[i][5]==3):
            chord = NoteSeq([Note(notelist[i][3],dur=notelist[i][2]),Note(notelist[i+1][3],dur=notelist[i][2]),Note(notelist[i+2][3],dur=notelist[i][2])])
        elif(notelist[i][5]==4):
            chord = NoteSeq([Note(notelist[i][3],dur=notelist[i][2]),Note(notelist[i+1][3],dur=notelist[i][2]),Note(notelist[i+2][3],dur=notelist[i][2]),Note(notelist[i+3][3],dur=notelist[i][2])])
        else:
            chord = NoteSeq([Note(notelist[i][3],dur=notelist[i][2])])
        

        NoteList.append(chord)

        #else:
            #NoteList.append(Rest(notelist[i][2]))

    print(NoteList)
    #seq = NoteSeq(NoteList)
        
    #midi = Midi(number_tracks=2, tempo=90)
    #midi.seq_notes(NoteList, track=0)
    #midi.seq_notes(notes2, track=0)
    midi = Midi(1, tempo=60)
    midi.seq_chords(NoteList, track=0)
    midi.write(".vscode//demotest.mid")

#main

pdfpath = '.vscode//1.pdf'   
#imgpath = '.vscode//12-1.png'
#note_search(imgpath)

num = pdftopng(pdfpath)

for i in range(num):
    imgpath = f'.vscode//outfile{i}.png'
    note_search(imgpath)