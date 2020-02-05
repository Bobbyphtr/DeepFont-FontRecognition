import os
import concurrent.futures
import time
from zipfile import ZipFile
from pathlib import Path
import numpy as np

from fontTools import ttLib

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1

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

def common_member(a, b): 
      
    a_set = set(a) 
    b_set = set(b) 
      
    # check length  
    if len(a_set.intersection(b_set)) > 0: 
        return(a_set.intersection(b_set))   
    else: 
        return("no common elements") 

def main():
    # process_id_counter = 1
    # secs = [5, 3, 4, 1, 2]
    # results = []
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     for sec in secs:
    #         result = executor.submit(do_something, sec, process_id_counter)
    #         results.append(result)
    #         process_id_counter+=1
        
    #     for f in concurrent.futures.as_completed(results):
    #         print(f.result())
    file_path = Path('E:\Google Drive\Colab Notebooks')
    b_path = Path('Fonts_2')
    dataset_path = file_path.joinpath('Dataset\Dataset.zip')
    textfile = open(file_path.joinpath('Dataset\\font_names.txt'), 'r')

    # Opening a zip file and write the directory
    # with ZipFile(dataset_path, 'r') as f:
    #      names = [info.filename for info in f.infolist() if info.is_dir()]
    #      for name in names:
    #          name = name[:len(name) - 1]
    #          print(name)
    #          textfile.write(name+"\n")
    
    #Opening existing font names
    line_list = textfile.readlines()
    old_fonts = []
    for line in line_list:
        line = line.replace("\n","").lower().replace(" ","").replace("-","")
        old_fonts.append(line)
    print(f"Existing fonts is {len(old_fonts)}")

    # Opening new Font Files
    types = ('*.ttf', '*.otf')
    all_fonts = []
    for files in types:
        all_fonts.extend(b_path.glob(files))
    
    all_fonts.sort()
    all_fonts = np.array(all_fonts)
    new_fonts = []
    
    for font in all_fonts:
        tt = ttLib.TTFont(font)
        font_name = shortName(tt)[0]
        font_name = font_name.lower().replace(" ","").replace("-","")
        new_fonts.append(font_name)
        if font_name in old_fonts:
            print(font_name)

    print(f"New fonts is {len(new_fonts)}")
    existing_fonts = common_member(old_fonts, new_fonts)
    print("Exisiting font = " + existing_fonts)

    # Removing existing fonts
    delete_count = 0
    for font in all_fonts:
        tt = ttLib.TTFont(font)
        font_name = shortName(tt)[0]
        font_name = font_name.lower().replace(" ","").replace("-","")
        if font_name in existing_fonts:
            os.remove(font)
            delete_count+=1
            print(f"Remove {font_name} counter = {delete_count}")




if __name__ == "__main__":
    start = time.perf_counter()
    main()
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} seconds(s)')