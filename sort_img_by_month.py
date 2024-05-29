#!/usr/bin/env python3

# TODO
# - Add support for other file types (like .mp4 etc.)
# - Use a context manager for the entire process to ensure cleanup/removal of the old directory upon completion
# - Improve error handling by providing more detailed error messages
# - Improve performance by using multithreading/multiprocessing

import re
import os
import sys
import shutil
import argparse

from ExecutionTimer import ExecutionTimer
from ProgressBar import ProgressBar
from MetaData import *
from Color import *

SPECIAL_FILES = {
    re.compile("^(DSC|P_\d+|IMG-\d+)"): lambda x: rename_file(output_dir, x),
    re.compile("^Screenshot"): lambda x: screenshots(output_dir, x),
    re.compile("joona.and.ella"): lambda x: wedding_photos(output_dir, x)
}

JUNK_FILE_REGEX = re.compile("Abakus")

def rename_file(output_dir, image_object):
    # If no capture date is found, do nothing
    if not image_object.capture_date:
        return
    capture_date = str(image_object.capture_date).replace(' ','_')
    if capture_date:
        new_name = f"{capture_date}{image_object.extension}"
        return new_name
        #shutil.move(image_object.path, os.path.join(image_object.dir_name, new_name))
def wedding_photos(output_dir, image_object):
    wedding_photo_dir = os.path.join(output_dir, 'Wedding')
    wedding_photo_path = os.path.join(wedding_photo_dir, image_object.basename)
    try:
        os.makedirs(wedding_photo_dir, exist_ok=True)
        return wedding_photo_path
        #shutil.move(image_object.path, wedding_photo_path)
    except Exception as e:
        cprint(f"Error moving Wedding photo from {image_object.path} -> {wedding_photo_path}: {e}",
               fg.reg, style.bold)
def screenshots(output_dir, image_object):
    screenshots_dir = os.path.join(output_dir, 'Screenshots')
    screenshot_path = os.path.join(screenshots_dir, image_object.basename)
    try:
        os.makedirs(screenshots_dir, exist_ok=True)
        return screenshot_path
        #shutil.move(image_object.path, screenshot_path)
    except Exception as e:
        cprint(f"Error moving screenshots photo from {image_object.path} -> {screenshots_photo_path}: {e}", fg.reg, style.bold)
        
def remove_file(image_object):
    try:
        os.remove(image_object.path)
    except FileNotFoundError:
        cprint(f'Error removing {image_object.path}: {e}', fg.red)
        

def parse_args():
    parser = argparse.ArgumentParser(
        description="Organize images into directories by year, based on the original capture date")
    parser.add_argument('input', type=str, help='Path to the directory containing the images')
    parser.add_argument('output', type=str, help='Path to the output directory')
    return parser.parse_args()


def cleanup(input_dir):
    # Cleanup function to be called upon completion of script execution
    # Check to make sure no files are left behind and remove the dolr dir tree
    print("\nCleaning up...")
    old_files = [file for root, dirs, files in os.walk(input_dir) for file in files]
    if not old_files:
        shutil.rmtree(input_dir)
        sys.exit("Script completed successfully")
    else:
        print("Could not clean up: Files left behind")
        print('\n'.join(old_files))
        sys.exit(1)


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
                if JUNK_FILE_REGEX.match(pic.basename):
                    try:
                        os.remove(pic.path)
                    except FileNotFoundError:
                        cprint(f'FileNotFound: Error removing {image_object.path}', fg.red)
                        
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
                            shutil.move(pic.path, os.path.join(output_dir , 'NoMetaData', ''))
                    # Meta data found, move it to appropriate year subdirectory based 
                    # on metadata date
                    else:
                        capture_year = pic.capture_date.year
                        output_file_path = os.path.join(output_dir, capture_year, pic.basename)
                        for regex, func in SPECIAL_FILES.items():
                            if regex.match(pic.basename):
                                output_file_path = func(output_dir, pic)
                        # Check if the file already exists in the destination directory, 
                        # if so increment a counter to create a unique name for it.
                        if os.path.exists(output_file_path):
                            while True:
                                count = 0
                                try:
                                    filename = os.path.split(output_file_path)[-1][:-4]
                                    output_file_name = f"{filename}_{count}{pic.extension}"
                                    output_file_path = os.path.join(
                                        output_dir, capture_year, output_file_name)
                                    shutil.move(pic.path, output_file_path)
                                    break
                                except Exception as e:
                                    cprint(e, fg.orange)
                                    count += 1
                        try:
                            os.makedirs(os.path.join(output_dir, capture_year), exist_ok=True)
                            shutil.move(pic.path, output_file_path)
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