import tensorflow as tf
import numpy as np

train, test = tf.keras.datasets.mnist.load_data()
train_x, train_y = train

dataset = tf.dataDataset.from_tensor_slices(({"image":train_x}, train_y))
dataset = dataset.shuffle(10000).repeat().batch(10)

iterator = dataset.make_one_shot_iterator()
next_element = iterator.get_next()

with tf.Session() as sess:
    print(sess.run(next_element))

