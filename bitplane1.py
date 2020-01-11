import cv2 
import numpy as np

img = cv2.imread('.vscode\score4.png', 0) 
#cv2.imshow(f"bit plane", img)


    # create an image for each k bit plane
plane = np.full((img.shape[0], img.shape[1]), 2 ** 6, np.uint8)
    # execute bitwise and operation
res = cv2.bitwise_and(plane, img)
    # multiply ones (bit plane sliced) with 255 just for better visualization
x = res * 255
    # append to the output list
#out.append(x)

kernel = np.ones((9,9),np.uint8)

closing = cv2.morphologyEx(x, cv2.MORPH_CLOSE, kernel)


#cv2.imshow(f"bit plane", np.hstack(out))
#cv2.imshow(f"bit plane1", x)
#cv2.imshow(f"bit plane1", closing)
#cv2.imwrite('.vscode\closebit.png',closing)
'''
lower_orange = (0, 100, 0)

upper_orange = (0, 255, 100)

img = np.full((1000,2000,255), 12, np.uint8)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_mask = cv2.inRange(img_hsv, lower_orange, upper_orange)
img_result = cv2.bitwise_and(img, img, mask=img_mask)
'''

cv2.imshow(f"bit plane1", closing)

cv2.waitKey()