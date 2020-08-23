#%%

import torch
import h5py
import torchvision
import numpy as np
import time
import os
from PIL import Image
import torch.utils.data as Data
import torchvision.transforms as transforms
import torchvision.datasets as dset
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

train_dataset = dset.ImageFolder('./reserror_cat7',transform=transform)

#%%

train_loader=torch.utils.data.DataLoader(
    dataset=train_dataset,
    batch_size=1,
    shuffle=True
)
for step,(b_x,b_y) in enumerate(train_loader):
    image = transforms.ToPILImage()(b_x.view(3,64,64))
    if step < 767:
        image.save('./restrue7/train/cat.'+str(11144+step)+'.jpg')

#%%

