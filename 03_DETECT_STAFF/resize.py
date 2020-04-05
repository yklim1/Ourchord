import cv2


# 원본 이미지
img_source = cv2.imread('.vscode//ad.png')
cv2.imshow("original", img_source)

cv2.waitKey(0)


# 2배 이미지
img_result = cv2.resize(img_source, None, fx=1.625, fy=1.625, interpolation = cv2.INTER_CUBIC)
cv2.imshow("x2", img_result)
cv2.imwrite(".vscode//resizeaa.png",img_result)
cv2.waitKey(0)

cv2.waitKey(0)


cv2.destroyAllWindows()