import numpy as np
import cv2

def img_load():
    img = cv2.imread('jenny.jpeg', cv2.IMREAD_COLOR)
    cv2.imshow('JENNY', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
img_load()