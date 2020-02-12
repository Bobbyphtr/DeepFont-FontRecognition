"""
Copying Dataset 3

"""

from shutil import copyfile, copytree
import os, errno, concurrent.futures, time
from multiprocessing import Value
from pathlib import Path

def copy_img(src, dst):
    copyfile(src=src, dst=dst)
    return f"Copy {src} to {dst}"

def check_dirs(dirs):
    for dir in dirs:
        dst_dir_path = DST_PATH.joinpath(dir)
        if len(os.listdir(dst_dir_path)) == 1000:
            print(f"dir {dir} has already copied")
        else:
            print("\n")
            print(f"dir {dir} has not completely copied")
            print("\n")

def copy_worker(src_dir, dst_dir):
    print(f"Copying {dir} from {src_dir} ti {dst_dir}")
    copytree(src_dir, dst_dir)
    return None

DST_PATH = Path("E:\FontRecognition\Dataset_Final\Dataset_3")
SRC_PATH = Path("E:\FontRecognition\Dataset_3")


os.chdir(SRC_PATH)
src_dirs = os.listdir(os.getcwd())
dst_dirs = os.listdir(DST_PATH)

# Substract src - dst, resulting in not coppied dirs
not_copied_dirs = [dir for dir in src_dirs if dir not in dst_dirs]
# print(not_copied_dirs)

def main():
    # processes = []
    # process_id_counter = 1
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     for dir in not_copied_dirs[:]:
    #         dst_dir = DST_PATH.joinpath(dir)
    #         src_dir = SRC_PATH.joinpath(dir)
    #         process = executor.submit(copy_worker, src_dir, dst_dir)
    #         processes.append(process)
    #         process_id_counter +=1

    #     for p in concurrent.futures.as_completed(processes):
    #         print(p.result())

    check_dirs(dst_dirs)
    print(f"{len(dst_dirs)} total directories")

if __name__ == "__main__":
    main()