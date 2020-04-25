# 파일 정렬 완료 -> 모델 학습 더시켜야 됨!!!
import tensorflow.keras
from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join
from operator import itemgetter
import numpy as np
import cv2

np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('./note_model/note_staff_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

path_dir = '/Users/zjisuoo/Documents/zjisuoo_git/OurChord/02_DEEPLEARNING/vscode_3/'
onlyfiles = [f for f in listdir(path_dir) if isfile(join(path_dir, f))]
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

    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    
    image[item] = image[item].resize((224, 224))
    image[item] = ImageOps.fit(image[item], (224, 224), Image.ANTIALIAS, centering = (0.5, 0.5))

    # turn the image int a numpy array
    image_array = np.array(image[item])

    # Normalize the image
    normalized_image_array = (image_array.astype(dtype = np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)

    if(prediction[0][0] > 0.5):
        print(onlyfiles[item]," 사진 : 2분음표")
    elif(prediction[0][1] > 0.5):
        print(onlyfiles[item]," 사진 : 2분음표")
    elif(prediction[0][2] > 0.5):
        print(onlyfiles[item]," 사진 : 4분음표")
    elif(prediction[0][3] > 0.5):
        print(onlyfiles[item]," 사진 : 4분음표")
    elif(prediction[0][4] > 0.5):
        print(onlyfiles[item]," 사진 : 8분음표")
    elif(prediction[0][5] > 0.5):
        print(onlyfiles[item]," 사진 : 8분음표")
    else:
        print("음표아님")
