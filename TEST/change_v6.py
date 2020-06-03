<<<<<<< HEAD
=======
#f_demo.py
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
import socketserver
from os.path import exists
from pyknon.genmidi import Midi
from pyknon.music import NoteSeq, Note, Rest

<<<<<<< HEAD
import os
=======
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
import cv2
import numpy as np
import copy
from matplotlib import pyplot as plt
from operator import itemgetter
<<<<<<< HEAD
import operator
=======
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
import pdb
import fitz
import tensorflow.keras
from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join
<<<<<<< HEAD

=======
from operator import itemgetter
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4

standard_detect_gap = 13

HOST = ''
<<<<<<< HEAD
PORT = 9300
=======
PORT = myport
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
Base=''
Change=''
#//home//ec2-user//test//socket_test//test.txt
class MyTcpHandler(socketserver.BaseRequestHandler):
    
    '''def init_base(self,base):
        self.base = base
    def init_change(self,change):
        self.change = change'''
        

    def handle(self):
        global Base
        global Change
        data_transferred = 0
        print('연결됨')
        #basecode = self.request.recv(1024)
        #print("1 : ",basecode)
        #basecode = basecode.decode()
        #changecode = self.request.recv(1024)
        #print("2 : ",changecode)
        #changecode = changecode.decode()
        basecode = ['bC','bD','bE','bF','bG','bA','bB']  #기존악보 코드 - bC는 basecode[0]
        changecode = ['cC','cD','cE','cF','cG','cA','cB'] #바꿀악보 코드

        code = ['C','D','E','F','G','A','B']

<<<<<<< HEAD

        filename = self.request.recv(2048)
        #print("1 : ",filename) #파일 잘 들어왔는지 확인
        ########################
        #print(filename)
        
        filename = filename.decode()
        filename2 = self.request.recv(2048)
        filename2 = filename2.decode()

        filename = filename + filename2
        print(filename)
=======
        filename = self.request.recv(1024)
        print("1 : ",filename) #파일 잘 들어왔는지 확인
        filename = filename.decode()
        #print(filename)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4

        #filename의 첫번째는 기존악보 코드가 무엇인지 저장됨
        if filename in basecode:
            #index함수로
            num = basecode.index(filename) 
            #basecode로 code의 원소중 몇번째 원소를 받아온건지 확인(0 1 2 순서임)
<<<<<<< HEAD
            #print(code[num])
=======
            print(code[num])
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
            Base = code[num] 
            #init_base(code[num])
            #print(self.base)

        
        #filename의 두번째는 새로운악보 코드가 무엇인지 저장됨
        elif filename in changecode:
            #index함수로
            num = changecode.index(filename)
            #changecode code의 원소중 몇번째 원소를 받아온건지 확인(0 1 2 순서임)
<<<<<<< HEAD
            #print(code[num])
=======
            print(code[num])
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
            Change = code[num]
            #init_change(code[num])
            #print(self.change)
    
        else:#pdf 이름이 들어올 때 여기서 filename == pdf이름
            if not exists('/home/ec2-user/Ourchord/PDF/'+filename):
                print('못찾음')
                return

            else:
                pdfpath ='/home/ec2-user/Ourchord/PDF/'+filename
                
            num = pdftopng(pdfpath)

            for i in range(num):
                imgpath = f'/home/ec2-user/Ourchord/PDF/pdf/filename{i}.png' # ---------------------------------------------------- 경로 수정
                #imgpath = f'.vscode//outfile{i}.png'
<<<<<<< HEAD
                #
                name = filename.replace('.pdf',"")
                
                print(name)
                print("notesearch base,change",Base,Change,filename)
                note_search(imgpath,Base,Change,name)
=======
                print("notesearch base,change",Base,Change)
                note_search(imgpath,Base,Change)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
                #tempo_classfication()


            '''
            print('전송 시작')
            print('/home/ec2-user/Ourchord/PDF/',filename)
            #주석처리
            with open('/home/ec2-user/Ourchord/PDF/'+filename, 'rb') as f:
                try:
                    data = f.read(1024)
                    while data:
                        data_transferred += self.request.send(data)
                        data=f.read(1024)

                except Exception as e:
                    print(e)
            '''
            print('전송 완료')


def runServer():
    print('서버 시작')

    try:
        server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)
<<<<<<< HEAD
        #print("반복")
=======
        print("반복")
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
        server.serve_forever()
    except KeyboardInterrupt:
        print('파일 서버를 종료합니다')

#main함수랑 def통합해놓은거 복붙

<<<<<<< HEAD
#음표 좌표 추출
def note_search(imgpath,base,change,name):
    #img_rgb = cv2.imread('.vscode\score4.png', 0) 
    
