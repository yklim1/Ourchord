import tensorflow.keras
from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2

np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('./note_model/NOTE_B_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

path_dir = '/Users/zjisuoo/Documents/zjisuoo_git/OurChord/02_DEEPLEARNING/test/'
onlyfiles = [f for f in listdir(path_dir) if isfile(join(path_dir, f))]

image = np.empty(len(onlyfiles), dtype = object)

for item in range(0, len(onlyfiles)) :
    #image[item] = cv2.imread(join(path_dir, onlyfiles[item]))
    image[item] = Image.open(join(path_dir+onlyfiles[item])).convert('RGB')
    print(path_dir+onlyfiles[item])
    print((item + 1), '번째 Note')
    #print(onlyfiles[item])
    print(image[item])
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    
    image[item] = image[item].resize((224, 224))
    image[item] = ImageOps.fit(image[item], (224, 224), Image.ANTIALIAS, centering = (0.5, 0.5))

    #turn the image int a numpy array
    image_array = np.array(image[item])

    # Normalize the image
    normalized_image_array = (image_array.astype(dtype = np.float32) / 127.0) - 1

    image[item].show()
    image[item].save(f'./{item}.png')
    # Load the image into the array
    data[0] = normalized_image_array
    # data[0] = image_array

    # run the inference\
    prediction = model.predict(data)
    print(prediction)
    print(f"{item}번째")

    if(prediction[0][0] > 0.5):
        print("2분음표")
    elif(prediction[0][1] > 0.5):
        print("4분음표")
    elif(prediction[0][2] > 0.5):
        print("8분음표")
    elif(prediction[0][3] > 0.5):
        print("16분음표")
    else:
        print("음표아님")
