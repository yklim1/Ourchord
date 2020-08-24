#-*- coding: utf-8 -*-
import socketserver
from pyknon.genmidi import Midi
from pyknon.music import NoteSeq, Note, Rest

import time
import os
import cv2
import numpy as np
import copy
import threading
from multiprocessing import Process, Queue
from operator import itemgetter
import fitz
import tensorflow.keras
from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join, exists




standard_detect_gap = 13

HOST = ''
PORT = 9300
Base='C'
Change='D'
model = tensorflow.keras.models.load_model('/home/ec2-user/Ourchord/DEEP/staff_224.h5')
#model = tensorflow.keras.models.load_model('/home/ec2-user/Ourchord/DEEP/note_model.h5')

class NoteInfo:
    def __init__(self):
        self.harmony = 1
        self.tempo = 1/4
    def Set_X(self, x):
        self.x = x
    def Set_Y(self, y):
        self.y = y
    def Set_XY(self, x, y):
        self.x = x
        self.y = y
    def Set_Scale(self, scale):
        self.scale = scale
    def Set_Tempo(self, tempo):
        self.tempo = tempo
    def Set_Line(self, line):
        self.line = line
    def Set_Harmony(self, harmony):
        self.harmony = harmony
    
class ScoreInfo:
    def __init__(self,base,change):
        self.base = base
        self.change = change

    def transpose(self):
        scorelist = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        basenum = scorelist.index(self.base)
        changenum = scorelist.index(self.change)
        gap = changenum - basenum
        self.gap = gap

class PdfInfo:
    def __init__(self,pdf_path,pdf_name):
        self.pdf_path = pdf_path
        self.pdf_name = pdf_name
    def Set_pdfPage(self,pdf_page):
        self.pdf_page = pdf_page


