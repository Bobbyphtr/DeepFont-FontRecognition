from pathlib import Path
from fontTools import ttLib
import os,errno, glob
import numpy as np
from random import sample

import concurrent.futures
import time
from multiprocessing import Value

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1

# file_path = Path('E:\Google Drive\Colab Notebooks')
file_path = Path('E:\FontRecognition')
font_path = file_path.joinpath('Fonts_500')
dataset_path = file_path.joinpath('Dataset_Final\\Dataset_test')

total_images_per_font = 20

def shortName( font ):
    """Get the short name from the font's names table"""
    name = ""
    family = ""
    for record in font['name'].names:
        if b'\x00' in record.string:
            name_str = record.string.decode('utf-16-be')
        else:   
            name_str = record.string.decode('latin-1')
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            name = name_str
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family: 
            family = name_str
        if name and family: break
    return name, family

def generate_images(fonts, process_id):
    print(f'Begin generating image from process {process_id}')
    for font in fonts[:]:
        tt = ttLib.TTFont(font)
        font_name = shortName(tt)[0]
        space_counter = 0
        for char in reversed(font_name):
            if char == ' ':
                space_counter+=1
            else:
                break
        font_name = font_name[:len(font_name) - space_counter]
        synthetic_font_path = str(dataset_path.joinpath(font_name))
        font_type_used = str(font)
        try:
            os.makedirs(synthetic_font_path)
            print(f"creating {font_name} dataset")
            """
            TRDG Configuration
            --outputdir
            count (c)       = 1000 image
            blur (bl)       = 0 - 3 (nilai tengah dari random)
            format (f)      = 105px
            character_spacing (cs) = 3px (tidak bisa dirandom)
            background (b)  = pictures (random)
            skew (k)        = 6 affine transform random

            trdg cannot random cs.
            """
            command_str  = f"trdg --output_dir \"{synthetic_font_path}\" -c {total_images_per_font} -b 3 -bl 3 -rbl -k 6 -rk -tc #000000,#4A4A4A -f 105 -cs 3 -ft \"{font_type_used}\""
            os.system('cmd /c '+command_str)
        except OSError as e:
            if e.errno == errno.EEXIST:
                total_image = len(glob.glob1(synthetic_font_path, '*.jpg'))
                if total_image < total_images_per_font:
                    print(f"{font_name} lack of {(total_images_per_font - total_image)}, Generating lacked image")
                    command_str  = f"trdg --output_dir \"{synthetic_font_path}\" -c {total_images_per_font} -b 3 -bl 3 -rbl -k 6 -rk -tc #000000,#4A4A4A -f 105 -cs 3 -ft \"{font_type_used}\""
                    os.system('cmd /c '+command_str)
               
        # print(font_name)
    return f"Image generator from process {[process_id]} finished"

def check_all_directory(fonts, process_id):
    is_cleared = True
    all_folder_count = 0
    all_image_count = 0
    print(f'Begin checking all directory from process {process_id}')
    for font in fonts:
        tt = ttLib.TTFont(font)
        font_name = shortName(tt)[0]
        space_counter = 0
        for char in reversed(font_name):
            if char == ' ':
                space_counter+=1
            else:
                break
        font_name = font_name[:len(font_name) - space_counter]
        synthetic_font_path = str(dataset_path.joinpath(font_name))
        if os.path.isdir(synthetic_font_path):
            total_image = len(glob.glob1(synthetic_font_path, '*.jpg'))
            # print(f"{font_name} is {total_image}")
            all_folder_count+=1
            all_image_count+=total_image
            if total_image  < total_images_per_font:
                print(f"{font_name} lack of {(total_images_per_font - total_image)} on {font}")
                print(f"Generating {font_name} : {(total_images_per_font - total_image)} with {font}")
                command_str  = f"trdg --output_dir \"{synthetic_font_path}\" -c {total_images_per_font - total_image} -b 3 -bl 3 -rbl -k 6 -rk -tc #000000,#4A4A4A -f 105 -cs 3 -ft \"{font_type_used}\""
                os.system('cmd /c '+command_str)
                is_cleared = False
            elif total_image > total_images_per_font:
                print(f"{font_name} is over {(total_image - total_images_per_font)}")
                print(f"Removing {(total_image - total_images_per_font)} in {str(synthetic_font_path)}")
                thefiles = os.listdir(synthetic_font_path)
                for file in sample(thefiles,(total_image - total_images_per_font)):
                    # print(synthetic_font_path +"'\\"+ file)
                    os.remove(synthetic_font_path +"\\"+ file)
                is_cleared = False
            else:
                pass
        # print(font_name)
    print(f"Image generator from process {[process_id]} report is_cleared: {is_cleared}")
    return all_folder_count, all_image_count

def main():
    types = ('*.ttf', '*.otf')
    all_fonts = []
    for files in types:
        all_fonts.extend(font_path.glob(files))
    all_fonts.sort()

    # splitting data
    all_fonts = np.array(all_fonts)
    print(f'{len(all_fonts)} detected')
    all_fonts = np.array_split(all_fonts, 8)
    print(f'{len(all_fonts)}  splits are created')

    # creating multiple process and generate images
    processes = []
    process_id_counter = 1
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for split in all_fonts:
            process = executor.submit(generate_images, split, process_id_counter)
            processes.append(process)
            process_id_counter +=1

        for p in concurrent.futures.as_completed(processes):
            print(p.result())
    
    # Checking all directories
    counter_font_folder = 0
    counter_all_images = 0
    print("Checking all directory")
    processes = []
    process_id_counter = 1
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for split in all_fonts:
            process = executor.submit(check_all_directory, split, process_id_counter)
            processes.append(process)
            process_id_counter +=1

        for p in concurrent.futures.as_completed(processes):
            # print(p.result())
            temp = p.result()
            dir_count = float(temp[0])
            img_count = float(temp[1])
            counter_font_folder+=dir_count
            counter_all_images+=img_count
    print(f"Total Directories : {counter_font_folder}")
    print(f"Total Images : {counter_all_images}")

    # generate_images(fonts, 0)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print("Synthetic data has been created")
    print(f"Finished in {round(t2 - t1, 2)} seconds")