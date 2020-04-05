import cv2
import numpy as np

img = cv2.imread('.vscode//bb.png',cv2.COLOR_BGR2GRAY)  #load image
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #convert to grayscale

height, width, channel = img.shape

#print(height, width)
#width, height = img.size
#ylist[height] = 0
#px = img[2338, 1653]
#print(px)

ylist=[0 for _ in range(height)]

for i in range(height):#y좌표
    for j in range(width):#x좌표
        px = img[i,j]
        if(px[0]<50 and px[1]<50 and px[2]<50):
            ylist[i] +=1

staff=[]
for i in range(len(ylist)):
    if(ylist[i]>1300):
        #print(i)
        staff.append(i)

print(len(staff))

removelsit=[]

for i in range(len(staff)-1):
    if(staff[i+1]-staff[i]<3):
        removelsit.append(i)

print(staff,removelsit)

for i in range(len(removelsit)-1, -1, -1):
    del staff[removelsit[i]]

for i in range(len(staff)):
    cv2.line(img, (10,staff[i]), (width,staff[i]),(255,0,0),2)

print(staff,removelsit)
print("오선 개수 : ",len(staff))

cv2.imshow('staff',img)
cv2.imwrite('.vscode//result2.png',img)
cv2.waitKey()
cv2.destroyAllWindows()