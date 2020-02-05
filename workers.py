from shutil import copy
import concurrent.futures
from multiprocessing import Value
from pathlib import Path
import os, errno

from pathlib import Path
from PIL import Image, ImageOps

def pil_image(img_path):
    pil_im = Image.open(img_path).convert('L')
#     imshow(np.asarray(pil_im))
    return pil_im

def crop(pil_img):
    width, height = pil_img.size
#     width = img.shape[1]
#     x0 = int(width/2 - 52.5)
#     x1= int(width/2 + 52.5)
#     y0 = int(0)
#     y1 = int(105)
#     img = img[y0:y1, x0:x1, :]
    left = width/2 - 52.5
    top = 0
    right = width/2 + 52.5 
    bottom = 105
    img = pil_img.crop((left, top, right, bottom))
#     imshow(img)
    return img

def crop_resize(pil_img):
    (width, height) = pil_img.size
    print(width, height)
    if width < 105 or height < 105:
        img = pil_img.resize((105,105), Image.ANTIALIAS)
        print("resize")
    elif width > 500 or height > 500:
        # Squeezing operation
        baseheight = 105
        hpercent = (baseheight/float(pil_img.size[1]))
        wsize = int((float(pil_img.size[0])*float(hpercent)))
        temp_img = pil_img.resize((wsize,baseheight), Image.ANTIALIAS)
        img = crop(temp_img)
        print("scale down")
    else:
        img = crop(pil_img)
        print("crop")
    return img
#     return cv2.resize(pil_img, dsize=(105, 105), interpolation=cv2.INTER_CUBIC)

def worker_operation(file, process_id_counter):
    print(f"Processing {process_id_counter}")
    pil_img = pil_image(realvfr_path.joinpath(file))
    pil_img = crop_resize(pil_img)
    # imshow(pil_img)
    print(f"Save at {real_train_dataset.joinpath(file)}")
    pil_img.save(f"{real_train_dataset.joinpath(file)}")
    return f"Process {process_id_counter} finished"

# for file in files:
#     src = realvfr_path.joinpath(file)
#     print(f"Copying {src} to {dst}")
#     print(copy_ops(src, dst, 1))

file_path = Path('E:\FontRecognition')
dataset_path = file_path.joinpath('Dataset_Final')

real_train_dataset = dataset_path.joinpath('real_train') 

dataset3_path = file_path.joinpath('Dataset_3')
realvfr_path = file_path.joinpath('AdobeVFRDataset\\real')

files = os.listdir(realvfr_path)
dst = real_train_dataset

def main():
    processes = []
    process_id_counter = 1
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for file in files[:]:
            process = executor.submit(worker_operation, file, process_id_counter)
            processes.append(process)
            process_id_counter +=1

        for p in concurrent.futures.as_completed(processes):
            print(p.result())

if __name__ == "__main__":
    main()