=======

#음표 좌표 추출
def note_search(imgpath,base,change):
    #img_rgb = cv2.imread('.vscode\score4.png', 0) 
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    print("base,change",base,change)
    #테스트 조 설정
    #base='G#'
    #change='C'
    print("note search start",base,change)
    transegap = transpose(base,change)
<<<<<<< HEAD
    #print(transegap)
=======
    print(transegap)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4


    stafflist = detect_staff(imgpath)
    #print("stafflist : ",stafflist)
    reszie_rate=averge_rate_staff(stafflist)
    #print("resize_rate : ",reszie_rate)
<<<<<<< HEAD
    resize_img_path =resize_image(imgpath,reszie_rate)
=======
    resize_img_path =resize_image(imgpath,reszie_rate) #imgpath: png로 변환된 pdf악보 이미지 사이즈 변경
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    resize_stafflist = detect_staff(resize_img_path)
    #print("resize_stafflist",resize_stafflist)

    img_rgb = cv2.imread(resize_img_path, 0) 
    img_rgb2 = cv2.imread(resize_img_path, 0)
    img_gray = cv2.imread(resize_img_path, cv2.COLOR_BGR2GRAY)
    
    # ---------------------------------------------------- 경로 수정
    #notelists: tem_empty, tem_full: 기존-6, 4 --> 5, 5
    #/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_1~5.png
    #/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_1~5.png
    notelists = ['/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_1.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_2.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_3.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_4.png',
<<<<<<< HEAD
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_5.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_6.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_7.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_1.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_2.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_3.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_4.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_5.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_6.png']#empty, full png경로
=======
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_1.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_2.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_3.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_4.png']#empty, full png경로
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    eightrest=['/home/ec2-user/Ourchord/NOTE/rest/eightrest/eight.png'] #8분쉼표
    quarterrest=['/home/ec2-user/Ourchord/NOTE/rest/quarterrest/quarter.png'] #4분쉼표
    halfrest=['/home/ec2-user/Ourchord/NOTE/rest/halfrest/half.png'] #2분쉼표
    wholerest=['/home/ec2-user/Ourchord/NOTE/rest/wholerest/whole.png'] #온쉼표
    # ---------------------------------------------------- 경로 수정
<<<<<<< HEAD
=======
    '''
    notelists = ['.vscode//qu1.png','.vscode//qu2.png','.vscode//qu3.png','.vscode//qu4.png','.vscode//qu5.png','.vscode//qu6.png','.vscode//ha1.png','.vscode//ha2.png','.vscode//ha3.png','.vscode//ha4.png']#나중 DB 경로로 수정
    eightrest=['.vscode//eightrest.png']
    quarterrest=['.vscode//quarterrest.png']
    halfrest=['.vscode//halfrest.png']
    wholerest=['.vscode//wholerest.png']'''

>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4

    notevalue = '음표'
    eightvalue = 1/8
    quartervalue = 1/4
    halfvalue = 1/2
    wholevalue = 1
    #8분 쉼표 0.8
    #4분 쉼표 0.75
    #2분,온쉼표 0.9 이상

<<<<<<< HEAD
    
=======
    xylist = template_note_list(resize_img_path,notelists,notevalue,resize_stafflist)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    eightlist = template_note_list(resize_img_path,eightrest,eightvalue,resize_stafflist)
    #print("8분 : ",eightlist)
    quarterlist = template_note_list(resize_img_path,quarterrest,quartervalue,resize_stafflist)
    #print("4분 : ",quarterlist)
    halflist = template_note_list(resize_img_path,halfrest,halfvalue,resize_stafflist)
    #print("2분 : ",halflist)
    wholelist = template_note_list(resize_img_path,wholerest,wholevalue,resize_stafflist)
    #print("온 : ",wholelist)
<<<<<<< HEAD
    xylist = template_note_list(resize_img_path,notelists,notevalue,resize_stafflist)
=======
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4

    restlist = eightlist+quarterlist+halflist
    #print("전체 : ",restlist)
    #print("xylist : ",xylist)
    #print(xylist)
    #print(len(xylist))
    
    staff_average_line = line_average(resize_stafflist)
    #print("staff_average_line : ",staff_average_line)
    
    startlist=start_list(staff_average_line,xylist)
    
<<<<<<< HEAD

    note_image(xylist,resize_stafflist,resize_img_path)

    tempolist = tempo_classfication(xylist)
    #print("startlist : ",startlist)
    #print("test",startlist)
    
=======
    #print("startlist : ",startlist)
    #print("test",startlist)

    
    
    note_image(xylist,resize_stafflist,resize_img_path)

    tempolist = tempo_classfication(xylist)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    #박자 딥러닝 하기전 테스트
    #for i in range(len(xylist)):
    #    xylist[i].append(1/4)
    #print(xylist)
    scale_note_list = note_scale(resize_stafflist,xylist,startlist)
<<<<<<< HEAD
    note_list = scale_note_list + restlist

    note_list.sort(key=itemgetter(1))
    #print(note_list)
    sort_list=sort_staff_note(staff_average_line,note_list)
    
=======

    note_list = scale_note_list + restlist

    note_list.sort(key=itemgetter(1))
    sort_list=sort_staff_note(staff_average_line,note_list)
    
    print(sort_list)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    #list -> [x,y,박자,음계,오선번째]

    change_list=changescale(sort_list,transegap)

    '''
    for i in range(len(change_list)):
        print(f"{i}번째 :", change_list[i][3])
    '''
    
    #print(change_list)

    #midi 생성
<<<<<<< HEAD
    midicreate(change_list,name)
=======
    midicreate(change_list)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4


    #테스트 좌표
    #stafflist = [323, 335, 349, 362, 375, 588, 600, 614, 626, 640, 856, 868, 882, 895, 907]
    #04/26 테스트중 주석처리함
<<<<<<< HEAD
    
    


def template_note_list(imgpath, temlist,divide,stafflist):
    #img_rgb = cv.imread('.vscode\score4.png', 0) 
    img_rgb = cv2.imread(imgpath, 0)
    #테스트 확인용
    #img_gray = cv2.imread(imgpath,cv2.COLOR_RGB2BGR)
    img_gray = cv2.imread(imgpath,cv2.COLOR_RGB2BGR)
    #img_gray2 = cv2.imread('.vscode//checkre.png',cv2.COLOR_RGB2BGR)
    #img_gray3 = cv2.cvtColor(img_gray2,cv2.COLOR_RGB2BGR)

=======
    #note_image(xylist,resize_stafflist,resize_img_path)


def template_note_list(imgpath, temlist, divide, stafflist):
    #img_rgb = cv.imread('.vscode\score4.png', 0) 
    img_rgb = cv2.imread(imgpath, 0) 
    img_gray = cv2.imread(imgpath, cv2.COLOR_BGR2BGRA)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    ret, dst = cv2.threshold(img_gray,100,255,cv2.THRESH_BINARY)
    #x = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
    img_rgb2 = cv2.imread(imgpath, cv2.COLOR_BGR2GRAY)

    if(divide == '음표'):
        threshold = 0.68
    elif(divide == 1):
<<<<<<< HEAD
        threshold = 0.89
    elif(divide == 1/2):
        threshold = 0.9
    elif(divide == 1/4):
        threshold = 0.75
=======
        threshold = 0.9
    elif(divide == 1/2):
        threshold = 0.9
    elif(divide == 1/4):
        threshold = 0.68
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    elif(divide == 1/8):
        threshold = 0.8
        

    #lists = ['.vscode//qu1.png','.vscode//qu2.png','.vscode//qu3.png','.vscode//qu4.png','.vscode//qu5.png','.vscode//qu6.png','.vscode//ha1.png','.vscode//ha2.png','.vscode//ha3.png','.vscode//ha4.png']#나중 DB 경로로 수정
    #lists = ['.vscode//quarterrest.png','.vscode//eighthrest.png','.vscode//pointhalfrest.png','.vscode//halfrest.png','.vscode//wholerest.png']
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
<<<<<<< HEAD
            #cv2.rectangle(img_gray2, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
=======
            #cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
            
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
<<<<<<< HEAD
 
=======

>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
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
    for i in range(len(xylist)):
        if(xylist[i][1]<2*stafflist[0]-stafflist[4]):
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
<<<<<<< HEAD
    #print("xylist",xylist)
    #테스트용
    img_gray3 = cv2.cvtColor(img_gray,cv2.COLOR_RGB2BGR)
    for i in range(len(xylist)):
        cv2.rectangle(img_gray3, (xylist[i][0],xylist[i][1]), (xylist[i][0]+w,xylist[i][1]+h), (0,0,255), 2)
    cv2.imwrite('/home/ec2-user/Ourchord/PDF/pdf/testnotesearch.png',img_rgb2) 
    #cv2.imshow("result",img_gray)
    #cv2.imwrite(".vscode//checkre.png",img_gray3)
=======
    #cv2.imshow("result",img_gray)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    #cv2.waitKey()
    return xylist

def note_image(xylist,stafflist,image_path):

    img_rgb = cv2.imread(image_path, 0) 
    img_rgb2 = cv2.imread(image_path, 0) 
<<<<<<< HEAD
=======
    #print("xylist", xylist)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    #테스트 오선 없는 것
    #img_white = cv2.imread('.vscode/whiteimg.png',0)
    num = len(xylist)
    #y좌표를 오름차순으로 정렬
    xylist.sort(key=itemgetter(1))
<<<<<<< HEAD
    m=1
    #print(stafflist)
=======
    #m=1
    print(stafflist)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    staffnum = int(len(stafflist)/5)
    updownlist = []
    #밑에 음표 자르는 부분 def 로 변환 필요
    for i in range(num):
        #testcopy = img_rgb.copy()
        for j in range(0,staffnum*2):
            if(j%2 == 0):
                if(xylist[i][1]<stafflist[5*int(j/2)+2]):
                    updownlist.append("down")
                    #print(f"{m}번째 : ", xylist[i][0],xylist[i][1], updownlist[i])
                    cv2.rectangle(img_rgb2, (xylist[i][0]-2,xylist[i][1]-3), (xylist[i][0] + 31, xylist[i][1] + 60), (0,0,255), 1)
                    testcopy = img_rgb[xylist[i][1]-3:xylist[i][1]+60, xylist[i][0]-2:xylist[i][0]+31]
<<<<<<< HEAD
=======
                    #딥러닝 시킨 파일과 현재 악보 음표의 박자 구분 확인을 위한 꼬리부분 png저장
                    
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
                    cv2.imwrite(f'/home/ec2-user/Ourchord/PDF/pdf/note/{i}.png',testcopy)    # ---------------------------------------------------- 경로 수정
                    break
            else:
                if(xylist[i][1]<stafflist[5*int(j/2)+4]+20):
                    updownlist.append("up")
                    #print(f"{m}번째 : ", xylist[i][0],xylist[i][1], updownlist[i])
                    cv2.rectangle(img_rgb2, (xylist[i][0]-2,xylist[i][1]-48), (xylist[i][0] + 31, xylist[i][1] + 15), (0,0,255), 1)
                    testcopy = img_rgb[xylist[i][1]-48:xylist[i][1]+15, xylist[i][0]-2:xylist[i][0]+31]
                    cv2.imwrite(f'/home/ec2-user/Ourchord/PDF/pdf/note/{i}.png',testcopy)    # ---------------------------------------------------- 경로 수정
                    break
        #cv.rectangle(img_rgb2, (xylist[i][0]-2,xylist[i][1]-48), (xylist[i][0] + 31, xylist[i][1] + 15), (0,0,255), 1)
        #print(f"{m}번째 : ", xylist[i][0],xylist[i][1], updownlist[i])
        #testcopy = img_rgb[xylist[i][1]:xylist[i][1]+18, xylist[i][0]:xylist[i][0]+13]
        #cv2.imwrite(f'.vscode\stest{i}.png',testcopy) #추후 DB저장으로 수정
<<<<<<< HEAD
        m=m+1

    #print("갯수", len(updownlist))
=======
        #m=m+1

    print("갯수", len(updownlist))
    #cv2.imwrite('.vscode//testnotesearch.png',img_rgb2)    # ---------------------------------------------------- 경로 수정
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    cv2.imwrite('/home/ec2-user/Ourchord/PDF/pdf/testnotesearch.png',img_rgb2) 
    #cv2.waitKey(0)

# 오선 비율 확인
def averge_rate_staff(stafflist):
    gaplist=[]

    for i in range(int(len(stafflist)/5)):
        for j in range(4):
            #print((staff[5*i+j+1],staff[5*i+j]))
            gaplist.append((stafflist[5*i+j+1]-stafflist[5*i+j]))

<<<<<<< HEAD
    #print(gaplist)
    averagegap = sum(gaplist)/len(gaplist)
    #averagegap = round(averagegap,3)
    #print(averagegap)
=======
    print(gaplist)
    averagegap = sum(gaplist)/len(gaplist)
    #averagegap = round(averagegap,3)
    print(averagegap)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    rate = standard_detect_gap/averagegap
    round(rate,3)

    return rate

# 오선 좌표구하는 함수, 입력 값 : 이미지 경로 , 출력 값 : 오선 좌표 리스트
<<<<<<< HEAD
def detect_staff(imagepath):
    img = cv2.imread(imagepath,cv2.IMREAD_COLOR)
=======
def detect_staff(imgpath):
    img = cv2.imread(imgpath,cv2.IMREAD_COLOR)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
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
    
    #이미지로 확인 테스트
    '''
    for i in range(len(staff)):
        cv2.line(gray,(0,staff[i]),(width-10,staff[i]),(0,0,255),1)
    cv2.imshow("rr",gray)
    cv2.imwrite(".vscode//testimg.png",gray)
    cv2.waitKey()
    
    print(len(staff))
    '''
    return staff

def resize_image(imgpaht, rate):
    img_source = cv2.imread(imgpaht,0)
<<<<<<< HEAD
    resize_img_path = '/home/ec2-user/Ourchord/PDF/pdf/resize/renew.png'
=======
    resize_img_path = '/home/ec2-user/Ourchord/PDF/pdf/resize/renew.png' # ---------------------------------------------------- 경로 수정
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    #이미지 변환
    img_result = cv2.resize(img_source, None, fx=rate, fy=rate, interpolation = cv2.INTER_CUBIC)
    #cv2.imshow("x2", img_result)
    #cv2.waitKey()
    cv2.imwrite(resize_img_path,img_result)
    
    return resize_img_path



#오선과 오선 사이 중간값 구하는 것, 활용할지는 보류
def line_average(stafflist):
    checkrange = []
    #print(stafflist)
    #print(len(stafflist))
    staffnum = len(stafflist)/5
    for i in range(1,int(staffnum)):
        checkrange.append(int((stafflist[5*i]+stafflist[5*i-1])/2))
    
    #gap=checkrange[1]-checkrange[0]+checkrange[len(checkrange)-1]
    gap = stafflist[len(stafflist)-1]+(stafflist[4]-stafflist[0])*2
    
    checkrange.append(gap)
    

    #print(checkrange)
    #checkrangenum = int(len(checkrange))

    return checkrange

def start_list(staff_average,notelist):
    m=0
    num=0
    startlist = []
    for i in range(len(notelist)):
        if(notelist[i][1]>staff_average[m]):
            m=m+1
            if(m==len(staff_average)):
                if(num==0):
                    startlist.append(i)
                    m=len(staff_average)-1
                    num+1
                    break
                else:
                    m=len(staff_average)-1
                    break
            startlist.append(i)
    return startlist

def sort_staff_note(staff_average, notelist):

    m = 0
    num = 1
    for i in range(len(notelist)):
        #print(notelist[i][1],staff_average[m])
        if(notelist[i][1]>staff_average[m]):
            #print(num)
            m=m+1
            num=num+1
            notelist[i].append(num)
        else:
            notelist[i].append(num)
<<<<<<< HEAD
    #print(notelist)
    notelist.sort(key = itemgetter(4,0))
    
=======

    notelist.sort(key = itemgetter(4,0))
    print(notelist)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    #print(notelist)
    return notelist
    '''
    m=0
    num=0
    start_list = []
    for i in range(len(notelist)):
        if(notelist[i][1]>staff_average[m]):
            m=m+1
            if(m==len(staff_average)):
                if(num==0):
                    start_list.append(i)
                    m=len(staff_average)-1
                    num+1
                    break
                else:
                    m=len(staff_average)-1
                    break
            start_list.append(i)
    '''
    
    '''
    #05/07 3차원 배열 -> 2차원 배열로 변경
    m=0
    num=0
    test = []
    line=[]
    #print(start_list)
    for i in range(len(notelist)):
        line.append(notelist[i])
        #print(m)
        if(i>=start_list[m]-1):
            m=m+1
            if(m==len(staff_average)):
                if(num==0):
                    line.sort(key=itemgetter(0))
                    test.append(line)
                    line=[]
                    num=num+1
                    m=len(staff_average)-1
                else:
                    m=len(staff_average)-1
            else:
                line.sort(key=itemgetter(0))
                test.append(line)
                line=[]
<<<<<<< HEAD

=======
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    line.sort(key=itemgetter(0))
    test.append(line)
    print(test)
    '''

    
    #return test

def note_scale(staff_list,notelist,start_list):
    i=0
    gap=6.5
    #print(staff_list)
    #scale_list = []
    #print(staff_list)
    #print(notelist)
    #print(start_list)
    #print(len(start_list))

    for y in range(len(notelist)):
        if(i != len(start_list)):
            if(y==start_list[i]):
                i=i+1

        #print(notelist[y][1],staff_list[5*i],y)
        #pdb.set_trace() 
        #print(f"{y}번째",notelist[y][1],staff_list[5*i],staff_list[5*i+1],staff_list[5*i+2],staff_list[5*i+3],staff_list[5*i+4])
        #print(notelist[y])
        
<<<<<<< HEAD
        if(staff_list[5*i]-gap*6.5<notelist[y][1]<staff_list[5*i]-gap*5.5):
            notelist[y].insert(4,26)#멜로디 레 D5

        elif(staff_list[5*i]-gap*5.5<notelist[y][1]<staff_list[5*i]-gap*4.5):
            notelist[y].insert(4,24)#멜로디 도 C5

        elif(staff_list[5*i]-gap*4.5<notelist[y][1]<staff_list[5*i]-gap*3.5):
=======
        if(staff_list[5*i]-gap*4.5<notelist[y][1]<staff_list[5*i]-gap*3.5):
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
            notelist[y].insert(4,23)#멜로디 시 B5

        elif(staff_list[5*i]-gap*3.5<notelist[y][1]<staff_list[5*i]-gap*2.5):
            notelist[y].insert(4,21)#멜로디 라 A5

        elif(staff_list[5*i]-gap*2.5<notelist[y][1]<staff_list[5*i]-gap*1.5):
            notelist[y].insert(4,19)#멜로디 솔 G5

        elif(staff_list[5*i]-gap*1.5<notelist[y][1]<staff_list[5*i]-gap/2):
            notelist[y].insert(4,17)#멜로디 파 F5

        elif(staff_list[5*i]-gap/2<notelist[y][1]<staff_list[5*i]+gap/2):
            #print("1미",notelist[y][1],staff_list[5*i])
            #scale_list.append("1미")
            notelist[y].insert(4,16)#멜로디 미 E5
        
        elif(staff_list[5*i]+gap/2<notelist[y][1]<staff_list[5*i+1]-gap/2):
            #print("1레",notelist[y][1],staff_list[5*i]+gap)
            #scale_list.append("1레")
            notelist[y].insert(4,14)#멜로디 레 D5

        elif(staff_list[5*i+1]-gap/2<notelist[y][1]<staff_list[5*i+1]+gap/2):
            #print("1도",notelist[y][1],staff_list[5*i+1])
            #scale_list.append("1도")
            notelist[y].insert(4,12) #멜로디 도 C5

        elif(staff_list[5*i+1]+gap/2<notelist[y][1]<staff_list[5*i+2]-gap/2):
            #print("2시",notelist[y][1],staff_list[5*i+1]+gap)
            #scale_list.append("2시")
            notelist[y].insert(4,11)#멜로디 시 B4

        elif(staff_list[5*i+2]-gap/2<notelist[y][1]<staff_list[5*i+2]+gap/2):
            #print("2라",notelist[y][1],staff_list[5*i+2])
            #scale_list.append("2라")
            notelist[y].insert(4,9)#멜로디 라 A4

        elif(staff_list[5*i+2]+gap/2<notelist[y][1]<staff_list[5*i+3]-gap/2):
            #print("2솔",notelist[y][1],staff_list[5*i+2]+gap)
            #scale_list.append("2솔")
            notelist[y].insert(4,7)#멜로디 솔 G4

        elif(staff_list[5*i+3]-gap/2<notelist[y][1]<staff_list[5*i+3]+gap/2):
            #print("2파",notelist[y][1],staff_list[5*i+3])
            #scale_list.append("2파")
            notelist[y].insert(4,5)#멜로디 파 F4

        elif(staff_list[5*i+3]+gap/2<notelist[y][1]<staff_list[5*i+4]-gap/2):
            #print("2미",notelist[y][1],staff_list[5*i+3]+gap)
            #scale_list.append("2미")
            notelist[y].insert(4,4)#멜로디 미 E4

        elif(staff_list[5*i+4]-gap/2<notelist[y][1]<staff_list[5*i+4]+gap/2):
            #print("2레",notelist[y][1],staff_list[5*i+4])
            #scale_list.append("2레")
            notelist[y].insert(4,2)#멜로디 레 D4

        elif(staff_list[5*i+4]+gap/2<notelist[y][1]<staff_list[5*i+4]+gap*1.5):
            #print("2도",notelist[y][1],staff_list[5*i+4]+gap)
            #scale_list.append("2도")
            notelist[y].insert(4,0)#멜로디 도 C4
        
        elif(staff_list[5*i+4]+gap*1.5<notelist[y][1]<staff_list[5*i+4]+gap*2.5):
            notelist[y].insert(4,-1)#멜로디 시 B3
        
        elif(staff_list[5*i+4]+gap*2.5<notelist[y][1]<staff_list[5*i+4]+gap*3.5):
            notelist[y].insert(4,-3)#멜로디 라 A3
        
        elif(staff_list[5*i+4]+gap*3.5<notelist[y][1]<staff_list[5*i+4]+gap*4.5):
            notelist[y].insert(4,-5)#멜로디 솔 G3

        else:
            notelist[y].insert(4,"미확인")
    
    return notelist
<<<<<<< HEAD
=======

>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
# 박자 인식 05/13
def tempo_classfication(xylist) :

    np.set_printoptions(suppress=True)

    # 모델 로드
<<<<<<< HEAD
    model = tensorflow.keras.models.load_model('/home/ec2-user/Ourchord/DEEP/staff_224.h5')
=======
    model = tensorflow.keras.models.load_model('/home/ec2-user/Ourchord/DEEP/no_staff_224_c.h5')
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4

    # 타겟 사이즈 224 X 224 
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    #notelist_path: 음표 꼬리 저장(250,258)
    notelist_path = '/home/ec2-user/Ourchord/PDF/pdf/note/'
    onlyfiles = [f for f in listdir(notelist_path) if isfile(join(notelist_path, f))]
    onlist = []
    for i in range(len(onlyfiles)):
        onlyfiles[i] = onlyfiles[i].replace(".png", "")
        onlyfiles[i] = onlyfiles[i].replace(".PNG", "")
        onlist.append(int(onlyfiles[i]))
    onlist.sort()

    for i in range(len(onlist)):
        onlyfiles[i] = str(onlist[i]) + '.png'

<<<<<<< HEAD
    #print(onlyfiles)

    image = np.empty(len(onlyfiles), dtype = object)
    tempolist = []
    #print("노트개수",len(xylist))
    #print("파일 수",len(onlyfiles))
=======
    print(onlyfiles)

    image = np.empty(len(onlyfiles), dtype = object)
    tempolist = []
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    for item in range(0, len(onlyfiles)) :
        image[item] = Image.open(join(notelist_path+onlyfiles[item])).convert('RGB')
        
        image[item] = image[item].resize((224, 224))
        image[item] = ImageOps.fit(image[item], (224, 224), Image.ANTIALIAS, centering = (0.5, 0.5))

        image_array = np.array(image[item])

        normalized_image_array = (image_array.astype(dtype = np.float32) / 127.0) - 1

        data[0] = normalized_image_array

        prediction = model.predict(data)
<<<<<<< HEAD
        #print(prediction)
        index, value = max(enumerate(prediction[0]), key=operator.itemgetter(1))
        #print(index)
        #print(prediction)
        '''
        if(prediction[0][0] > 0.5):
            xylist[item].append(1/2)
            print(onlyfiles[item]," 사진 : 2분음표")
        elif(prediction[0][1] > 0.5):
            xylist[item].append(1/2)
            print(onlyfiles[item]," 사진 : 2분음표")
        elif(prediction[0][2] > 0.5):
            xylist[item].append(1/4)
            print(onlyfiles[item]," 사진 : 4분음표")
        elif(prediction[0][3] > 0.5):
            xylist[item].append(1/4)
            print(onlyfiles[item]," 사진 : 4분음표")
        elif(prediction[0][4] > 0.5):
            xylist[item].append(1/8)
            print(onlyfiles[item]," 사진 : 8분음표")
        elif(prediction[0][5] > 0.5):
            xylist[item].append(1/8)
            print(onlyfiles[item]," 사진 : 8분음표")
        else:
            xylist[item].append(0)
            print("음표아님",onlyfiles[item])
        '''
        #print(prediction)
        if(index == 0):
            xylist[item].append(1/2)
            print(onlyfiles[item]," 사진 : 2분음표")
        elif(index == 1):
            xylist[item].append(1/2)
            print(onlyfiles[item]," 사진 : 2분음표")
        elif(index == 2):
            xylist[item].append(1/4)
            print(onlyfiles[item]," 사진 : 4분음표")
        elif(index == 3):
            xylist[item].append(1/4)
            print(onlyfiles[item]," 사진 : 4분음표")
        elif(index == 4):
            xylist[item].append(1/8)
            print(onlyfiles[item]," 사진 : 8분음표")
        elif(index == 5):
            xylist[item].append(1/8)
            print(onlyfiles[item]," 사진 : 8분음표")
        else:
            xylist[item].append(0)
            #print("음표아님",onlyfiles[item])
        
    
    #print(xylist)
    #print(len(xylist))
    return xylist        

#가존 코드와 바꿀 코드의 차이
def transpose(base, change):
=======

        if(prediction[0][0] > 0.5):
            xylist[item].append(1/2)
            #print(onlyfiles[item]," 사진 : 2분음표")
        elif(prediction[0][1] > 0.5):
            xylist[item].append(1/2)
            #print(onlyfiles[item]," 사진 : 2분음표")
        elif(prediction[0][2] > 0.5):
            xylist[item].append(1/4)
            #print(onlyfiles[item]," 사진 : 4분음표")
        elif(prediction[0][3] > 0.5):
            xylist[item].append(1/4)
            #print(onlyfiles[item]," 사진 : 4분음표")
        elif(prediction[0][4] > 0.5):
            xylist[item].append(1/8)
            #print(onlyfiles[item]," 사진 : 8분음표")
        elif(prediction[0][5] > 0.5):
            xylist[item].append(1/8)
            #print(onlyfiles[item]," 사진 : 8분음표")
        else:
            xylist[item].append(0)
            print("음표아님")

    #print(xylist)
    #print(len(xylist))
    return xylist


#가존 코드와 바꿀 코드의 차이
def transpose(base, change):
    print("base,chage : ",base, change)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
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

#조변환에 따른 음변환
def changescale(scalelist,transgap):
    
    for i in range(len(scalelist)):
        if(scalelist[i][3]!='Rest'):
<<<<<<< HEAD
            #print(scalelist[i][3])
=======
            print(scalelist[i][3])
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
            scalelist[i][3]=scalelist[i][3]+transgap
    
    return scalelist

#midi 생성
<<<<<<< HEAD
def midicreate(notelist,name):
    

    #for i in range(len(notelist)):
        #print(notelist[i][3],notelist[i][2]) #문제: 음표박자랑 쉼표
    #change_list=[8,5,6,'Rest',1,3]
    #tempo_list=[1/2,1/2,1/4,1/4,1/2,1/2]
#0  1  2  3  4  5  6  7  8  9  10  11
#C  C# D  D# E  F  F# G  G#  A  A#  B

#12  13  14  15  16  17  18  19  20  21  22  23
#C  C#    D  D#  E   F   F#  G   G#  A   A#  B
=======
def midicreate(notelist):
    #change_list=[8,5,6,'Rest',1,3]
    #tempo_list=[1/2,1/2,1/4,1/4,1/2,1/2]
#0  1  2  3  4  5  6  7  8  9  10  11
#C  C# D  D# E  F  F# G  G# A  A#  B
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    NoteList = []

    for i in range(len(notelist)):
        if(notelist[i][3]!='Rest'):
            NoteList.append(Note(notelist[i][3],dur=notelist[i][2]))
        else:
            NoteList.append(Rest(notelist[i][2]))

<<<<<<< HEAD
    #print(NoteList)
=======
    print(NoteList)
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    seq = NoteSeq(NoteList)
        
    midi = Midi(number_tracks=2, tempo=90)
    midi.seq_notes(seq, track=0)
    #midi.seq_notes(notes2, track=0)
<<<<<<< HEAD
    midi.write(f"/home/ec2-user/Ourchord/MIDI/result_{name}.mid") # ---------------------------------------------------- 경로 수정
          

    

=======
    #midi.write(".vscode//demotest.mid")
    midi.write("/home/ec2-user/Ourchord/MIDI/result.mid") # ---------------------------------------------------- 경로 수정
        
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4

    '''
    #note_sort_list = [[[0 for col in range(2)] for row in range(50)] for depth in range(len(staff_average)+1)]
    a=[]
    cutlist = []
    num=0
    checknum=0
    for i in range(len(notelist)):
        line = []              # 안쪽 리스트로 사용할 빈 리스트 생성
        if(start_list[checknum]>i):
            if(num==0):
                a.append(cutlist)
                checknum= checknum+1    
                num=num+1
        for j in range(2):
            line.append(notelist[i][j])     # 안쪽 리스트에 0 추가
        cutlist.append(line)         # 전체 리스트에 안쪽 리스트를 추가
    
    a.append(cutlist)
    
    print(a)
    '''

#pdf to png
def pdftopng(pdfpath):

    #pdffile = ".vscode//12.pdf"
    doc = fitz.open(pdfpath)
<<<<<<< HEAD
    mat = fitz.Matrix(3,3)
=======
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
    '''
    page = doc.loadPage(0) #number of page
    pix = page.getPixmap()
    output = ".vscode//outfile.png"
    pix.writePNG(output)
    '''
    for i in range(len(doc)):
        page = doc.loadPage(i)
<<<<<<< HEAD
        pix = page.getPixmap(matrix = mat)
        #pix = page.getPixmap()
        output = f'/home/ec2-user/Ourchord/PDF/pdf/filename{i}.png'
=======
        pix = page.getPixmap()
        #기존 outfile-->filename
        output = f'/home/ec2-user/Ourchord/PDF/pdf/filename{i}.png'# ---------------------------------------------------- 경로 수정
        #output = f".vscode//outfile{i}.png" # ---------------------------------------------------- 경로 수정
>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
        pix.writePNG(output)
        
    return len(doc)

<<<<<<< HEAD
=======
#note_search(imgpath)
#여기까지*************************************************

>>>>>>> 6a18104ae48c501dbb035979f7d686d67f0be9b4
runServer()
