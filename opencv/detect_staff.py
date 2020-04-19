import cv2
import numpy as np

def detect_staff(imagepath):#오선 좌표구하는 함수, 입력 값 : 이미지 경로 , 출력 값 : 오선 좌표 리스트
    img = cv2.imread(imagepath,cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, dst = cv2.threshold(gray, 170,255,cv2.THRESH_BINARY)#ret에는 임계값이 저장
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

def average_staff_gap(stafflist):#오선의 한칸의 값의 평균 값 구하는 함수. 입력 : 오선 좌표 리스트, 출력 : 오선 한 칸의 평균 값. 활용도 : 이미지 리사이즈를 위해 사용
    standard_detect_gap = 13
    gaplist=[]
    for i in range(int(len(stafflist)/5)):
        for j in range(4):
            gaplist.append((stafflist[5*i+j+1]-stafflist[5*i+j]))
    averagegap = sum(gaplist)/len(gaplist)
    rate = standard_detect_gap/averagegap
    rate = round(rate,3)
    return rate

def resize_staff(imagepath, rate):
    img = cv2.imread(imagepath,cv2.IMREAD_COLOR)
    img_result = cv2.resize(img, None, fx=rate, fy=rate, interpolation = cv2.INTER_CUBIC)
    cv2.imwrite(".vscode//resizestaff.png",img_result)#이 부분은 return으로 경로가 잘 안 될수도 있어 이미지를 따로 저장. 이 경로는 서버쪽으로 가면 추후 수정 해야 함.
    return img_result


#테스트
#img = cv2.imread('.vscode\gu.png',cv2.COLOR_BGR2GRAY)
imgpath=".vscode//gu.png"
staff = detect_staff(imgpath)
print(staff)
print(len(staff))
rate = average_staff_gap(staff)
print(rate)
reszieimg = resize_staff(imgpath,rate)