#음표 좌표 추출
def note_search(imgpath,mPdf,mScore):

    #transegap : 조 변환 gap, stafflist : 기존 악보의 오선 좌표, reszie_rate : 기존 악보 오선과 탬플릿 매칭 오선 좌표 비율, resize_img_path : 리사이즈 된 악보 이미지
    #resize_stafflist : 리사이즈 된 악보의 오선 좌표, divideimglist : 악보 오선 별 로 자른 이미지 리스트
    
    # 조 변환 gap 구하는 함수
    # 입력 값 : 기존 조(코드), 변환 조(코드)      
    # 출력 값 : 두 조의 갭
    transe = threading.Thread(target = mScore.transpose)
    transe.start()


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
    resize_img_path = resize_image(imgpath,reszie_rate,mPdf.pdf_page)


    # 오선 좌표구하는 함수       
    # 입력 값 : 이미지 경로       
    # 출력(리턴) 값 : 오선 좌표 리스트
    # 리사이즈 된 오선 좌표
    resize_stafflist = detect_staff(resize_img_path)
    
    # 악보 오선으로 이미지 자르기 -> ex) 첫번째 오선 이미지, 두번째 오선 이미지 ...
    # 입력 값 : 리사이즈 된 악보 이미지, 리사이즈 된 오선 리스트
    # 출력 값 : 분류 된 오선 이미지
    divideimglist = dividescore(resize_img_path,resize_stafflist)
    
    # ---------------------------------------------------- 경로 수정
    # notelists: tem_empty, tem_full: 기존-6, 4 --> 5, 5
    # /home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_1~5.png
    # /home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_1~5.png
    notelists = ['/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_1.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_2.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_3.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_4.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_5.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_full/tem_full_6.png']#full png경로
    emptylists = ['/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_1.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_2.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_3.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_4.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_5.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_6.png',
                 '/home/ec2-user/Ourchord/NOTE/tem/tem_empty/tem_empty_7.png']#empty png 경로
    eightrest=['/home/ec2-user/Ourchord/NOTE/rest/eightrest/eight.png'] #8분쉼표
    quarterrest=['/home/ec2-user/Ourchord/NOTE/rest/quarterrest/quarter.png'] #4분쉼표
    halfrest=['/home/ec2-user/Ourchord/NOTE/rest/halfrest/half.png'] #2분쉼표
    wholerest=['/home/ec2-user/Ourchord/NOTE/rest/wholerest/whole.png'] #온쉼표
    # ---------------------------------------------------- 경로 수정

    notevalue = '음표'
    emptyvalue = '2분음표'
    eightvalue = 1/8
    quartervalue = 1/4
    halfvalue = 1/2
    wholevalue = 1
    # 8분 쉼표 0.8
    # 4분 쉼표 0.75
    # 2분,온쉼표 0.9 이상

    # 자른 오선 이미지의 오선 좌표
    divide_stafflist = [40,53,66,79,92]
    alllist = []

    for i in range(len(divideimglist)):
        
    #     ######################종합설계 발표 테스트 데모 작업 copyimgtest 추가 후에 삭제 -> template_note_list()에 변수추가 후에 삭제 해야 한다.
        copyimgtest = cv2.cvtColor(divideimglist[i], cv2.COLOR_RGB2BGR)
        

    #     이어져 있는 8,16음표 찾기
    #     입력 값 : 자른 오선 이미지
    #     출력 값 : 8, 16음표인 x 좌표
        checklinklist = checklink(divideimglist[i],i)

    #     탬플릿 매칭
    #     입력 값 : 오선으로 자른 이미지, 탬플릿 매칭할 이미지, 설정 값
    #     출력 값 : x,y좌표
        xylist = template_note_list(divideimglist[i],notelists,notevalue,copyimgtest,i)

    #     박자 딥러닝 하기전 테스트
    #     여기다 박자 딥러닝 시킨거 해서 insert
    #     for a in range(len(xylist)):
    #       xylist[a].append(1/4)
    #     xylist.sort(key=itemgetter(0))

    #     음표 이미지 자르기
    #     입력 값 : x,y 좌표 리스트
    #     출력 값 : 없음 -> 따로 이미지 저장
        note_image(xylist,divide_stafflist,divideimglist[i],mPdf.pdf_page)

    #     print("xylist 좌표 ",xylist)                
        tempolist = tempo_classfication(xylist,model,mPdf.pdf_page)
    #     tempolist.sort(key=itemgetter(0))

    #     print("xylist 템포 추가 ",tempolist) 
    #     박자 변환
    #     입력 값 : 음표 리스트, 8,16 음표의 x좌표 리스트
    #     출력 값 : 변환된 리스트
        chxylist = change_tempolist(xylist,checklinklist)
        
        halfnote = template_note_list(divideimglist[i],emptylists,emptyvalue,copyimgtest,i)
        chxylist = chxylist + halfnote
        chxylist = sorted(chxylist, key = lambda note: note.y)
        

    #     쉼표 좌표 찾기
        eightlist = template_note_list(divideimglist[i],eightrest,eightvalue,copyimgtest,i)
    #     print("8분 : ",eightlist)  
        quarterlist = template_note_list(divideimglist[i],quarterrest,quartervalue,copyimgtest,i)
    #     print("4분 : ",quarterlist)
        halflist = template_note_list(divideimglist[i],halfrest,halfvalue,copyimgtest,i)
    #     print("2분 : ",halflist)
        wholelist = template_note_list(divideimglist[i],wholerest,wholevalue,copyimgtest,i)
    #     print("온 : ",wholelist)

    #     쉼표 리스트
        restlist = eightlist+quarterlist+halflist+wholelist
    #     xylist.sort()
        restlist = sorted(restlist, key = lambda note: note.x)

    #     음계 추출-> y좌표를 가지고 음계 값 설정
    #     입력 값 : 자른 이미지의 오선 y좌표, 음표
    #     출력 값 : 음계가 insert 된 list
        scale_note_list = note_scale(divide_stafflist,chxylist)
        note_list = scale_note_list + restlist
        
    #     오선 순서
        for xy in range(len(note_list)):
            note_list[xy].Set_Line(i)

        note_list = sorted(note_list, key = lambda note: note.x)
        alllist = alllist + note_list



    # 화음 리스트 찾기
    # 입력 값 : 음표 리스트
    # 리턴 값 : 화음 정보 추가된 리스트 -> 리스트 정보 [x,y,박자,음계,오선번째,화음정보]  -> 화음정보 1이면 기본, 2이상 이면 그 수만큼의 개수, 0이면 제외 
    harmolist = harmonysearch(alllist)

    baseResultNmae = 'Base_' + mScore.base
    chageResultName = 'Change_' + mScore.change
    # midi 생성
    # 입력 값 : 음표 리스트
    # 리턴 값 : midi
    
    midicreate(harmolist,baseResultNmae,mPdf.pdf_page)

    # 음계 체인지
    # 입력 값 : 음표 리스트, 바꿀 조 갭
    # 리턴 값 : 음계 변환 된 리스트
    change_list=changescale(harmolist,mScore.gap)


    # midi 생성
    # 입력 값 : 음표 리스트
    # 리턴 값 : midi
    midicreate(change_list,chageResultName,mPdf.pdf_page)

    

