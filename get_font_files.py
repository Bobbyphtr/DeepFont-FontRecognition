from shutil import copy 
from fontTools import ttLib
from pathlib import Path
import time
import os,errno, glob


font_path = Path('E:\\FontRecognition\\Fonts_Final\\')

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

def duplicate(src, dest) :
    copy(src, dest)


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
        font_dict[shortName(tt)[0]] = font

    # Get all 500 fonts
    files = os.listdir('E:\\FontRecognition\\Dataset_Final\\Dataset_3_500_2\\')
    filtered_dict = {}
    for font_name in font_dict:
        if font_name in files:
            filtered_dict[font_name] = font_dict[font_name]

    # Copy all of the 500 font to destination
    destination_dir = 'E:\\FontRecognition\\Fonts_500\\'
    for font in filtered_dict:
        duplicate(filtered_dict[font], destination_dir)

    print(os.listdir(destination_dir))
    
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Finished in {round(t2 - t1, 2)} seconds")
