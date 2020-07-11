import numpy as np
from matplotlib import pyplot as plt
import cv2

img_1 = cv2.imread('/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/score1.png', cv2.COLOR_BGR2GRAY)


template = cv2.imread('./tem/tem_full_1.png', cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for method in methods :
    #img_1 = img_2.copy()
    methods = eval(method)
    
    try : 
        res = cv2.matchTemplate(img_1, template, methods)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    except :
        print('오류', method)
        continue

    if methods in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED] :
        top_left = min_loc
    else :
        top_left = max_loc

    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img_1, top_left, bottom_right, 255, 2)

'''
    plt.subplot(121), plt.imshow(res, cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.ytikcs([])

    plt.subplot(122), plt.imshow(img_1, cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.ytikcs([])
    plt.subtitle(method)

    plt.show()
'''      
cv2.imshow('result', img_1)
cv2.waitKey(0)