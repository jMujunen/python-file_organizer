#!/usr/bin/env python3

# TODO
# - Add support for other file types (like .mp4 etc.)
# - Use a context manager for the entire process to ensure cleanup/removal of the old directory upon completion
# - Improve error handling by providing more detailed error messages
# - Improve performance by using multithreading/multiprocessing


import os
import sys
import shutil
import argparse

from ExecutionTimer import ExecutionTimer
from ProgressBar import ProgressBar
from MetaData import *
from Color import *


def parse_args():
    parser = argparse.ArgumentParser(
        description="Organize images into directories by year, based on the original capture date")
    parser.add_argument('input', type=str, help='Path to the directory containing the images')
    parser.add_argument('output', type=str, help='Path to the output directory')
    return parser.parse_args()


def main(input_dir, output_dir):
    with ExecutionTimer():
        # Initialize objects and variables
        d = DirectoryObject(input_dir)
        progress = ProgressBar(len(d) + 1)

        # Create a directory for the images without metadata
        os.makedirs(os.path.join(output_dir, 'NoMetaData'), exist_ok=True)
        # Iterate over all files in the directory
        for pic in d:
            progress.increment()
            # Ensure the file is an image
            if pic.is_image:
                try:
                    # Sort the images into directories by capture date year
                    # If the image does not have a capture date, move it to 'NoMetaData' directory
                    # and rename if necessary to avoid duplicates
                    if not pic.capture_date:
                        # Move the file to 'NoMetaData' directory
                        os.makedirs(os.path.join(output_dir, 'NoMetaData'), exist_ok=True)
                        no_meta_data_dir = os.path.join(output_dir, 'NoMetaData')
                        no_meta_data_image = os.path.join(no_meta_data_dir, pic.basename)
                        # Rename the file if it already exists in 'NoMetaData' directory 
                        # to avoid duplicates
                        if os.path.exists(no_meta_data_image):
                            # Increment the count until we find a filename that does not exist yet
                            while True:
                                count = 0
                                try:
                                    new_file_name = f"{pic.basename[:-4]}_{count}{pic.extension}"
                                    shutil.move(
                                        pic.path, os.path.join(no_meta_data_dir,  new_file_name))
                                    # If the new filename does not exist, break the loop and
                                    # continue execution with the new filename
                                    break
                                except Exception as e:
                                    cprint(e, fg.orange)
                                    count += 1
                        # If the file does not exist in 'NoMetaData' directory yet, move it there
                        else:
                            shutil.move(pic.path, os.path.join(input_dir, 'NoMetaData', ''))
                    # Meta data found, move it to appropriate year subdirectory based 
                    # on metadata date
                    else:
                        capture_year = pic.capture_date[:4]
                        new_file_path = os.path.join(output_dir, capture_year, pic.basename)
                        # Check if the file already exists in the destination directory, 
                        # if so increment a counter to create a unique name for it.
                        if os.path.exists(new_file_path):
                            while True:
                                count = 0
                                try:
                                    new_file_path = f"{pic.basename[:-4]}_{count}{pic.extension}"
                                    shutil.move(pic.path, os.path.join(
                                        output_dir, capture_year, new_file_name))
                                    break
                                except Exception as e:
                                    cprint(e, fg.orange)
                                    count += 1
                        try:
                            os.makedirs(os.path.join(output_dir, capture_year), exist_ok=True)
                            shutil.move(pic.path, new_file_path)
                        except KeyboardInterrupt:
                            break
                        except Exception as e:
                            cprint(e, fg.deeppink)
                            continue
                except Exception as e:
                    cprint(e, fg.red)


if __name__ == "__main__":
    args = parse_args()
    try:
        main(args.input, args.output)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)