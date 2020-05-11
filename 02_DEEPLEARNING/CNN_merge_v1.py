# 파일 정렬 완료 -> 모델 학습 더시켜야 됨!!!
import tensorflow.keras
from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join
from operator import itemgetter
import numpy as np
import cv2


def tempo_classfication(notelist_path, notelist) :

    np.set_printoptions(suppress=True)

    # 모델 로드
    model = tensorflow.keras.models.load_model('./note_model/staff_224.h5')

    # 타겟 사이즈 224 X 224 
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    notelist_path = '/Users/zjisuoo/Documents/학교/OurChord/Code/02_DEEPLEARNING/test_data/'
    onlyfiles = [f for f in listdir(notelist_path) if isfile(join(notelist_path, f))]
    onlist = []
    for i in range(len(onlyfiles)):
        onlyfiles[i] = onlyfiles[i].replace(".png", "")
        onlyfiles[i] = onlyfiles[i].replace(".PNG", "")
        onlist.append(int(onlyfiles[i]))
    onlist.sort()

    for i in range(len(onlist)):
        onlyfiles[i] = str(onlist[i]) + '.png'

    print(onlyfiles)

    image = np.empty(len(onlyfiles), dtype = object)
    notelist = []
    for item in range(0, len(onlyfiles)) :
        image[item] = Image.open(join(path_dir+onlyfiles[item])).convert('RGB')
        
        image[item] = image[item].resize((224, 224))
        image[item] = ImageOps.fit(image[item], (224, 224), Image.ANTIALIAS, centering = (0.5, 0.5))

        image_array = np.array(image[item])

        normalized_image_array = (image_array.astype(dtype = np.float32) / 127.0) - 1

        data[0] = normalized_image_array

        prediction = model.predict(data)

        if(prediction[0][0] > 0.5):
            notelist[item].insert(5,"2")
            print(onlyfiles[item]," 사진 : 2분음표")
        elif(prediction[0][1] > 0.5):
            notelist[item].insert(5,"2")
            print(onlyfiles[item]," 사진 : 2분음표")
        elif(prediction[0][2] > 0.5):
            notelist[item].insert(5,"4")
            print(onlyfiles[item]," 사진 : 4분음표")
        elif(prediction[0][3] > 0.5):
            notelist[item].insert(5,"4")
            print(onlyfiles[item]," 사진 : 4분음표")
        elif(prediction[0][4] > 0.5):
            notelist[item].insert(5,"8")
            print(onlyfiles[item]," 사진 : 8분음표")
        elif(prediction[0][5] > 0.5):
            notelist[item].insert(5,"8")
            print(onlyfiles[item]," 사진 : 8분음표")
        else:
            notelist[item].insert(5,"NONE")
            print("음표아님")
