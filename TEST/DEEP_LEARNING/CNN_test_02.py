import tensorflow.keras
from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join
import numpy as np
import glob
import cv2

np.set_printoptions(suppress = True)

# Load the model
model = tensorflow.keras.models.load_model('./converted_keras/keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape = (1, 224, 224, 3), dtype = np.float32)

path = glob.glob("/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/TEST/*.png")
images = []

for image in path :
    n1 = cv2.imread(image)
    n2 = cv2.resize(n1, (244, 244))
    images.append(n2)

    print(image)

#turn the image int a numpy array
image_array = np.array(n2)

# Normalize the image
normalized_image_array = (image_array.astype(dtype = np.float32) / 127.0) - 1

# Load the image into the array
data = normalized_image_array

# run the inference
prediction = model.predict(data)
# print(prediction)

if(prediction[0][0] > 0.8):
    print("2분음표")
elif(prediction[0][1] > 0.8):
    print("4분음표")
elif(prediction[0][2] > 0.8):
    print("8분음표")
elif(prediction[0][3] > 0.8):
    print("16분음표")
else:
    print("음표아님")