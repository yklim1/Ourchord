import os, re, glob
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

groups_folder_path = "./test-image/"
categories = ["4", "8", "16"]
score_classes = len(categories)

image_w = 28
image_h = 28

X = []
Y = []

for idex, categories in enumerate(categories):
    label = [0 for i in range(score_classes)]
    label[idex] = 1
    image_dir = groups_folder_path + categories + "/"

    for top, dir, f in os.walk(image_dir):
        for filename in f:
            print(image_dir + filename)
            img = cv2.imread(image_dir + filename)
            # resize -> 곱하기 연산
            img = cv2.resize(img, None, fx = image_w/img.shape[0], fy = image_h/img.shape[1])
            X.append(img/256)
            Y.append(img/label)

X = np.array(X)
Y = np.array(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
xy = (X_train, X_test, Y_train, Y_test)

# npy -> 이진화 해서 저장
np.save("./img_data.npy", xy)
