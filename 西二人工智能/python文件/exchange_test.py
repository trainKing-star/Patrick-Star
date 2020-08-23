#%%

import torch
import h5py
import torchvision
import numpy as np
import time
import os
from PIL import Image
import torchvision.transforms as transforms
from matplotlib import pyplot as plt
transform = transforms.Compose(
    [
        transforms.Resize(64),
        transforms.CenterCrop(64),
        transforms.ToTensor()
    ]
)
def showTorchImage(image):
    mode = transforms.ToPILImage()(image)
    plt.imshow(mode)
    plt.show()
path = os.path.join('./test_500/test/1' + '.jpg' )
fopen = Image.open(path)
data = transform(fopen)
image = data.view(1,3,64,64).cuda()
print('开始')
st = time.time()

#%%

for i in range(1,500):
    path = os.path.join('./test_500/test/' + str(i+1) + '.jpg' )
    fopen = Image.open(path)
    data = transform(fopen)
    data = data.view(1,3,64,64).cuda()
    image = torch.cat((image,data),0)
    if i % 10 == 0:
        print('进行'+str(i)+'次')

#%%

print(time.time()-st)

#%%

print(image.size())

#%%

import pandas as pd
train_y=pd.read_csv('test_500_label.csv')
train_y=np.array(train_y)
train_y=train_y[:,1].reshape(-1)
print(train_y)

#%%

import h5py
f=h5py.File('test_true_dataset.h5',"w")
dset1=f.create_dataset('test_y',data=train_y)
dset2=f.create_dataset('test_x',data=image.cpu())
print(dset1.shape)
print(dset2.shape)

#%%

showTorchImage(image[0].cpu())
showTorchImage(image[1].cpu())

#%%

test_dataset=h5py.File('test_true_dataset.h5','r')
test_x=test_dataset['test_x'][:]
test_y=test_dataset['test_y'][:]
print(test_x.shape,test_y.shape)
test_x=torch.FloatTensor(test_x)
showTorchImage(test_x[368])
showTorchImage(test_x[25])
print(test_y[368])
print(test_y[25])

#%%


