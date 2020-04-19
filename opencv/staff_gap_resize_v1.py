import cv2


# 원본 이미지
img_source = cv2.imread('.vscode//ad.png')
cv2.imshow("original", img_source)

cv2.waitKey(0)


# 2배 이미지
# 밑의 fx와 fy에 이미지 비율에 대한 값이 들어가야 함. 값은 구하는 값은 다른 곳에 구현 되어 있다.
img_result = cv2.resize(img_source, None, fx=1.625, fy=1.625, interpolation = cv2.INTER_CUBIC)
cv2.imshow("x2", img_result)
cv2.imwrite(".vscode//resizeaa.png",img_result)
cv2.waitKey(0)

cv2.waitKey(0)


cv2.destroyAllWindows()
