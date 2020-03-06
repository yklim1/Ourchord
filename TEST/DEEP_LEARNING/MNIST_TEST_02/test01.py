import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator

np.random.seed(3)

# 데이터 생성
train_datagen = ImageDataGenerator(rescale = 1./255)

train_generator = train_datagen.flow_from_directory(
    './score/train',
    target_size = (24, 24),
    batch_size = 3,
    class_mode = 'categorical')

test_datagen = ImageDataGenerator(rescale = 1./255)

test_generator = test_datagen.flow_from_directory(
    './score/test',
    target_size = (24, 24),
    batch_size = 3,
    class_mode = 'categorical')

# 모델 구성
model = Sequential()
model.add(Conv2D(32, kernel_sizㅡe = (3, 3),
                 activation = 'relu',
                 input_shape = (24, 24, 3)))
model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Flatten())
model.add(Dense(128, activation = 'relu'))
model.add(Dense(3, activation = 'softmax'))

# 모델 학습 과정 설정
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

# 모델 학습
model.fit_generator(
    train_generator,
    steps_per_epoch = 5,
    epochs = 50,
    validation_data = test_generator,
    validation_steps = 5)

# 모델 평가
print(" -- EVALUATE -- ")
scores = model.evaluate_generator(test_generator, steps = 5)
print("%s : %.2f%%" %(model.metrics_names[1], scores[1]*100))

# 모델 사용
print(" -- PREDICT -- ")
output = model.predict_generator(test_generator, steps = 5)
np.set_printoptions(formatter = {'float' : lambda x : "{0:0.3f}".format(x)})
print(test_generator.class_indices)
print(output)
