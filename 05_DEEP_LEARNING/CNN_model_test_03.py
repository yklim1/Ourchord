from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense

# dimensions of our images.
train_data_dir = 'Note/TrainingData'
validation_data_dir = 'Note/TestData'
nb_train_samples = 960
nb_validation_samples = 240
nb_epoch = 50
model = Sequential()
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(train_data_dir,
                                                    target_size = (24, 24),
                                                    batch_size = 32,
                                                     class_mode = 'categorical')
validation_generator = test_datagen.flow_from_directory(validation_data_dir,
                                                        target_size = (24, 24),
                                                        batch_size = 32,
                                                        class_mode = 'categorical')
model.fit_generator(train_generator,
                    samples_per_epoch = nb_train_samples,
                    nb_epoch = nb_epoch,
                    validation_data = validation_generator,
                    nb_val_samples = nb_validation_samples)
