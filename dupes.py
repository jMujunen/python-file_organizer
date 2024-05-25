#!/usr/bin/env python3

# dupes.py - Find duplicate files in two directories and remove the dupes.
#            Conditions for dupes are as follows:
#            1. The files are the same size
#            2. The files have the same extension
#            3. The files have the same basename (some_file.txt)

import os
import sys
import re
import shutil
import argparse

from ExecutionTimer import ExecutionTimer
from ProgressBar import ProgressBar
from MetaData import *
from Color import *

# TODO
# - [ ] Add verbose mode
# - [ ] Implement dry-run mode
# - [ ] Implement the feature which allowes inputting a single directory or serveral

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Find and remove duplicate files from 1 or more directories",
        )
    parser.add_argument(
        "dir1", help="Path to the first directory where the duplicate files will be removed")
    parser.add_argument(
        "dir2", help="Path to the second directory where the duplicate files will be kept")
    return parser.parse_args()


def main(dir1, dir2):
    with ExecutionTimer():
        errors = []
        files_to_remove = []

        dir1_obj = DirectoryObject(dir1)
        dir2_obj = DirectoryObject(dir2)

        jobs = len(dir1_obj) + 1
        progress = ProgressBar(jobs)
        for item in dir1_obj:
            progress.increment()
            if item.basename in dir2_obj:
                if item.is_file and item.extension in [
                    '.jpg', '.jpeg', '.png', '.nef', '.mp4', 'avi', 'mkv', 'wmv', 'webm', 'mov']:

                        try:
                            file_info = dir2_obj.file_info(item.basename)
                            larger_file = file_info if file_info.size > item.size else item
                            if larger_file.is_corrupt:
                                cprint(f"{larger_file.path} is corrupt. Removing...", fg.red, style.underline)
                                files_to_remove.append(larger_file.path)
                                #os.remove(larger_file.path)
                            elif item.is_corrupt:
                                cprint(f"{item.path} is corrupt. Removing...", fg.red, style.underline)
                                files_to_remove.append(item.path)
                                # os.remove(item.path)
                            else:
                                cprint(f"Removing {larger_file.path}", fg.red, style.bold)
                                files_to_remove.append(larger_file.path)
                                # os.remove(larger_file.path)
                        except AttributeError:
                            errors.append(f'Nonetype: {item.path}, and {dir2_obj.path}')
                        except Exception as e:
                            print(e)
                            pass
                else:
                    try:
                        if item.content == dir2_obj.file_info(item.basename).content:
                            if not item.is_corrupt:
                                cprint(f"Removing {item.path}", fg.red, style.bold)
                                files_to_remove.append(item.path)
                                # os.remove(item.path)
                            elif dir2_obj.file_info(item.basename).is_corrupt:
                                cprint(f"Removing {item.path}", fg.red, style.bold)
                                files_to_remove.append(item.path)
                                # os.remove(item.path)
                    except Exception as e:
                        pass
        cprint(f'\n{"\n".join(files_to_remove)}', style.bold)
        if files_to_remove:
            try:
                with open('files_to_remove.log', 'w') as f:
                    '\n'.join(files_to_remove)

            except:
                cprint('Error writing to file', bg.red, style.bold, style.underline)
        
            if input('Are you sure you want to remove these files? [y/N]: ') in ['y', 'Y']:
                remove_progress = ProgressBar(len(files_to_remove))
                for f in files_to_remove:
                    remove_progress.increment()
                    try:
                        os.remove(f)
                    except KeyboardInterrupt:
                        break
                    except Exception as e:
                        cprint(f'\n{e}', fg.red, style.bold)
                        errors.append(f'Error removing {f}')
                        continue
            cprint(f'\n\n{'\n'.join(errors)}', bg.red, style.bold)


if __name__ == '__main__':
    args = parse_arguments()
    main(args.dir1, args.dir2)
