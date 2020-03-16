#!/usr/bin/env python
# coding: utf-8

# In[8]:


# get_ipython().system('pip install Pillow')
# get_ipython().system('pip install opencv-python')


# In[2]:


from pathlib import Path
from PIL import Image, ImageOps, ImageFile
import os, errno
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from matplotlib import gridspec
import matplotlib.image as mpimg
import numpy as np
import cv2, math
from shutil import copy

import concurrent.futures
from multiprocessing import Value
import time
# get_ipython().run_line_magic('matplotlib', 'inline')


# In[15]:
REAL_DATASET = 'Dataset_Final\\real_500'
DATASET_3_500 = 'Dataset_Final\\Dataset_3_500_2'

REAL_TRAIN_DATASET = 'preprocessed\\real_train_500_2'
SYN_TRAIN_DATASET = 'preprocessed\\syn_train_500_2'

FILE_LIMIT = 5
DIR_LIMIT = 2

file_path = Path('E:\FontRecognition')
dataset_path = file_path.joinpath('Dataset_Final')

real_train_dataset = dataset_path.joinpath(REAL_TRAIN_DATASET) 
syn_train_dataset = dataset_path.joinpath(SYN_TRAIN_DATASET)

# # Defining locations

# In[4]:


#Data files
dataset3_500_path = file_path.joinpath(DATASET_3_500)
realvfr_path = file_path.joinpath(REAL_DATASET)


# ## Preprocess Functions

# In[5]:

Image.MAX_IMAGE_PIXELS = 1000000000 # SILENCE PIL IMAGE COMPRESSION BOMB WARNING
ImageFile.LOAD_TRUNCATED_IMAGES = True

def pil_image(img_path):
    pil_im = Image.open(img_path).convert('L')
#     imshow(np.asarray(pil_im))
    return pil_im

dim = 105
def crop(pil_img):
    width, height = pil_img.size
    # print(f"{width, height} Cropped")
#     width = img.shape[1]
#     x0 = int(width/2 - 52.5)
#     x1= int(width/2 + 52.5)
#     y0 = int(0)
#     y1 = int(105)
#     img = img[y0:y1, x0:x1, :]
    left = 0
    right = dim
    top = 0
    bottom = dim
    cropped_imgs = []
    while(width >= dim):
        img = pil_img.crop((left, top, right, bottom)) 
        cropped_imgs.append(img)
        left += dim
        right += dim
        width -= dim
        
#     imshow(img)
    return cropped_imgs

def crop_resize(pil_img):
    (width, height) = pil_img.size
    # print(width, height)
#     if width < 105 or height < 105:
#         img = pil_img.resize((105,105), Image.ANTIALIAS)
#         print("resize")
#     elif width > 500 or height > 500:
#         # Squeezing operation
#         img = crop(squeezing_operation(pil_img))
#         print("scale down and squeeze")
#     else:
#         img = crop(pil_img)
#         print("crop")
    img = crop(squeezing_operation(pil_img))
    return img

def squeezing_operation(pil_img):
    baseheight = 105
    hpercent = (baseheight/float(pil_img.size[1]))
    wsize = int((float(pil_img.size[0])*float(hpercent)))
    temp_img = pil_img.resize((wsize,baseheight), Image.ANTIALIAS)
    return temp_img

def rgb2gray(pil_img):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def noise_image(pil_im):
    # Adding Noise to image
    img_array = np.asarray(pil_im)
    mean = 0.0   # some constant
    std = 5   # some constant (standard deviation)
    noisy_img = img_array + np.random.normal(mean, std, img_array.shape)
    noisy_img_clipped = np.clip(noisy_img, 0, 255)
    noise_img = Image.fromarray(np.uint8(noisy_img_clipped)) # output
    #imshow((noisy_img_clipped ).astype(np.uint8))
    noise_img=noise_img.resize((105,105))
    return noise_img

def blur_image(pil_im):
    #Adding Blur to image 
    blur_img = pil_im.filter(ImageFilter.GaussianBlur(radius=3)) # ouput
    #imshow(blur_img)
    blur_img=blur_img.resize((105,105))
    return blur_img

def affine_rotation(img):
    
    #img=cv2.imread(img_path,0)
    rows, columns = img.shape

    point1 = np.float32([[10, 10], [30, 10], [10, 30]])
    point2 = np.float32([[20, 15], [40, 10], [20, 40]])

    A = cv2.getAffineTransform(point1, point2)

    output = cv2.warpAffine(img, A, (columns, rows))
    affine_img = PIL.Image.fromarray(np.uint8(output)) # affine rotated output
    #imshow(output)
    affine_img=affine_img.resize((105,105))
    return affine_img

def gradient_fill(image):
    #image=cv2.imread(img_path,0)
    laplacian = cv2.Laplacian(image,cv2.CV_64F)
    laplacian = cv2.resize(laplacian, (105, 105))
    return laplacian

"""
This is worker for Adobe VFR Dataset

"""

