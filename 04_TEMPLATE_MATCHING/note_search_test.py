import cv2 as cv
import numpy as np

img_rgb = cv.imread('a.jpg', 0)
img_gray_1 = cv.imread('a.jpg', cv.COLOR_BGR2GRAY)
# ret 에 임계값 저장 / 임계값은 흑백 나눌 기준 값이 100 이기 때문에 100 이하면 0, 100 이상이면 최댓값 255로 변경
ret, dst = cv.threshold(img_gray_1, 100, 255, cv.THRESH_BINARY)
x = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
img_gray_2 = cv.imread('a.jpg', cv.COLOR_BGR2GRAY)

lists = ['./tem/tem_full_1.png', './tem/tem_full_2.png', './tem/tem_full_3.png', './tem/tem_full_4.png', './tem/tem_full_5.png', './tem/tem_full_6.png', './tem/tem_full_7.png', './tem/tem_full_8.png', './tem/tem.png', './tem/tem1.png'] 

xylist = []
xylist.append([])
i = 0
for image in lists :
    template = cv.imread(image, 0)
    w, h = template.shape[::-1]

    res = cv.matchTemplate(x, template, cv.TM_CCOEFF_NORMED) 
    threshold = 0.41
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]) :
        # pt 는 템플릿 매칭 시 사각형을 그려줄 때 왼쪽 위 좌표와 오른쪽 아래 좌표가 필요한데 오른쪽 아래 좌표를 뜻함
        cv.rectangle(img_gray_1, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
        # pt[0] 은 가로 pt[1] 은 세로
        xylist[i].append(pt[0])
        xylist[i].append(pt[1])
        xylist.append([])
        i = i + 1

    num = len(xylist)
    re_list = []
    k = 0

    for i in range(len(xylist) - 1):
        for j in range(i + 1,len(xylist) - 1):
            if abs(xylist[i][0] - xylist[j][0])<5 and abs(xylist[i][1] - xylist[j][1]) < 5 :
                re_list.append(i)
                
    re_list=list(set(re_list))
    re_list.sort()
    re_num=len(re_list)-1

    #중복 좌표 제거
    for i in range(re_num, -1, -1):
        del xylist[re_list[i]]

del xylist[len(xylist) - 1]

num = len(xylist)-1
m = 1
for i in range(num):
    print(f"{m}번째 : ", xylist[i][0],xylist[i][1])
    m = m + 1

cv.imshow('result-1', img_rgb)
cv.imshow('result-2', img_gray_1)
cv.waitKey(0)