import cv2
import numpy as np

img_gray = cv2.imread('file_path', cv2.IMREAD_GRAYSCALE)
img_gray = cv2.medianBlur(img_gray, 5)
img_color = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, param2 = 50, minRadius = 0, maxRadius = 0)
# circles = cv.HoughCircles(img_gray,cv.HOUGH_GRADIENT,1,20,param1=50,param2=35,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    center = (i[0], i[1])
    radius = i[2]

    cv2.circle(img_color, center, radius, (0, 255, 0), 2)

    cv2.circle(img_color, center, 2, (0, 0, 255), 3)

cv2.imshow('detected circles', img_color)
cv2.waitKey()
cv2.destroyAllWindows()