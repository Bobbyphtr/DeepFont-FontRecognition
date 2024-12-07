from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.optimizers import SGD
from tensorflow.python.keras import backend as K
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import precision_score , recall_score

import numpy as np
import matplotlib.pyplot as plt  
import os

def squeezing_operation(pil_img):
    baseheight = 105
    hpercent = (baseheight/float(pil_img.size[1]))
    wsize = int((float(pil_img.size[0])*float(hpercent)))
    temp_img = pil_img.resize((wsize,baseheight), Image.ANTIALIAS)
    return temp_img

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


picture_path = str(sys.argv[1])  
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

x = np.array(x).reshape(-1, 105, 105, 1)
x = x / 255.0

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
print("#",label)
print("#",font_files)


# FOR MODEL EVALUATION ONLY

# model = load_cnn()
# model.summary()

# test_data_path = 'E:\\FontRecognition\\Dataset_Final\\preprocessed\\dataset_test_50_RBKN\\'
# batch_size = 128
# test_datagen = ImageDataGenerator(rescale=1. / 255)
# test_generator = test_datagen.flow_from_directory(test_data_path,
#                                                   target_size=(105, 105),
#                                                   batch_size=batch_size,
#                                                   color_mode='grayscale',
#                                                   class_mode='sparse',
#                                                   shuffle=False)

# evaluate the model
# loss, accuracy, lr, precision, recall = model.evaluate_generator(test_generator, steps=test_generator.samples // batch_size + 1)

# print(f"loss : {loss}")
# print(f"accuracy : {accuracy}")
# print(f"precision : {precision}")
# print(f"recall : {recall}")
# print(f"lr : {lr}")

#Confution Matrix and Classification Report
# Y_pred = model.predict_generator(test_generator, steps=test_generator.samples // batch_size+1)
# y_pred = np.argmax(Y_pred, axis=1)
# print('Confusion Matrix')
# matrix = confusion_matrix(test_generator.classes, y_pred)
# print(matrix)
# import pickle
# with open('matrix', 'wb') as file:
#   pickle.dump(matrix, file)
# print('Classification Report')
# print(classification_report(test_generator.classes, y_pred))
# precision_scr = precision_score(test_generator.classes,y_pred,average='weighted')
# recall_scr = recall_score(test_generator.classes,y_pred,average='weighted')
# print('avg precision : ', precision_scr)
# print('avg recall : ', recall_scr)