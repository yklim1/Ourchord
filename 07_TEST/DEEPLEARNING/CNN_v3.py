import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
# .h5 오선o
model = tensorflow.keras.models.load_model('/home/ec2-user/Ourchord/DEEP/no_staff_224_c.h5', compile=False)

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape = (1, 24, 24, 3), dtype = np.float32)

# Replace this with the path to your image
image = Image.open('/home/ec2-user/Ourchord/NOTE/noteimg/note4_1.png').convert('RGB')
#image = cv2.imread('/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/TEST/note8_2.png',0)
#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
size = (24, 24)
image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
image_array = np.asarray(image)

# display the resized image
image.show()

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
data[0] = normalized_image_array
print("111111",data[0])
print("2222",data)

'''
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
