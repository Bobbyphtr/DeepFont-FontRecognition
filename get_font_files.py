from shutil import copy 
from fontTools import ttLib
from pathlib import Path
import time
import os,errno, glob
import pickle

font_path = Path('E:\\FontRecognition\\Fonts_500\\')

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1

def shortName(font):
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

# def duplicate(src, dest) :
#     copy(src, dest)


def main():
    types = ('*.ttf', '*.otf')

    # Get all the fonts
    all_fonts = []
    for files in types:
        all_fonts.extend(font_path.glob(files))
    all_fonts.sort()

    # Creating font dictionary
    font_dict = {}
    for font in all_fonts:
        tt = ttLib.TTFont(font)
        font_dict[shortName(tt)[0]] = font.name

    print(font_dict)
    print(len(font_dict))
    with open('E:\\FontRecognition\\App\\Model\\font_dict', 'wb') as file:
        pickle.dump(font_dict, file)
    
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Finished in {round(t2 - t1, 2)} seconds")
