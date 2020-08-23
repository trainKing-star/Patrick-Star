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
        transforms.Resize((64,64)),
        transforms.ToTensor()
    ]
)
def showTorchImage(image):
    mode = transforms.ToPILImage()(image)
    plt.imshow(mode)
    plt.show()
path = os.path.join('./train/train/cat.0' + '.jpg' )
fopen = Image.open(path)
data = transform(fopen)
showTorchImage(data)
print(data.size())
image = data.view(1,3,64,64).cuda()
print('开始')
st = time.time()

#%%

for i in range(1,12500):
    path = os.path.join('./train/train/cat.' + str(i) + '.jpg' )
    fopen = Image.open(path)
    data = transform(fopen)
    data = data.view(1,3,64,64).cuda()
    image = torch.cat((image,data),0)
    if i % 1000 == 0:
        print('进行'+str(i)+'次')

#%%

for i in range(0,12500):
    path = os.path.join('./train/train/dog.' + str(i) + '.jpg' )
    fopen = Image.open(path)
    data = transform(fopen)
    data = data.view(1,3,64,64).cuda()
    image = torch.cat((image,data),0)
    if i % 1000 == 0:
        print('进行'+str(i)+'次')

#%%

print(time.time()-st)

#%%

print(image.size())

#%%

train_y1=torch.zeros(12500)
train_y2=torch.ones(12500)
train_y=torch.cat((train_y1,train_y2),0)
print(train_y.size(),image.size(),train_y)

#%%

import h5py
f=h5py.File('train_res_dataset.h5',"w")
dset1=f.create_dataset('train_y',data=train_y)
dset2=f.create_dataset('train_x',data=image.cpu())
print(dset1.shape)
print(dset2.shape)
f.close()

#%%

showTorchImage(image[0].cpu())
showTorchImage(image[1].cpu())

#%%

test_dataset=h5py.File('train_res_dataset.h5','r')
test_x=test_dataset['train_x'][:]
test_y=test_dataset['train_y'][:]
print(test_x.shape,test_y.shape)
test_x=torch.FloatTensor(test_x)
showTorchImage(test_x[12499])
showTorchImage(test_x[12499+12500])
print(test_y[12499])
print(test_y[12499+12500])

#%%

test_dataset.close()

#%%


