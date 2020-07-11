import os, re, glob
import cv2
import numpy as np
import shutil
from numpy import argmax
from keras.models import load_model

groups_folder_path = "./test-image"
categories = ["4", "8", "16"]
score_classes = len(categories)

def DataClassificaion(img_path):
    image_w = 28
    image_h = 28
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx = image_w/img.shape[1], fy = image_h/img.shape[0])
    return (img/256)

src = []
name = []
test = []

image_dir = '/Users/zjisuoo/Desktop/Pre/test03/test-image'
for file in os.listdir(image_dir):
    if(file.find('.png')is not - 1):
        src.append(image_dir + file)
        name.append(file)
        test.append(DataClassificaion(image_dir + file))

test = np.array(test)
model = load_model('Score.h5')
predict = model.predict_classes(test)

for i in range(len(test)):
    print(name[i] + ":, Predict : "+ str(categories[predict[i]]))