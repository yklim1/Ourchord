import cv2
import numpy as np

def binary_search_np(A, B):
    # assume A and B are numpy arrays
    idx2 = np.minimum(len(A) - 1, np.searchsorted(A, B)) 
    idx1 = np.maximum(0, idx2 - 1)
    idx2_is_better = np.abs(A[idx1] - B) > np.abs(A[idx2] - B)
    np.putmask(idx1, idx2_is_better, idx2)
    return A[idx1]



img = cv2.imread('.vscode\score2.png',cv2.COLOR_BGR2GRAY)
#blur = cv2.GaussianBlur(img, (3,3), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 200, 300, apertureSize = 3)
minLineLength = 200
maxLineGap = 40
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
ytest=[]
n=1
if lines is not None:
   for line in lines:
        x1, y1, x2, y2 = line[0]
        #cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 1)
        if y2-y1 == 0:
            for y in ytest:
                if abs(y-y2)<8:
                    n=0
            if n!=0:
                ytest.append(y1)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            n=1

ytest.sort()
i=0
'''
cv2.line(img, (0, 549), (2000, 549), (255, 0, 255), 2)
cv2.line(img, (0, 1212), (2000, 1212), (255, 0, 255), 2)
cv2.line(img, (0, 1544), (2000, 1544), (255, 0, 255), 2)
'''

for  a in ytest:
    print(f"{i+1}번째 : ", end=' ')
    print(a)
    i=i+1
'''
gap=[]
gap.append((ytest[4]-ytest[0])/4)
gap.append((ytest[9]-ytest[5])/4)
gap.append((ytest[14]-ytest[10])/4)
print(gap)

step=ytest[5]-ytest[4]
print(step)
step=ytest[10]-ytest[9]
print(step)
'''
#cv2.imshow('SCORE_EDGE', edges)
cv2.imshow('RESULT', img)
cv2.imwrite('.vscode\score3.png',img)
cv2.waitKey()
cv2.destroyAllWindows()
