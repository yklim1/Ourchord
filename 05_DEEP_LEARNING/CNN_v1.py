import tensorflow.keras
from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('./converted_keras/keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

path_dir = '/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/NOTE_B/TestData/Test'
onlyfiles = [f for f in listdir(path_dir) if isfile(join(path_dir, f))]

image = np.empty(len(onlyfiles), dtype = object)

for item in range(0, len(onlyfiles)) :
    image[item] = cv2.imread(join(path_dir, onlyfiles[item]))
    print((item + 1), '번째 Note')
    print(onlyfiles[item])
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    # size = (224, 224)
    image = ImageOps.fit(image, (224, 224), Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.array(onlyfiles[item])

    # display the resized image
    # image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(dtype = object) / 127.0) - 1

    # Load the image into the array
    data = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(prediction)

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

