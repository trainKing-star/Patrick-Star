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
optimizer = torch.optim.Adam(net.parameters(), lr=0.001)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10, verbose=True,
                                                       threshold=0.0001, threshold_mode='rel', cooldown=0, min_lr=0,
                                                       eps=1e-08)
loss_func = nn.CrossEntropyLoss()

# %%

import h5py


def load_dataset():
    train_dataset = h5py.File('test_500_dataset.h5', 'r')
    train_x = train_dataset['test_x'][:]
    train_y = train_dataset['test_y'][:]
    train_x = torch.FloatTensor(train_x)
    train_y = torch.LongTensor(train_y)
    return train_x, train_y


train_x, train_y = load_dataset()
print(train_x.size(), train_y.size(), train_y)

# %%

for epoch in range(2000):
    output = net(train_x.cuda())
    loss = loss_func(output, train_y.cuda()).cuda()
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step(loss)
    if epoch % 10 == 0:
        print('第' + str(epoch) + '次成本:' + str(loss))

    # %%

torch.save(net.state_dict(), 'params_res_true_train2.pkl')
print('保存成功')

# %%

torch.save(net.state_dict(), 'params_res_true_train2_two.pkl')
print('保存成功')
