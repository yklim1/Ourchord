import numpy as np
import cv2

img = cv2.imread('jenny.jpeg', cv2.IMREAD_COLOR)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

cv2.imshow('JENNY', img)
cv2.imshow("JENNY_CONTOURS", thresh)
cv2.waitKey(0)