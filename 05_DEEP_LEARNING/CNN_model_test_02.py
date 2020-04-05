import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator

# 데이터 생성
train_datagen = ImageDataGenerator(rescale = 1./255)

train_generator = train_datagen.flow_from_directory(
    './Note/TrainingData',
    target_size = (24, 24),
    batch_size = 4,
    class_mode = 'categorical')

test_datagen = ImageDataGenerator(rescale = 1./255)

test_generator = test_datagen.flow_from_directory(
    './Note/TestData',
    target_size = (24, 24),
    batch_size = 4,
    class_mode = 'categorical')

# 모델 구성
model = Sequential()
model.add(Conv2D(32, kernel_size = (3, 3),
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
    # training data/batch size = steps_per_epoch
    steps_per_epoch = 240,
    epochs = 100,
    validation_data = test_generator,
    # test data/batch size = validation_steps
    validation_steps = 60)

# 모델 평가
print(" -- EVALUATE -- ")
scores = model.evaluate_generator(test_generator, steps = 60)
print("%s : %.2f%%" %(model.metrics_names[0], scores[0]*100))
print("%s : %.2f%%" %(model.metrics_names[1], scores[1]*100))

# 모델 사용
print(" -- PREDICT -- ")
output = model.predict_generator(test_generator, steps = 60)
np.set_printoptions(formatter = {'float' : lambda x : "{0:0.4f}".format(x)})
print(test_generator.class_indices)
print(output)

print(test_generator.filenames)