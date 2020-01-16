import cv2
import numpy as np

img = cv2.imread('Score2.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
minLineLength = 50
maxLineGap = 10

lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)

cv2.imshow('SCORE_EDGE', edges)
cv2.imshow('RESULT', img)
cv2.waitKey()
cv2.destroyAllWindows()