# 박자 인식 05/13
def tempo_classfication(xylist, model,page):

    np.set_printoptions(suppress=True)

    # 타겟 사이즈 224 X 224 
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    #notelist_path: 음표 꼬리 저장(250,258)
    notelist_path = f'/home/ec2-user/Ourchord/PDF/pdf/note/{page}/'
    onlyfiles = [f for f in listdir(notelist_path) if isfile(join(notelist_path, f))]
    onlist = []
    for i in range(len(onlyfiles)):
        onlyfiles[i] = onlyfiles[i].replace(".png", "")
        onlyfiles[i] = onlyfiles[i].replace(".PNG", "")
        onlist.append(int(onlyfiles[i]))
    onlist.sort()

    for i in range(len(onlist)):
        onlyfiles[i] = str(onlist[i]) + '.png'


    image = np.empty(len(onlyfiles), dtype = object)
    tempolist = []
    for item in range(0, len(onlyfiles)) :
        image[item] = Image.open(join(notelist_path+onlyfiles[item])).convert('RGB')
        
        image[item] = image[item].resize((224, 224))
        image[item] = ImageOps.fit(image[item], (224, 224), Image.ANTIALIAS, centering = (0.5, 0.5))

        image_array = np.array(image[item])

        normalized_image_array = (image_array.astype(dtype = np.float32) / 127.0) - 1

        data[0] = normalized_image_array

        prediction = model.predict(data)
        index, value = max(enumerate(prediction[0]), key=operator.itemgetter(1))
        if(index == 0):
            xylist[item].Set_Tempo(1/4)
            #print(onlyfiles[item]," 사진 : 4분음표")
        elif(index == 1):
            xylist[item].Set_Tempo(1/4)
            #print(onlyfiles[item]," 사진 : 4분음표")
        elif(index == 2):
            xylist[item].Set_Tempo(1/8)
            #print(onlyfiles[item]," 사진 : 8분음표")
        elif(index == 3):
            xylist[item].Set_Tempo(1/8)
            #print(onlyfiles[item]," 사진 : 8분음표")
        else:
            print("박자 넘어감",index)

    onlyfiles = [f for f in listdir(notelist_path) if isfile(join(notelist_path, f))]
    for i in range(len(onlyfiles)):
        os.remove(notelist_path+onlyfiles[i])

    os.rmdir(notelist_path)
    return xylist        

