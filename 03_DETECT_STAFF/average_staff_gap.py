import cv2
import numpy as np

standard_detect_gap = 13

img = cv2.imread('.vscode//ad.png',cv2.COLOR_BGR2GRAY)  
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#이진화 170이상일시 흰색 아니면 흑색
ret, dst = cv2.threshold(img, 230,255,cv2.THRESH_BINARY)#ret에는 임계값이 저장
height, width, channel = img.shape

#print(height, width)
#width, height = img.size
#ylist[height] = 0
#px = img[2338, 1653]
#print(px)

ylist=[0 for _ in range(height)]#이미지 높이 만큼 값 0을 가진 리스트 생성 => ylist[높이만큼 개수] = [0]

for i in range(height):#y좌표
    for j in range(width):#x좌표
        px = dst[i,j]
        if(px[0]==0 and px[1]==0 and px[2]==0):
            ylist[i] +=1

staff=[]#오선 좌표
for i in range(len(ylist)):
    if(ylist[i]>width*0.8):#이미지 크기의 너비의 80%이상일 때 오선으로 간주
        #print(i)
        staff.append(i)

print("뽑힌 오선 개수",len(staff))#오선 개수 확인(중복 있음)

removelsit=[]#제거할 원소 자리
#중복 제거 2픽셀이하로 가까우면 제거 리스트에 들어간다.
for i in range(len(staff)-1):
    if(staff[i+1]-staff[i]<3):
        removelsit.append(i)

print(staff,removelsit)

for i in range(len(removelsit)-1, -1, -1):#내림차순한 이유는 오름차순으로 제거하면 삭제되면서 정확한 데이터가 삭제가 안된다.
    del staff[removelsit[i]]

for i in range(len(staff)):
    cv2.line(img, (10,staff[i]), (width,staff[i]),(255,0,0),2)

print(staff,removelsit)#오선좌표와 제거되는 원소 자리수
print("오선 개수 : ",len(staff))

gaplist=[]

for i in range(int(len(staff)/5)):
    for j in range(4):
        #print((staff[5*i+j+1],staff[5*i+j]))
        gaplist.append((staff[5*i+j+1]-staff[5*i+j]))

print(gaplist)
averagegap = sum(gaplist)/len(gaplist)
#averagegap = round(averagegap,3)
print(averagegap)
rate = standard_detect_gap/averagegap
round(rate,3)
print(rate)

cv2.imshow('staff',img)
cv2.imwrite('.vscode//test.png',img)
cv2.waitKey()
cv2.destroyAllWindows()