from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2

path_dir = '/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/NOTE_B/TestData/Test'
onlyfiles = [f for f in listdir(path_dir) if isfile(join(path_dir, f))]

image = np.empty(len(onlyfiles), dtype = object)

for item in range(0, len(onlyfiles)) :
    image[item] = cv2.imread(join(path_dir, onlyfiles[item]))
    print((item + 1), '번째 Note')
    image_array = np.array(image)
    # image.show()

    print(onlyfiles[item])
