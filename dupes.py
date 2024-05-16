#!/usr/bin/env python3

# dupes.py - Find duplicate files in two directories and remove the dupes

import os, sys, re, shutil
import argparse

from ExecutionTimer import ExecutionTimer
from ProgressBar import ProgressBar
from MetaData import *
from Color import *

def parse_arguments():
    parser = argparse.ArgumentParser(description="Find and remove duplicate files from two directories")
    parser.add_argument("dir1", help="Path to the first directory where the duplicate files will be removed")
    parser.add_argument("dir2", help="Path to the second directory where the duplicate files will be kept")

    return parser.parse_args()

def main(dir1, dir2):
    with ExecutionTimer():
        dir1_obj = DirectoryObject(dir1)
        dir2_obj = DirectoryObject(dir2)

        progress = ProgressBar(len(dir1_obj))

        for item in dir1_obj:
            progress.increment()
            if item.is_file:
                if item.basename in dir2_obj:
                    try:
                        file_info = dir2_obj.file_info(item.basename)
                        
                        larger_file = file_info if file_info.size > item.size else item
                        if larger_file.is_corrupt:
                            cprint(f"{larger_file.path} is corrupt. Removing...", fg.red, style.bold)
                            os.remove(larger_file.path)
                        elif item.is_corrupt:
                            cprint(f"{item.path} is corrupt. Removing...", fg.red, style.bold)
                            os.remove(item.path)
                        else:
                            os.remove(larger_file.path)
                    except Exception as e:
                        print(e)
                        pass

        print('')

if __name__ == '__main__':
    args = parse_arguments()
    main(args.dir1, args.dir2)