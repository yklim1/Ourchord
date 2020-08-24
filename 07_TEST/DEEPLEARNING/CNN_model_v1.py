import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
# from IPython.display import SVG
# from keras.utils.vis_utils import model_to_dot
from tensorflow.keras.utils import plot_model

np.random.seed(4)

train_datagen = ImageDataGenerator(rescale = 1./255)

train_generator = train_datagen.flow_from_directory(
    '/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/NOTE_B/TrainingData',
    target_size = (224, 224),
    batch_size = 4,
    class_mode = 'categorical')

test_datagen = ImageDataGenerator(rescale = 1./255)

test_generator = test_datagen.flow_from_directory(
    '/Users/zjisuoo/Documents/zjisuoo_git/OurChord/00_NOTE_DATA/NOTE_B/TestData',
    target_size = (224, 224),
    batch_size = 4,
    class_mode = 'categorical')

# 모델 구성
model = Sequential()

# 입력 이미지 크기 24 X 24, 입력 이미지 채널 3 개 
# Conv 이미지 특징 추출
# Pooling 추출한 이미지 선명하게 함 / MaxPooling 컨볼루션 데이터에서 가장 큰 값 대표값으로 선정
model.add(Conv2D(32, kernel_size = (3, 3),
                activation = 'relu',
                input_shape = (224, 224, 3)))
model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Flatten())
model.add(Dense(128, activation = 'relu'))
model.add(Dense(4, activation = 'softmax'))

# 모델 시각화
# SVG(model_to_dot(model, show_shapes = True).create(prog = 'dot', format ='svg'))
plot_model(model, to_file = 'model.png')
plot_model(model, to_file = 'model_shapes.png', show_shapes = True)

# 모델 학습과정 설정
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

# 모델 학습2
model.fit_generator(train_generator, 
                    steps_per_epoch = 240,
                    epochs = 100,
                    validation_data = test_generator,
                    validation_steps = 60)

# 모델 평가
print("MODEL EVALUATE")
scores = model.evaluate_generator(test_generator, steps = 60)
print("%s : %.2f%%" % (model.metrics_names[1], scores[1]*100))

# 모델 저장
model.save('NOTE_B_model_224.h5')