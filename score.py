import cv2
import numpy as np

img = cv2.imread('.vscode\score2.png',cv2.COLOR_BGR2GRAY)
#blur = cv2.GaussianBlur(img, (3,3), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 200, 300, apertureSize = 3)
minLineLength = 50
maxLineGap = 10

#lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
i=1
y=[]

if lines is not None:
   for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        print(f"{i}번째 : ", end=' ')
        print(y1,y2)
        i=i+1
        '''
        no=1
        gap= y2-y1
        if gap==0:
            if y2 not in y:
                for x in y:
                    m=abs(x-y2)
                    if m<17:
                        no=0
                if no != 0:
                    if y2>230:
                        y.append(y1)    
                        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
            y = list(set(y))
            '''
#cv2.line(img, (0, 260), (400, 260), (0, 0, 255), 1)
#cv2.line(img, (0, 242), (400, 242), (0, 0, 255), 1)
'''
for a in y:
    print(f"{i}번째 :", end=' ')
    print(a)
    i=i+1
'''
cv2.imshow('SCORE_EDGE', edges)
cv2.imshow('RESULT', img)
cv2.waitKey()
cv2.destroyAllWindows()