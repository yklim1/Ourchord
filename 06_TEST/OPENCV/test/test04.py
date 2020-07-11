import cv2

img_color = cv2.imread('jenny.jpeg', cv2.IMREAD_COLOR)
img_gray = cv2.imread('jenny.jpeg', cv2.IMREAD_GRAYSCALE)

cv2.imshow("JENNY", img_color)
cv2.imshow("GRAY JENNY", img_gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
