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
        # Create the output directory if it doesn't exist
        os.makedirs(output_directory.path, exist_ok=True)
    except OSError as e:
        print(
            f"[\033[31m Error creating output directory '{output_directory}': {e} \033[0m]"
        )
        return

    # Get total files
    number_of_files = len(input_directory) + 1

    progress = ProgressBar(number_of_files)

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
                # Remove file if it is corrupt
                if output_file_object.is_corrupt:
                    os.path.remove(output_file_object.path)
                # If metadata is the same but size if different, its already compressed so skip
                # and flag for removal of old file
                elif (
                    output_file_object.metadata == item.metadata
                    and output_file_object.size != item.size
                ):
                    old_files.append(item)
                    new_files.append(output_file_object)
                    continue
                # Otherwise rename the file by appending _1, _2, etc.
                elif (
                    output_file_object.basename == item.basename
                    and not output_file_object.is_corrupt
                    and item.size != output_file_object.size
                ):
                    count = 0
                    # Loop until a unique name is found
                    while True:
                        try:
                            # Rename the file: "input_file.mp4" -> "input_file_1.mp4"
                            new_path = f"{output_file_path[:-4]}_{str(count)}.mp4"
                            shutil.move(new_path)
                            item = VideoObject(new_path)
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
                f'ffmpeg -i "{item.path}" -c:v h264_nvenc -crf 18 -qp 18 "{output_file_path}"',
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
