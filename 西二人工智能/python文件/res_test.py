# %%

import torch
import torch.nn as nn


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.block = {}
        self.start = nn.Sequential(
            nn.Conv2d(3, 64, 7, 2, 3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, 2, 1)
        )

        self.a1_1, self.b1_1 = self.Residual(64, 64, 3, 1)
        self.a1_2, self.b1_2 = self.Residual(64, 64, 3, 1)
        self.a1_3, self.b1_3 = self.Residual(64, 64, 3, 1)

        self.a2_1, self.b2_1 = self.Residual(64, 128, 3, 2)
        self.a2_2, self.b2_2 = self.Residual(128, 128, 3, 1)
        self.a2_3, self.b2_3 = self.Residual(128, 128, 3, 1)
        self.a2_4, self.b2_4 = self.Residual(128, 128, 3, 1)

        self.a3_1, self.b3_1 = self.Residual(128, 256, 3, 2)
        self.a3_2, self.b3_2 = self.Residual(256, 256, 3, 1)
        self.a3_3, self.b3_3 = self.Residual(256, 256, 3, 1)
        self.a3_4, self.b3_4 = self.Residual(256, 256, 3, 1)
        self.a3_5, self.b3_5 = self.Residual(256, 256, 3, 1)
        self.a3_6, self.b3_6 = self.Residual(256, 256, 3, 1)

        self.a4_1, self.b4_1 = self.Residual(256, 512, 3, 2)
        self.a4_2, self.b4_2 = self.Residual(512, 512, 3, 1)
        self.a4_3, self.b4_3 = self.Residual(512, 512, 3, 1)

        self.relu = nn.ReLU(inplace=True)
        self.avg = nn.AdaptiveAvgPool2d(1)
        self.linear = nn.Linear(512, 2)

    def forward(self, x):
        x = self.start(x)

        x = self.Block(self.a1_1, self.b1_1, x)
        x = self.Block(self.a1_2, self.b1_2, x)
        x = self.Block(self.a1_3, self.b1_3, x)

        x = self.Block(self.a2_1, self.b2_1, x)
        x = self.Block(self.a2_2, self.b2_2, x)
        x = self.Block(self.a2_3, self.b2_3, x)
        x = self.Block(self.a2_4, self.b2_4, x)

        x = self.Block(self.a3_1, self.b3_1, x)
        x = self.Block(self.a3_2, self.b3_2, x)
        x = self.Block(self.a3_3, self.b3_3, x)
        x = self.Block(self.a3_4, self.b3_4, x)
        x = self.Block(self.a3_5, self.b3_5, x)
        x = self.Block(self.a3_6, self.b3_6, x)

        x = self.Block(self.a4_1, self.b4_1, x)
        x = self.Block(self.a4_2, self.b4_2, x)
        x = self.Block(self.a4_3, self.b4_3, x)

        x = self.avg(x)

        x = self.linear(x.view(x.size()[0], -1))

        return x

    def Residual(self, C_in, C_out, size, stride):
        over = nn.Sequential(
            nn.Conv2d(C_in, C_out, size, stride, 1),
            nn.BatchNorm2d(C_out),
            nn.ReLU(inplace=True),
            nn.Conv2d(C_out, C_out, size, 1, 1),
            nn.BatchNorm2d(C_out)
        )
        if C_in != C_out:
            change = nn.Sequential(
                nn.Conv2d(C_in, C_out, 1, stride),
                nn.BatchNorm2d(C_out)
            )
        else:
            change = nn.Sequential()
        return over, change

    def Block(self, a, b, x):
        out = a(x)
        x = b(x)
        x = self.relu(x + out)
        return x


net = Net().cuda()
print(net)
net.load_state_dict(torch.load('params_res_train.pkl'))

# %%

import numpy as np
import h5py
import torch.utils.data as Data


def load_dataset(file, x, y):
    test_dataset = h5py.File(file, 'r')
    test_x = test_dataset[x][:]
    test_y = test_dataset[y][:]
    test_x = torch.FloatTensor(test_x)
    test_y = torch.LongTensor(test_y)
    return test_x, test_y


def practice(x, y):
    test_out = torch.softmax(net(x), 1)
    end = torch.max(test_out.cpu(), 1)[1].numpy()
    print('精确率：' + str(np.sum(end == y.numpy()) / end.shape[0]))


test_x, test_y = load_dataset('../test_500_dataset.h5', 'test_x', 'test_y')
train_dataset = Data.TensorDataset(test_x, test_y)
train_loader = Data.DataLoader(
    dataset=train_dataset,
    batch_size=1,
    shuffle=False,
    pin_memory=True,
    num_workers=4
)
k = 0
for step, (b_x, b_y) in enumerate(train_loader):
    test_out = torch.softmax(net(b_x.cuda()), 1)
    test_out = torch.max(test_out, 1)[1]
    k = k + torch.sum(test_out.cpu() == b_y)
print(test_x.size(), test_y.size())
print("K:" + str(k.data.numpy()))
print("精确:" + str(k.data.numpy() / (test_y.size()[0])))
practice(test_x.cuda(), test_y)

# %%

import torchvision.transforms as transforms
from matplotlib import pyplot as plt
import time


def showTorchImage(image):
    mode = transforms.ToPILImage()(image)
    plt.imshow(mode)
    plt.show()


# %%

import numpy as np

test_x, test_y = load_dataset('train_res_dataset.h5', 'train_x', 'train_y')
print(test_x.size(), test_y.size())

# %%

train_dataset = Data.TensorDataset(test_x, test_y)
train_loader = Data.DataLoader(
    dataset=train_dataset,
    batch_size=1,
    shuffle=False,
    pin_memory=True,
    num_workers=4
)
i = 0
j = 0
k = 0
l = 0
cat = 0
dog = 0
for step, (b_x, b_y) in enumerate(train_loader):
    test_out = torch.softmax(net(b_x.cuda()), 1)
    test_out = torch.max(test_out, 1)[1]
    image = transforms.ToPILImage()(b_x.view(3, 64, 64))
    if step < test_y.size()[0] // 2:
        cat = cat + torch.sum(test_out.cpu() == b_y)
        '''if test_out.cpu() == b_y:
            image.save('./restrue7/train/cat.'+str(j)+'.jpg')
            j = j+1
        else:
            image.save('./reserror_cat7/train/cat.'+str(i)+'.jpg')
            i = i+1'''
    else:
        dog = dog + torch.sum(test_out.cpu() == b_y)
        '''if test_out.cpu() == b_y:
            image.save('./restrue7/train/dog.'+str(k)+'.jpg')
            k = k+1
        else:
            image.save('./reserror_dog7/train/dog.'+str(l)+'.jpg')
            l = l+1'''
print("cat:" + str(cat.data.numpy() / (test_y.size()[0] // 2)))
print("dog:" + str(dog.data.numpy() / (test_y.size()[0] // 2)))
print("cat+dpg:" + str((cat + dog).data.numpy() / (test_y.size()[0])))
print('结束')

# %%