def note_image(xylist,stafflist,image_path,page):
    
    os.makedirs(f'/home/ec2-user/Ourchord/PDF/pdf/note/{page}')
    img_rgb = image_path
    img_rgb2 = image_path 
    num = len(xylist)
    #y좌표를 오름차순으로 정렬
    xylist = sorted(xylist, key = lambda note: note.y)
    staffnum = 1
    updownlist = []
    #밑에 음표 자르는 부분 def 로 변환 필요
    for i in range(num):
        if(xylist[i].y<stafflist[2]):
            updownlist.append("down")
            testcopy = img_rgb[xylist[i].y-3:xylist[i].y+60, xylist[i].x-2:xylist[i].x+31]
            cv2.imwrite(f'/home/ec2-user/Ourchord/PDF/pdf/note/{i}.png',testcopy)    # ---------------------------------------------------- 경로 수정
        else:
            updownlist.append("up")
            testcopy = img_rgb[xylist[i].y-48:xylist[i].y+15, xylist[i].x-2:xylist[i].x+31]
            cv2.imwrite(f'/home/ec2-user/Ourchord/PDF/pdf/note/{i}.png',testcopy)    # ---------------------------------------------------- 경로 수정

    cv2.imwrite('/home/ec2-user/Ourchord/PDF/pdf/testnotesearch.png',img_rgb2) 

#악보 이미지 리사이즈
def resize_image(imgpaht, rate, page):
    img_source = cv2.imread(imgpaht,0)
    resize_img_path = f'/home/ec2-user/Ourchord/PDF/pdf/resize/renew{page}.png'
    #이미지 변환
    img_result = cv2.resize(img_source, None, fx=rate, fy=rate, interpolation = cv2.INTER_CUBIC)
    cv2.imwrite(resize_img_path,img_result)
    
    return resize_img_path

#midi 생성
def midicreate(notelist,name,page):
    NoteList = []
    for i in range(len(notelist)):
        if(notelist[i].scale=='Rest'):
            chord = Rest(notelist[i].tempo)
        elif(notelist[i].harmony==0):
            continue
        elif(notelist[i].harmony==2):
            chord = NoteSeq([Note(notelist[i].scale,dur=notelist[i].tempo),Note(notelist[i+1].scale,dur=notelist[i].tempo)])
        elif(notelist[i].harmony==3):
            chord = NoteSeq([Note(notelist[i].scale,dur=notelist[i].tempo),Note(notelist[i+1].scale,dur=notelist[i].tempo),Note(notelist[i+2].scale,dur=notelist[i].tempo)])
        elif(notelist[i].harmony==4):
            chord = NoteSeq([Note(notelist[i].scale,dur=notelist[i].tempo),Note(notelist[i+1].scale,dur=notelist[i].tempo),Note(notelist[i+2].scale,dur=notelist[i].tempo),Note(notelist[i+3].scale,dur=notelist[i].tempo)])
        else:
            chord = NoteSeq([Note(notelist[i].scale,dur=notelist[i].tempo)])
        

        NoteList.append(chord)


    midi = Midi(1, tempo=117)
    checktract = 0
    midi.seq_chords(NoteList,track=0)
    midi.write(f"/home/ec2-user/Ourchord/MIDI/{page}/{name}.mid") # ---------------------------------------------------- 경로 수정


