from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.optimizers import SGD
from tensorflow.python.keras import backend as K
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from PIL import Image, ImageOps, ImageFile
from collections import Counter
import json
import random

import numpy as np
import os
import pickle
import sys
import cv2


dim = 105
label_dict = pickle.load(open('E:\\FontRecognition\\App\\Model\\label_dict','rb'))
font_dict = pickle.load(open('E:\\FontRecognition\\App\\Model\\font_dict','rb'))

def pil_image(img_path):
    pil_im = Image.open(img_path).convert('L')
#     imshow(np.asarray(pil_im))
    return pil_im

# Randomly Crop 105 x  105 within the area.
# Creating 15 randomly cropped from image.
def crop(pil_img):
    num_of_crop = 15
    width, height = pil_img.size
    left = 0
    right = dim
    top = 0
    bottom = dim
    cropped_imgs = []

    for _ in range(num_of_crop):
        img = pil_img.crop((left, top, right, bottom))
        cropped_imgs.append(img)
        left = random.randint(0, width)
        right = left + dim
    return cropped_imgs

def squeezing_operation(pil_img):
    baseheight = 105
    hpercent = (baseheight/float(pil_img.size[1]))
    wsize = int((float(pil_img.size[0])*float(hpercent)))
    temp_img = pil_img.resize((wsize,baseheight), Image.ANTIALIAS)
    return temp_img

def crop_resize(pil_img):
    (width, height) = pil_img.size
    img = crop(squeezing_operation(pil_img))
    return img

def load_cnn():
    def get_lr_metric(optimizer):
        def lr(y_true, y_pred):
            return optimizer.lr
        return lr
    def recall(y_true, y_pred):
        y_true = K.ones_like(y_true) 
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        all_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (all_positives + K.epsilon())
        return recall
    def precision(y_true, y_pred):
        y_true = K.ones_like(y_true) 
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    cnn_name = 'DeepFont_5'
    cnn = load_model(f'E:\\FontRecognition\\App\\Model\\{cnn_name}.h5', custom_objects={'lr':get_lr_metric(SGD()), 'precision':precision, 'recall':recall})
    return cnn

def get_label(val):
    for key, value in label_dict.items(): 
      if val == value: 
        return key
    return "key doesn't exist"

def get_fontfile(val):
    return font_dict[val]

picture_path = str(sys.argv[1])
# picture_path = "C:\\Users\\bobby\\Desktop\\Annotation 2020-03-29 004335.png"
print("Picture Path : ", picture_path)
# Preprocessing
img = pil_image(picture_path)
img = crop_resize(img)
cropped_img = []
cropped_img.extend(img)
x = []
for img in cropped_img:
    img_cv2 = np.array(img)
    x.append(img_cv2)
print(f"Processed image result {len(x)}")
print(f"sample \n {x[0].shape}")

# Normalize
x = np.array(x).reshape(-1, 105, 105, 1)
x = x / 255.0
print("Shape of x : ", x.shape)

# Load model
model = load_cnn()
# Predict
result = model.predict_classes(x)
# sort all prediction from the common one to less common
sorted_result = [key for key, count in sorted(Counter(result).most_common(), key=lambda tup : tup[1], reverse=True)]
# Result -- All Top predictions
print("Result ini : ", result)
print("Result sorted : ", sorted_result)
label = [get_label(item) for item in sorted_result]
font_files = [get_fontfile(item) for item in label]
print("Result font_file : ", font_files)
# Result -- 1 highest font
# result = np.bincount(result).argmax()
# print("Result 2 : ", result)
# Convert it to label name
# label = get_label(result)

print("#",label)
print("#",font_files)