import cv2 as cv
import numpy as np

'''
img_rgb = cv.imread('.vscode\score4.png', 0) 
img_rgb1 = cv.imread('.vscode\score4.png', cv.COLOR_BGR2GRAY) 

img_gray = cv.cvtColor(img_rgb, cv.COLOR_BAYER_BG2GRAY)
#img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
#gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('.vscode\mat2.png', cv.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)

threshold = 0.8
loc = np.where(res >= threshold)
red=(0, 0, 255)

for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb1, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv.imshow('result', img_rgb1)
cv.waitKey(0)
'''