#!/usr/bin/env python3

# bp_mp4_cs.py - Batch process all .mp4 files in a directory

import os
import subprocess
import argparse
import sys
import cv2

from MetaData import *

# TODO
# - Check for corrupt files
# - Remove old files

def parse_arguments():
    parser = argparse.ArgumentParser(description="Batch process all .mp4 files in a directory")
    parser.add_argument("input_directory", help="Input directory")
    parser.add_argument("output_directory", help="Output directory")
    return parser.parse_args()


def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        for line in content:
            file.write(line + '\n')

        
def compress(input_directory, output_directory):
    """
    Compresses all .mp4 files in the input directory and saves the compressed files in the output directory.
    
    Args:
        input_directory (str): The directory containing the .mp4 files to be compressed.
        output_directory (str): The directory where the compressed .mp4 files will be saved.
    
    Returns:
        list: A list of the names of the successfully compressed .mp4 files.
    
    Raises:
        SystemExit: If the output file already exists and is not a file.
    
    Prints:
        str: The progress of the compression process.
        str: Information about the current file being compressed.
        str: Information about the successful conversion of a file.
        str: Information about the failed conversion of a file.
        str: A message indicating the completion of the batch conversion.
    """
    compressed_files = []
    input_directory = DirectoryObject(input_directory)
    output_directory = DirectoryObject(output_directory)
    # Replace whitespace in the output directory path with underscores
    # output_directory = output_directory.replace(' ', '_')

    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output_directory.path, exist_ok=True)
    except OSError as e:
        print(f"[\033[31m Error creating output directory '{output_directory}': {e} \033[0m]")
        return

    # Get total files
    number_of_files = len(input_directory)

    print(f"\033[34mTotal number of .mp4 files to process:\033[0m \033[2;36m{number_of_files}\033[m") # DEBUGGING
    
    # Iterate over all .mp4 files in the input directory
    for i, input_file in enumerate(input_directory):
        print(f"[\033[33m Processing {input_file} ({i + 1}/{number_of_files}) \033[0m]")
        if input_file.basename.endswith(".mp4"):
            #video = VideoObject(os.path.join(input_directory, input_file))
            
            # Extract the file name without extension 
            # (some_video_file_name.getsome.arhagag.mp4) -> (some_video_file_name.getsome.arhagag)
            # file_name = os.path.splitext(input_file)[0]

            try:
                # Define the output file path
                output_file_path = os.path.join(output_directory.path,input_file.basename)
            except Exception as e:
                print(f"[\033[31m {e} \033[0m")
                continue
            # Check if the output file already exists
            if os.path.exists(output_file_path):
                output_file_object = VideoObject(output_file_path)
                # Remove file if it is corrupt
                if output_file_object.is_corrupt:
                    os.path.remove(output_file_path)
                # If metadata is the same but size if different, its already compressed so skip
                # and flag for removal of old file
                elif output_file_object.metadata == input_file.metadata and output_file_object.size != input_file.size:
                    compressed_files.append(input_file)
                    continue
                else:
                    print(f"[\033[31m {output_file_path} already exists. Skipping. \033[0m]")
                    continue
            # Run ffmpeg command for each file
            result = subprocess.run(
                 f'ffmpeg -i \'{input_file.path}\' \
                    -c:v h264_nvenc -rc constqp -qp 28 \'{output_file_path}\' -n',
                    shell=True, 
                    capture_output=True, 
                    text=True)
            result = result.returncode
            # Check if conversion was successful
            if result == 0:
                print(f"[\033[32m Successfully converted {input_file.basename} \033[0m]")
                compressed_files.append(input_file)
            else:
                print(f"[\033[31m {input_file.basename} could not be converted. Error code: {result}\033[0m]")
    print("[\033[1;32m Batch conversion completed. \033[0m]")
    return compressed_files

if __name__ == "__main__":
    args = parse_arguments()
    sucessfully_compressed_files = compress(args.input_directory, args.output_directory)

    for vid in sucessfully_compressed_files:
        if vid.is_corrupt:
            print(f"\033[31m{vid.path} is corrupt\033[0m")
        else:
            print(f"\033[32m{vid.path} is not corrupt. Removing old file...\033[0m")
            os.remove(os.path.join(args.input_directory, vid.basename))

    


