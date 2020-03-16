from skimage.io import imread
from skimage.transform import resize
from sklearn.utils import shuffle

from sklearn.model_selection import train_test_split
from time import time

from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, BatchNormalization, Conv2DTranspose
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.datasets import mnist
from tensorflow import keras
from tensorflow.keras.callbacks import TensorBoard
import numpy as np
import matplotlib.pyplot as plt
import os
import tensorflow as tf

import math

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please install GPU version of TF")

class My_Custom_Generator(keras.utils.Sequence) :

  def __init__(self, image_filenames, batch_size) :
    self.image_filenames = image_filenames
    self.batch_size = batch_size


  def __len__(self) :
    return (np.ceil(len(self.image_filenames) / float(self.batch_size))).astype(np.int)


  def __getitem__(self, idx) :
    batch_x = self.image_filenames[idx * self.batch_size : (idx+1) * self.batch_size]

    current_x = np.array([
            resize(imread('E:/FontRecognition/Dataset_Final/preprocessed/real_train_500_2/' + str(file_name)), (104,104,1)) 
                for file_name in batch_x])/255.0
    return current_x, current_x



# REAL_DATA_DIR = 'E:\\FontRecognition\\Dataset_Final\\preprocessed\\real_train_500_2'
# image_file_counter = 0

# files = os.listdir(REAL_DATA_DIR)
# files_count = len(files)
# files = shuffle(files)

# np.save('imagenames.npy', files)

# imagenames_shuffled_numpy = np.array(files)

# X_train_filenames, X_val_filenames = train_test_split(
#     imagenames_shuffled_numpy, test_size=0.2, random_state=1)

# print(X_train_filenames.shape)
# print(X_val_filenames.shape)

# np.save('X_train_filenames.npy', X_train_filenames)
# np.save('X_val_filenames.npy', X_val_filenames)

# load
X_train = np.load('X_train_filenames.npy')
X_val = np.load('X_val_filenames.npy')

# print(X_train.shape)
# print(X_val.shape)

batch_size = 128

my_training_batch_generator = My_Custom_Generator(X_train, batch_size=batch_size)
my_validation_batch_generator = My_Custom_Generator(X_val, batch_size=batch_size)

# images, labels = next(my_training_batch_generator)
# print("Train")
# print(images.shape)
# print(labels.shape)
# images, labels = next(my_validation_batch_generator)
# print("Val")
# print(images.shape)
# print(labels.shape)

input_img = Input(shape=(104,104,1))

x = Conv2D(64, kernel_size=(48,48), activation='relu', padding='same', strides=1)(input_img)
x = BatchNormalization()(x)
x = MaxPooling2D(pool_size=(2,2)) (x)
x = Conv2D(128, kernel_size=(24,24), activation='relu', padding='same', strides=1)(x)
x = BatchNormalization()(x)
encoded = MaxPooling2D(pool_size=(2,2))(x)

x = Conv2D(64, kernel_size=(24,24), activation='relu', padding='same', strides=1)(encoded)
x = UpSampling2D(size=(2,2))(x)
x = Conv2D(1, kernel_size=(48,48), activation='relu', padding='same', strides=1)(x)
decoded = UpSampling2D(size=(2,2))(x)

adam = keras.optimizers.Adam(lr=0.01)
autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer=adam, loss='mean_squared_error')

autoencoder.summary()

tensorboard = TensorBoard(log_dir=".\\tmp\\autoencoder\\{}".format(time()),histogram_freq=False,write_graph=True,  write_images=True)

num_epochs = 50
# autoencoder.fit(generator=my_training_batch_generator,
#                     epochs=num_epochs,
#                     verbose=1,
#                     validation_data=my_validation_batch_generator,
#                     callbacks=[tensorboard]
#                     # use_multiprocessing=True,
#                     # workers=6
#                     )
autoencoder.fit(
    x = my_training_batch_generator, 
    validation_data = my_validation_batch_generator,
    epochs=num_epochs,
    callbacks=[tensorboard],
    # use_multiprocessing=True,
    # workers=6 
    )

# evaluate
scores = autoencoder.evaluate(x=my_training_batch_generator, callbacks=[tensorboard])
print(scores)

# Save weight
autoencoder.save("SCAE.h5")
print("Saved model to disk")
print("Finished")