import os
import numpy as np
import random
import torch
import torchvision
import cv2
from torch.utils import data
import glob

class DataSet(data.Dataset):
    def __init__(self, root, train=True, mean=(128, 128, 128), mirror=True, ignore_label=255):
        self.root = root
        self.mean = mean
        self.mirror = mirror
        self.ignore_label = ignore_label

        self.train = train

        if self.train == True:
            self.image_dir = os.path.join(self.root, 'leftImg8bit/train/')
            self.label_dir = os.path.join(self.root, 'gtFine/train/')
        else:
            self.image_dir = os.path.join(self.root, 'leftImg8bit/val/')
            self.label_dir = os.path.join(self.root, 'gtFine/val/')

        self.image_paths = glob.glob(self.image_dir + '*/*.png')
        self.label_paths = glob.glob(self.label_dir + '*/*_gtFine_labelIds.png')

        self.image_paths.sort()
        self.label_paths.sort()

        self.id_to_trainid = {-1: ignore_label, 0: ignore_label, 1: ignore_label, 2: ignore_label,
                              3: ignore_label, 4: ignore_label, 5: ignore_label, 6: ignore_label,
                              7: 0, 8: 1, 9: ignore_label, 10: ignore_label, 11: 2, 12: 3, 13: 4,
                              14: ignore_label, 15: ignore_label, 16: ignore_label, 17: 5,
                              18: ignore_label, 19: 6, 20: 7, 21: 8, 22: 9, 23: 10, 24: 11, 25: 12, 26: 13, 27: 14,
                              28: 15, 29: ignore_label, 30: ignore_label, 31: 16, 32: 17, 33: 18}

    def id2trainId(self, label):
        label_copy = label.copy()
        for k, v in self.id_to_trainid.items():
            label_copy[label == k] = v
        return label_copy

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):
        image = cv2.imread(self.image_paths[index], cv2.IMREAD_COLOR)
        label = cv2.imread(self.label_paths[index], cv2.IMREAD_GRAYSCALE)

        image = np.asarray(image, np.float32)
        label = np.asarray(label, np.float32)

        image -= self.mean
        label = self.id2trainId(label)

        image = image.transpose((2, 0, 1))

        if self.mirror:
            flip = np.random.choice(2) * 2 - 1
            image = image[:, :, ::flip]
            label = label[:, ::flip]

        return image.copy(), label.copy()