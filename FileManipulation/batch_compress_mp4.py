#!/usr/bin/env python3

# bp_mp4_cs.py - Batch process all .mp4 files in a directory

import os
import subprocess
import argparse
import sys
import cv2

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


def write_to_file(file_path, content):
    with open(file_path, "w") as file:
        for line in content:
            file.write(line + "\n")


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
        print(
            f"[\033[31m Error creating output directory '{output_directory}': {e} \033[0m]"
        )
        return

    # Get total files
    number_of_files = len(input_directory) + 1

    progress = ProgressBar(number_of_files)

    # Iterate over all .mp4 files in the input directory
    for i, input_file in enumerate(input_directory):
        progress.increment()
        if input_file.basename.endswith(".mp4"):
            # video = VideoObject(os.path.join(input_directory, input_file))

            # Extract the file name without extension
            # (some_video_file_name.getsome.arhagag.mp4) -> (some_video_file_name.getsome.arhagag)
            # file_name = os.path.splitext(input_file)[0]

            try:
                # Define the output file path
                output_file_path = os.path.join(
                    output_directory.path, input_file.basename
                )
            except Exception as e:
                cprint(f"\n{e}", fg.red, style.underline)
                continue
            # Check if the output file already exists
            if os.path.exists(output_file_path):
                output_file_object = VideoObject(output_file_path)
                # Remove file if it is corrupt
                if output_file_object.is_corrupt:
                    os.path.remove(output_file_path)
                # If metadata is the same but size if different, its already compressed so skip
                # and flag for removal of old file
                elif (
                    output_file_object.metadata == input_file.metadata
                    and output_file_object.size != input_file.size
                ):
                    compressed_files.append(input_file)
                    cprint(
                        f"\n{input_file.basename} is already compressed",
                        fg.red,
                        style.underline,
                    )
                    continue
                elif (
                    output_file_object.basename == input_file.basename
                    and not output_file_object.is_corrupt
                    and input_file.size != output_file_object.size
                ):
                    count = 0
                    while True:
                        try:
                            shutil.move(
                                input_file.path,
                                input_file.path[:-4] + "_" + str(count) + ".mp4",
                            )
                        except FileExistsError:
                            count += 1
                            continue
                        else:
                            break
                else:
                    (
                        os.remove(input_file.path)
                        if not input_file.is_corrupt
                        else cprint(
                            "FATAL ERROR: Manual intervention required",
                            fg.red,
                            style.underline,
                        )
                    )
                    continue
            # Run ffmpeg command for each file
            result = subprocess.run(
                f"ffmpeg -i '{input_file.path}' \
                    -c:v h264_nvenc -rc constqp -qp 28 '{output_file_path}' -n",
                shell=True,
                capture_output=True,
                text=True,
            )
            result = result.returncode

            # Check if conversion was successful
            if (
                result == 0
                and not input_file.is_corrupt
                and not output_file_object.is_corrupt
            ):
                compressed_files.append(input_file)
            else:
                cprint(
                    f"\n{input_file.basename} could not be converted. Error code: {result}",
                    fg.red,
                    style.bold,
                )
    cprint("\nBatch conversion completed.", fg.green)
    return compressed_files


if __name__ == "__main__":
    with ExecutionTimer():
        args = parse_arguments()
        sucessfully_compressed_files = compress(
            args.input_directory, args.output_directory
        )

        for vid in sucessfully_compressed_files:
            if vid.is_corrupt:
                cprint(f"\n{vid.path} is corrupt", fg.red, style.underline)
                continue
            else:
                os.remove(os.path.join(args.input_directory, vid.basename))

        print("")