# 탬플릿 매칭
def template_note_list(divide_img, temlist,divide,copyimgtest,imgnum):
    

    ret, dst = cv2.threshold(divide_img,100,255,cv2.THRESH_BINARY)

    copyimg = divide_img.copy()

    if(divide == '음표'):
        threshold = 0.68
    elif(divide == '2분음표'):
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
    i=0
    for image in temlist:
        template = cv2.imread(image,0)
        ret1, dst1 = cv2.threshold(template,100,255,cv2.THRESH_BINARY)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(dst,template,cv2.TM_CCOEFF_NORMED) #0.6<x< 0.65
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            note = NoteInfo()
            note.Set_XY(pt[0],pt[1])
            if(divide != '음표'):
                if(divide == '2분음표'):
                    note.Set_Tempo(1/2)
                else:
                    note.Set_Tempo(divide)
                    note.Set_Scale('Rest')
            xylist.append(note)
            i=i+1
    
    num=len(xylist)
    xylist = sorted(xylist, key = lambda note: note.y)
    remlist=[]
    
    for i in range(num-1):
        for j in range(i+1,num):
            if abs(xylist[i].x-xylist[j].x)<5 and abs(xylist[i].y-xylist[j].y)<5 :
                remlist.append(i)

    remlist=list(set(remlist))
    remlist.sort()
    remnum=len(remlist)-1

    #중복 좌표 제거
    for i in range(remnum, -1, -1):
        del xylist[remlist[i]]
    num = len(xylist)-1

    #y좌표를 오름차순으로 정렬
    xylist = sorted(xylist, key = lambda note: note.y)

    return xylist

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
def checklink(divide_img,divide_num):
    w,h = divide_img.shape[::-1]
    kernel_size_row = 4
    kernel_size_col = 4
    kernel = np.ones((4, 4), np.uint8)
    alllist = []
    dilate_image = cv2.dilate(divide_img, kernel, iterations=1)
    ret, dst = cv2.threshold(dilate_image, 180,255,cv2.THRESH_BINARY)#ret에는 임계값이 저장
    test_w,test_h = dst.shape[::-1]
    eightlist=[]
    eightlist.append([])
    n=0
    nLen = 0
    nH = 0;
    nW = 0;

    for t_h in range(test_h):       
        for t_w in range(test_w):
            #if(t_h+nH<test_h and t_w+nW<test_w):
                
            if(dst[t_h+nH,t_w+nW]==0):
                nLen = nLen +1
                continue
            else:
                if(t_h+1<test_h):    
                    if(dst[t_h+1,t_w]==0):
                        nH = nH + 1
                        nLen = nLen + 1
                    elif(dst[t_h-nH,t_w]==0):
                        nH = nH - 1
                        nLen = nLen + 1
                    else:
                        if(nLen>23):
                            eightlist[n].append(t_w-nLen-1)
                            eightlist[n].append(t_w)
                            eightlist[n].append(t_h)
                            eightlist.append([])
                            n=n+1
                        nLen = 0
                        nH = 0;
                        nW = 0;
                else:
                    if(nLen>23):
                        eightlist[n].append(t_w-nLen-1)
                        eightlist[n].append(t_w)
                        eightlist[n].append(t_h)
                        eightlist.append([])
                        n=n+1
                    nLen = 0
                    nH = 0;
                    nW = 0;

                    


                 

    del eightlist[len(eightlist)-1]
    eightlist.sort(key=itemgetter(0,2))

    testremove = []
    testremove2 = []
    for i in range(len(eightlist)-1):
        for j in range(i+1,len(eightlist)):
            if(abs(eightlist[i][0] - eightlist[j][0])<6 and abs(eightlist[i][2] - eightlist[j][2])<6 and abs(eightlist[i][0]-eightlist[i][1]) <= abs(eightlist[j][0]-eightlist[j][1])):
                testremove.append(i)
                break

    testremove.sort()
    for i in reversed(range(len(testremove))):
        del eightlist[testremove[i]]

    for i in range(len(eightlist)-1):
        for j in range(i+1,len(eightlist)):
            if(abs(eightlist[i][0] - eightlist[j][0])<6 and abs(eightlist[i][2] - eightlist[j][2])<6 and abs(eightlist[i][0]-eightlist[i][1]) >= abs(eightlist[j][0]-eightlist[j][1])):
                testremove2.append(j)
                break
    testremove2.sort()
    for i in reversed(range(len(testremove2))):
        del eightlist[testremove2[i]]

    img_copy2 = cv2.cvtColor(divide_img,cv2.COLOR_BGR2RGB)
    for i in range(len(eightlist)):
        eightlist[i][0] = eightlist[i][0] - 20
        eightlist[i][1] = eightlist[i][1] + 10
        cv2.line(img_copy2,(eightlist[i][0]-20,eightlist[i][2]),(eightlist[i][1],eightlist[i][2]),(0,0,255))
        alllist.append(eightlist[i])

    del eightlist
    
    cv2.imwrite(f'/home/ec2-user/test/{divide_num}.png',img_copy2)
    
    return alllist

