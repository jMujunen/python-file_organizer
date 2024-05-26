#!/usr/bin/env python3

# bp_mp4_cs.py - Batch process all .mp4 files in a directory

import os
import subprocess
import argparse
import sys
import cv2
import shutil

from MetaData import *
from Color import *
from ExecutionTimer import ExecutionTimer
from ProgressBar import ProgressBar
from ByteConverter import ByteConverter

# TODO
# - Check for corrupt files
# - Remove old files


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Batch process all .mp4 files in a directory"
    )
    parser.add_argument("input_directory", help="Input directory")
    parser.add_argument("output_directory", help="Output directory")
    return parser.parse_args()


def main(input_directory, output_directory):
    # List of file objects
    old_files = []
    new_files = []
    input_directory = DirectoryObject(input_directory)
    output_directory = DirectoryObject(output_directory)

    try:
        # for folder_path in input_directory.rel_directories:
            # Create the output directorys if they don't exist
        os.makedirs(output_directory.path, exist_ok=True)
    except OSError as e:
        print(
            f"[\033[31m Error creating output directory '{output_directory}': {e} \033[0m]"
        )
        return

    # Initialize progress bar
    number_of_files = len(input_directory) + 1
    progress = ProgressBar(number_of_files)

    # Loop through all files in input directory
    for item in input_directory:
        progress.increment()
        if item.extension == ".mp4":
            try:
                # Define the output file path
                output_file_path = os.path.join(output_directory.path, item.basename)
            except Exception as e:
                cprint(f"\n{e}", fg.red, style.underline)
                continue

            # Check if the output file already exists
            if os.path.exists(output_file_path):
                output_file_object = VideoObject(output_file_path)
                # If metadata is the same but size if different, its already compressed so skip
                # and flag for removal of old file
                duration_diff = output_file_object.metadata['duration'] - item.metadata['duration']
                if (
                    output_file_object.metadata == item.metadata
                    and output_file_object.size != item.size
                    or output_file_object.size != item.size
                    and output_file_object.metadata['aspect_ratio'] == item.metadata['aspect_ratio']
                    and abs(duration_diff) < 0.1
                ):
                    old_files.append(item)
                    new_files.append(output_file_object)
                    continue
                elif output_file_object.is_corrupt:
                    os.remove(output_file_object.path)
                elif (
                    output_file_object.basename == item.basename
                    and not output_file_object.is_corrupt
                    and item.size != output_file_object.size
                ):
                    count = 0
                    # Loop until a unique name is found
                    while True:
                        try:
                            print(output_file_object.metadata)
                            print(output_file_object.bitrate)
                            print(output_file_object.size)
                            print(output_file_object.basename)
                            print('-------------')
                            print(item.metadata)
                            print(item.bitrate)
                            print(item.size)
                            print(item.basename)
                            # Rename the file: "input_file.mp4" -> "input_file_1.mp4"
                            new_path = f"{output_file_path[:-4]}_{str(count)}.mp4"
                            shutil.move(item.path, new_path)
                            item = VideoObject(new_path)
                            break
                        except FileExistsError:
                            count += 1
                            continue
                        else:
                            break
                # If all else fails, something was not accounted for
                else:
                    (
                        os.remove(item.path)
                        if not item.is_corrupt
                        else cprint(
                            "FATAL ERROR: Manual intervention required",
                            fg.red,
                            style.underline,
                        )
                    )
                    continue
            # Run ffmpeg command for each file
            result = subprocess.run(
                f'ffmpeg -i "{item.path}" -c:v hevc_nvenc -crf 20 -qp 20 "{output_file_path}"',
                shell=True,
                capture_output=True,
                text=True,
            )
            result = result.returncode
            output_file_object = VideoObject(output_file_path)

            # Check if conversion was successful and do a few more checks for redundancy
            if (
                result == 0
                and not item.is_corrupt
                and not output_file_object.is_corrupt
            ):
                old_files.append(item)
                new_files.append(output_file_object)

            else:
                cprint(
                    f"\n{item.basename} could not be converted. Error code: {result}",
                    fg.red,
                    style.bold,
                )

    # Notify user of completion
    cprint("\nBatch conversion completed.", fg.green)
    return old_files, new_files


if __name__ == "__main__":
    with ExecutionTimer():
        args = parse_arguments()
        # Run the main function
        old_files, new_files = main(args.input_directory, args.output_directory)

        # Output how much data was saved in the conversion
        total_preproccessed_size = 0
        total_processed_size = 0
        for vid in old_files:
            total_preproccessed_size += vid.size
        for vid in new_files:
            total_processed_size += vid.size

        space_saved = ByteConverter(total_preproccessed_size - total_processed_size)

        cprint(f"\nSpace saved: {space_saved}", fg.green, style.bold)
        # Triple check validity of conversion and finally, remove old files
        for vid in new_files:
            if vid.is_corrupt:
                cprint(f"\n{vid.path} is corrupt", fg.red, style.underline)
                continue
            else:
                try:
                    os.remove(os.path.join(args.input_directory, vid.basename))
                except Exception as e:
                    cprint(f"\n{e}", fg.red, style.underline)
                    continue

        print("")