def worker_1(file, process_id):
    print(f"Reading {file}")

    result_imgs = []

    pil_img = pil_image(realvfr_path.joinpath(file))
    pil_img = crop_resize(pil_img)

    try:
        result_imgs.extend(pil_img)
        for i in range(len(result_imgs)):
            result_imgs[i].save(f"{real_train_dataset}\{i+1}{file}")
        print(f"Removed {file}")
        os.remove(realvfr_path.joinpath(file)) # remove original image
    except TypeError:
        # print("Only one element")
        result_imgs.append(pil_img)
        pil_img.save(f"{real_train_dataset.joinpath(file)}")
        print(f"Removed {file}")
        os.remove(realvfr_path.joinpath(file)) # Remove original image
    
    return f"Worker AdobeVFR {process_id} finished"

"""
This is worker for Synthetic Data

"""
def worker_2(dir, process_id):
    dir_path = dataset3_500_path.joinpath(dir)
    files = os.listdir(dir_path)
    image_counter = 1
    file_counter = 1
    for z in range(len(files[:])): # Put variable file limit here!
        img_path = dir_path.joinpath(files[z])
        image_counter = 1
        result_imgs = []

        pil_img = pil_image(dir_path.joinpath(files[z]))
        # Using squeezing operations
        pil_img = crop_resize(pil_img)
        # Create target Directory if don't exist
        dirName = f"{syn_train_dataset}\\{dir}"
        if not os.path.exists(f"{syn_train_dataset}\\{dir}"):
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ")
            try:
                # try to add to results
                result_imgs.extend(pil_img)
                for i in range(len(result_imgs)):
                    temp = result_imgs[i]
                    # Add Noise
                    temp = noise_image(temp)
                    #Save for real dataset
                    temp.save(f"{real_train_dataset}\\{file_counter}_{image_counter}_{dir}_{files[z]}.jpg")
                    # Save for synth dataset + label
                    temp.save(f"{dirName}\\{file_counter}_{image_counter}_{dir}_{files[z]}.jpg")
                    image_counter+=1
                os.remove(img_path) # Delete original file
                file_counter+=1
            except TypeError:
                # If only have one image result
                # print("Only one element")
                result_imgs.append(pil_img)
                # Add Noise
                pil_img = noise_image(pil_img)
                # Save for real dataset
                pil_img.save(f"{real_train_dataset}\\{file_counter}_{image_counter}_{dir}_{files[z]}.jpg")
                # Save for synth dataset + label
                pil_img.save(f"{dirName}\\{file_counter}_{image_counter}_{dir}_{files[z]}.jpg")
                image_counter+=1
                file_counter+=1
                os.remove(img_path) # Delete original file
        else:    
            print("Directory " , dirName ,  " already exists")
            try:
                result_imgs.extend(pil_img)
                for i in range(len(result_imgs)):
                    temp = result_imgs[i]
                    # Add Noise
                    temp = noise_image(temp)
                    #Save for real dataset
                    temp.save(f"{real_train_dataset}\\{file_counter}_{image_counter}_{dir}_{files[z]}.jpg")
                    # Save for synth dataset + label
                    temp.save(f"{dirName}\\{file_counter}_{image_counter}_{dir}_{files[z]}.jpg")
                    image_counter+=1
                os.remove(img_path) # Delete original file
                file_counter+=1
            except TypeError:
                # print("Only one element")
                result_imgs.append(pil_img)
                # Add Noise
                pil_img = noise_image(pil_img)
                # Save for real dataset
                pil_img.save(f"{real_train_dataset}\\{file_counter}_{image_counter}_{dir}_{files[z]}.jpg")
                # Save for synth dataset + label
                pil_img.save(f"{dirName}\\{file_counter}_{image_counter}_{dir}_{files[z]}.jpg")
                image_counter+=1
                file_counter+=1
                os.remove(img_path) # Delete original file
    return f"Worker Synth {len(files)} has been processed by {process_id}"

def main():
    # # Preprocess and moving part 1
    # For AdobeVFR Real Dataset
    processes = []
    process_id_counter = 1
    processed_counter = 0
    print("Start processing AdobeVFR")
    files = [f for f in os.listdir(realvfr_path) if f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.png') or f.endswith('.tiff') or f.endswith('.bmp') or f.endswith('.gif')]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for file in files[:]: # Put Variable File limit here!
            if file.endswith(".bmp"):
                image = cv2.imread(f"{realvfr_path.joinpath(file)}")
                cv2.imwrite(file.replace('.bmp','.jpg'), image)
            if file.endswith(".tiff"):
                image = cv2.imread(f"{realvfr_path.joinpath(file)}")
                cv2.imwrite(file.replace('.tiff','.jpg'), image)

            process = executor.submit(worker_1, file, process_id_counter)
            processes.append(process)
            process_id_counter +=1

        for p in concurrent.futures.as_completed(processes):
            print(p.result())
            processed_counter+=1
            pass

    print(f"AdobeVFR Processes Complete {processed_counter} has been processed")

    # Preprocess and moving part 2
    # For Synthetic Dataset
    processes = []
    process_id_counter_2 = 0
    print("Start processing Synth")
    dirs = os.listdir(dataset3_500_path)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for dir in dirs[:]: # DIR LIMIR
            process = executor.submit(worker_2, dir, process_id_counter_2)
            processes.append(process)
            process_id_counter_2 +=1

        for p in concurrent.futures.as_completed(processes):
            print(p.result())
            pass

    # print(f"AdobeVFR Processes Complete {processed_counter} has been processed")
    print(f"Syn processes complete {process_id_counter_2} directories has been processed")



if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Finished in {round(t2 - t1, 2)} seconds")