#8,16 박자 변환  
def change_tempolist(notelist, chlist):
    #x좌표로 정렬
    notelist = sorted(notelist, key = lambda note: note.x)
    if (len(chlist)==1):
        chlist[0].append(1/8)
    else:
        for s in range(len(chlist)-1):
            if(chlist[s+1][0]-chlist[s][0]<3):
                chlist[s].append(1/16)
                if(chlist[s+1][1]-chlist[s][1]<3):
                    chlist[s+1].append(1/16)
                else:
                    chlist[s+1].append(1/8)
            else:
                chlist[s].append(1/8)
                if(s==len(chlist)-2):
                    chlist[s+1].append(1/8)

    for i in reversed(range(len(chlist))):
        for x in range(len(notelist)):
            if(chlist[i][0]<notelist[x].x<chlist[i][1]):
                notelist[x].Set_Tempo(chlist[i][3])

    return notelist

# 오선 비율 확인
def averge_rate_staff(stafflist):
    gaplist=[]

    for i in range(int(len(stafflist)/5)):
        for j in range(4):
            gaplist.append((stafflist[5*i+j+1]-stafflist[5*i+j]))

    averagegap = sum(gaplist)/len(gaplist)
    rate = standard_detect_gap/averagegap
    round(rate,3)

    return rate

