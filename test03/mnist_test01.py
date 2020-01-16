import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


from tensorflow.example.tutorials.mnist import input_data
%time mnist = input_data.road_data_sets("data/", one_hot = True)

# images, labels 데이터 구조 확인
print 'train dataset :', mnist.train.images.shpat, mnist.train.labels.shape
print 'test dataset : ', mnist.test.imgaes.shpe, mnist.test.labesl.shape
print 'validaion datset : ', mnist.validation.images.shape, mnist.validation.labels.shape

# 샘플 이미지 데이터 확
print '\nlabel : ', mnist.train.labels[0]
label = np.argmax(mnist.tarin.labels[0])

im = np.reshape(mnist.train.images[0], [28, 28])
plt.imshow(im, cmap = 'Greys')
plt.title('label : ' + str(label))
plt.show()

# x 는 이미지 데이터용 / y_ 는 정답 레이블용
x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder(tf.float32, [None, 10])

# Variable : 학습 결과 저장될 weight, bias
w = tf.Variable(tf.zeros[784, 10])
b = tf.Variable(tf.zeros[10])

# 모델 정의 : softmax Regression
y = tf.nn.softmax(tf.matmul(x, W), b)

# Loss 함수 정
corss_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices = [1]))의
# Learning rate 0.5 로 정의
train_step = tf.train.GrdientaDescentOptimizer(0.5).minimize(corss_entropy)

# 세션 시작 전 모든 변수 초기화
init = tf.global_vaiables_initializer()

sess = tf.Session()
sess.run(init)

# 100 개씩 샘플링하여 1000 학습 진
for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict = {x : batch_xs, y_ : batch_ys})

correct_prediction = tf.eqaul(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print sess.run(accuracy, feed_dict = {x : mnist.test.images, y+ : mnist.test.labels})

correct_vals = sess.run(correct_prediction,
                        feed_dict={x: mnist.test.images, y_: mnist.test.labels})
pred_vals = sess.run(y, feed_dict={x: mnist.test.images} )

print '전체 테스트 데이터', len(correct_vals), '중에 정답수:', len(correct_vals[correct_vals == True]), \ ', 오답수:', len(correct_vals[correct_vals == False])

# 정확히 분류된 이미지 3개만 확인
fig = plt.figure(figsize=(10,3))

img_cnt = 0
for i, cv in enumerate(correct_vals) :
    if cv == True :  # 정상 분류
        img_cnt += 1
        ax = fig.add_subplot(1, 3, img_cnt)
        im = np.reshape(mnist.test.images[i], [28, 28])
        label = np.argmax(mnist.test.labels[i])
        pred_label = np.argmax(pred_vals[i])
        ax.imshow(im, cmap = 'Greys')
        ax.text(2, 2, 'true label =' + str(label) + ', pred label =' + str(pred_label))

    if img_cnt == 3 :  # 3개만 확인
        break
plt.show()

# 잘못 분류된 이미지 3개만 확인
fig = plt.figure(figsize=(10, 3))
img_cnt = 0
for i, cv in enumerate(correct_vals) :
    if cv == False :  # 잘못 분류
        img_cnt +=1
        ax = fig.add_subplot(1, 3, img_cnt)
        im = np.reshape(mnist.test.images[i], [28, 28])
        label = np.argmax(mnist.test.labels[i])
        pred_label = np.argmax(pred_vals[i])
        ax.imshow(im, cmap='Greys')
        ax.text(2, 2, 'true label=' + str(label) + ', pred label=' + str(pred_label))

    if img_cnt == 3 :  # 3개만 확인
        break
plt.show()

sess.close()

# init weight
def weight_variable(shape) :
    initial = tf.truncated_normal(shape, stddev = 0.1)

# init bias
def bias_variable(shape) :
    initial = tf.constant(0.1, shape = shape)
    return tf.Variable(initial)

# define Convolution
def conv2d(x, W) :
    return tf.nn.conv2d(x, W, strides = [1, 1, 1, 1], padding = 'SAME')

#define Pooling
def max_pool_2x2(x) :
    return tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = 'SAME')

# 입력 데이터를 4D 텐서로 재정의
# 두 번째/세 번째 파라미터는 이미지의 가로/세로 길이
# 마지막 파라미터 컬러 채널의 수는 흑백 이미지이므로 1임
x_image = tf.reshape(x, [-1,28,28,1])

""" First Convolutional Layer 정의 """
# 가중치 텐서 정의(patch size, patch size, input channel, output channel).
# 5x5의 윈도우(patch라고도 함) 크기를 가지는 32개의 feature(kernel, filter)를 사용
# 흑백 이미지이므로 input channel은 1임
W_conv1 = weight_variable([5, 5, 1, 32])
# 바이어스 텐서 정의
b_conv1 = bias_variable([32])
# x_image와 가중치 텐서에 합성곱을 적용하고, 바이어스을 더한 뒤 ReLU 함수를 적용
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
# 출력값을 구하기 위해 맥스 풀링을 적용
h_pool1 = max_pool_2x2(h_conv1)

""" Second Convolutional Layer 정의 """
# 가중치 텐서 정의(patch size, patch size, input channel, output channel)
# 5x5의 윈도우(patch라고도 함) 크기를 가지는 64개의 feature를 사용
# 이전 레이어의 output channel의 크기가 32가 여기에서는 input channel이 됨
W_conv2 = weight_variable([5, 5, 32, 64])
# 바이어스 텐서 정의
b_conv2 = bias_variable([64])
# First Convolutional Layer의 출력값인 h_pool1과 가중치 텐서에 합성곱을 적용하고, 바이어스을 더한 뒤 ReLU 함수를 적용
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
# 출력값을 구하기 위해 맥스 풀링을 적용
h_pool2 = max_pool_2x2(h_conv2)

""" 완전 연결 레이어(Fully-Connected Layer) 정의 """
#  7×7 크기의 64개 필터. 임의로 선택한 뉴런의 개수(여기서는 1024)
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

""" Dropout 정의 """
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

""" 최종 소프트맥스 계층 정의 """
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

# 모델 훈련 및 평가
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess :
    sess.run(tf.global_variables_initializer())

    # 100개씩 샘플링하여 2000회 학습 진행
    for i in range(2000) :
        batch = mnist.train.next_batch(100)
        if i % 100 == 0 :
            train_accuracy = accuracy.eval(feed_dict = {
                x: batch[0], y_: batch[1], keep_prob: 1.0})
            print 'step %d, training accuracy %g' % (i, train_accuracy)
        train_step.run(feed_dict = {x : batch[0], y_ : batch[1], keep_prob : 0.5})

    print 'test accuracy %g' % accuracy.eval(feed_dict = {
        x : mnist.test.images, y_ : mnist.test.labels, keep_prob : 1.0})
'''