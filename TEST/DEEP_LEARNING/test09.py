import sys, os
sys.path.append(os.pardir)
import numpy as np
import matplotlib.pyplot as plt
from dataset.mnist import load_mnist
from simple_convnet import SimpleConvNet
from common.trainer import Trainer


(x_train, t_train), (x_test, t_test) = load_mnist(flatten = False)

x_train, t_train = x_train[:5000], t_train[:5000]
x_test, t_test = x_test[:1000], t_test[:1000]

network = SimpleConvNet(input_dim = (1, 28, 28), conv_param = {'filter_num':30, 'filter_size =':5, 'pad':0, 'stride':1}, hidden_size=100, output_size=10,weight_init_std=0.01)

trainer = Trainer(network, x_train, t_train, x_test, t_test, epochs = max_epochs, mini_batch_size = 100, optimizer = 'Adam', optimizer_param = {'lr':0.001}, evaluate_saple_num_per_epoch = 1000)
trainer.train()

network.save_params("param.pkl")
print("Saved Network Parameters!")

markers = {'train':'o', 'test':'s'}
x=np.arange(max_epochs)
plt.plot(x, trainer.train_acc_list, markers='o', label='train', markevery=2)
plt.plot(x, trainer.test_acc_list, markers='s', label='test', markevery=2)
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.ylim(0, 1.0)
plt.legend(loc='lower right')
plt.show()

def filter_show(filters, nx=8, margin=3, scale=10):
    FN, C, FH, FW = filters.shape
    ny = int(np.ceil(FN/nx))

    fig = plt.figure()
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)

    for i in range(FN):
        ax = fig.add_subplot(ny, nx, i+1, xticks=[], yticks=[])
        ax.imshow(filters[i, 0], cmap = plt.cm.gray_r, interpolation='nearest')
    plt.show()

network = SimpleConvNet()
filter_show(network.params['W1'])

network.load_params("params.pkl")
filter_show(network.params['W1'])