#!/usr/bin/env python3

# remove_duplicate_media.py - Finds and removes duplicate images and videos.

import os
import sys
from time import sleep
import re
import shutil
import argparse

from ExecutionTimer import ExecutionTimer
from ProgressBar import ProgressBar
from MetaData import *
from Color import *

IGNORED_DIRS = [".Trash-1000", "Screenshots", "RuneLite"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compares hash values of images and removes any duplicates"
    )
    parser.add_argument("path", help="Path to the directory")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print the duplicate images that would be removed",
    )
    return parser.parse_args()


def main(args):

    with ExecutionTimer():
        hashes = {}
        duplicate_files = []
        directory = DirectoryObject(args.path)
        files = len(directory.files) + 1

        cprint(f"Found {files - 1} files", fg.green, style.bold)
        progress = ProgressBar(files)
        try:
            for item in directory:
                if (
                    "Trash-1000" in item.path
                    or "RuneLite" in item.path
                    or "Wallpaper" in item.path
                ):
                    continue

                if item.is_file:
                    progress.increment()
                if item.is_file and item.is_image:
                    hash = item.calculate_hash('dhash')
                    if hash in hashes.keys():
                        hashes[hash].append(item.path)
                        cprint(
                            f"{item.path} hash is similar to {hashes[hash]}",
                            fg.yellow,
                            style.bold,
                            end="\r",
                        )
                    else:
                        hashes[hash] = []
                        hashes[hash].append(item.path)
        except Exception as e:
            pass
        for k, v in hashes.items():
            if len(v) > 1:
                for img in v:
                    subprocess.run(
                        f'kitten icat --use-window-size 500,100,500,100 "{img}"',
                        shell=True,
                    )
                    duplicate_files.append(img)

                reply = input(f"\033[33mRemove these files? [Y/n]: \033[0m")
                if reply.lower() == "y" or reply == "":
                    for i, img in enumerate(v):
                        # Skip the first image
                        if i == 0:
                            continue
                        try:
                            os.remove(img)
                            cprint(f"{img} removed", fg.green, style.bold)
                        except FileNotFoundError:
                            cprint(f"{img} not found", fg.red, style.bold)
                            next
                else:
                    os.system("clear")
                    continue
        print("")


if __name__ == "__main__":
    args = parse_args()
    main(args)