# 오선 좌표구하는 함수, 입력 값 : 이미지 경로 , 출력 값 : 오선 좌표 리스트
def detect_staff(imagepath):
    img = cv2.imread(imagepath,cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 테스트 확인용 카피 이미지
    ret, dst = cv2.threshold(gray, 160,255,cv2.THRESH_BINARY)#ret에는 임계값이 저장
    height, width = gray.shape

    np.clip(dst,-1,1,out=dst)
    sumb = dst.sum(axis=1)
    res = np.where(sumb<width*0.2)
    removelist=[]#제거할 원소 자리
    # 중복 제거 2픽셀이하로 가까우면 제거 리스트에 들어간다.
    for i in range(len(res[0])-1):
        if(res[0][i+1]-res[0][i]<3):
            removelist.append(i)
    new_res = np.delete(res,removelist)

    return new_res


#음계 설정
def note_scale(staff_list,notelist):
    i=0
    gap=6.5
    #나중에 np를 활용하여 해당 조건에 맞는 list 모아서 바로 변경
    for y in range(len(notelist)):
        if(staff_list[i]-gap*4.5<notelist[y].y<staff_list[i]-gap*3.5):
            notelist[y].Set_Scale(23)#멜로디 시 B5

        elif(staff_list[i]-gap*3.5<notelist[y].y<staff_list[i]-gap*2.5):
            notelist[y].Set_Scale(21)#멜로디 라 A5

        elif(staff_list[i]-gap*2.5<notelist[y].y<staff_list[i]-gap*1.5):
            notelist[y].Set_Scale(19)#멜로디 솔 G5

        elif(staff_list[i]-gap*1.5<notelist[y].y<staff_list[i]-gap/2):
            notelist[y].Set_Scale(17)#멜로디 파 F5

        elif(staff_list[i]-gap/2<notelist[y].y<staff_list[i]+gap/2):
            notelist[y].Set_Scale(16)#멜로디 미 E5
        
        elif(staff_list[i]+gap/2<notelist[y].y<staff_list[i+1]-gap/2):
            notelist[y].Set_Scale(14)#멜로디 레 D5

        elif(staff_list[i+1]-gap/2<notelist[y].y<staff_list[i+1]+gap/2):
            notelist[y].Set_Scale(12) #멜로디 도 C5

        elif(staff_list[i+1]+gap/2<notelist[y].y<staff_list[i+2]-gap/2):
            notelist[y].Set_Scale(11)#멜로디 시 B4

        elif(staff_list[i+2]-gap/2<notelist[y].y<staff_list[i+2]+gap/2):
            notelist[y].Set_Scale(9)#멜로디 라 A4

        elif(staff_list[i+2]+gap/2<notelist[y].y<staff_list[i+3]-gap/2):
            notelist[y].Set_Scale(7)#멜로디 솔 G4

        elif(staff_list[i+3]-gap/2<notelist[y].y<staff_list[i+3]+gap/2):
            notelist[y].Set_Scale(5)#멜로디 파 F4

        elif(staff_list[i+3]+gap/2<notelist[y].y<staff_list[i+4]-gap/2):
            notelist[y].Set_Scale(4)#멜로디 미 E4

        elif(staff_list[i+4]-gap/2<notelist[y].y<staff_list[i+4]+gap/2):
            notelist[y].Set_Scale(2)#멜로디 레 D4

        elif(staff_list[i+4]+gap/2<notelist[y].y<staff_list[i+4]+gap*1.5):
            notelist[y].Set_Scale(0)#멜로디 도 C4
        
        elif(staff_list[i+4]+gap*1.5<notelist[y].y<staff_list[i+4]+gap*2.5):
            notelist[y].Set_Scale(-1)#멜로디 시 B3
        
        elif(staff_list[i+4]+gap*2.5<notelist[y].y<staff_list[i+4]+gap*3.5):
            notelist[y].Set_Scale(-3)#멜로디 라 A3
        
        elif(staff_list[i+4]+gap*3.5<notelist[y].y<staff_list[i+4]+gap*4.5):
            notelist[y].Set_Scale(-5)#멜로디 솔 G3

        else:
            notelist[y].Set_Scale("미확인")
    
    return notelist

# 음계 변환
def changescale(scalelist,transgap):
    
    for i in range(len(scalelist)):
        if(scalelist[i].scale!='Rest'):
            #print(scalelist[i][3])
            scalelist[i].scale=scalelist[i].scale+transgap
            
    return scalelist

#화음 체크
def harmonysearch(notelist):
    for i in range(len(notelist)):
        num = 1
        if(notelist[i].harmony == 0):
            continue
        
        for ck in range(1,5):
            
            if(i+ck >= len(notelist)-1):
                if(notelist[i+ck-1].harmony != 1):
                    notelist[i+ck].harmony = 0
                    break
                
                else:
                    break
            
            if(abs(notelist[i].x-notelist[i+ck].x)<3):
                num = num + 1
                notelist[i].harmony=num
                notelist[i+ck].harmony=0
                
            else:
                notelist[i].harmony = num
                break
    return notelist


    #pdf to png
def pdftopng(pdf_path):
    doc = fitz.open(pdf_path)
    mat = fitz.Matrix(3,3)
    for i in range(len(doc)):
        page = doc.loadPage(i)
        pix = page.getPixmap(matrix = mat)
        output = f'/home/ec2-user/Ourchord/PDF/pdf/filename{i}.png'
        pix.writePNG(output)
            
    return len(doc)

#########       main        #######

#runServer()

def midiMain(filename,Base,Change):
    #filename = 'oldday_oldnight.pdf'
    #서버 pdf 저장 공간 

    pdfpath ='/home/ec2-user/Ourchord/USER/zjisuoo/'+filename
    mPdf = PdfInfo(pdfpath,filename)
    num = pdftopng(mPdf.pdf_path)

    mScore = ScoreInfo(Base,Change)
    processlist = []
    for a in range(num):
        processlist.append(f'process{a}')
    mPdfList = []
    for i in range(num):
        imgpath = f'/home/ec2-user/Ourchord/PDF/pdf/filename{i}.png' # ---------------------------------------------------- 경로 수정
        mPdf.pdf_name = filename.replace('.pdf',"")
                    
        print(mPdf.pdf_name)
        mPdf.Set_pdfPage(i)
        print(f"{i} 번째 프로세스 시작")
        processlist[i] = Process(target=note_search, args=(imgpath, mPdf,mScore))
        processlist[i].start()
    for i in range(num):
        processlist[i].join()

# starttime = time.time()
# filename = 'oldday_oldnight.pdf'
# Base = 'C'
# Change = 'D'
# midiMain(filename,Base,Change)

# print("time :", time.time() - starttime)
