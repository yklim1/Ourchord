import cv2
import numpy as np

img = cv2.imread('jenny.jpeg', cv2.IMREAD_COLOR)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

cv2.imshow('JENNY', img)
cv2.imshow("JENNY_CONTOURS", thresh)
cv2.waitKey(0)

while(1):
    ret, frame = img.read()

    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lowerBound = np.array([20, 100, 100])
        upperBound = np.array([30, 255, 255])

        mask = cv2.inRange(img, lowerBound, upperBound)

        kernelOpen = np.ones((5, 5))
        kernelClose = np.ones((20, 20))

        maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

        maskFinal = maskClose
        img2, contours, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(img, contours, -1 (255, 0, 0), 3)
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
