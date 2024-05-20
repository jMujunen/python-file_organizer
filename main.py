#!/usr/bin/env python3

import sys, os, shutil
import subprocess
import json
import re

from PIL import Image
from PIL import UnidentifiedImageError
from PIL.ExifTags import TAGS
from moviepy.editor import VideoFileClip

import imagehash

from ExecutionTimer import ExecutionTimer
from ByteConverter import ByteConverter
from ProgressBar import ProgressBar

ERRORS = []
TARGET_DIR = '/mnt/hdd/IMPORTANT_MEDIA/from_4tb_hdd/from_windows/Videos/Dashcam/Honeymoon clips/2021_0709_102802_626.MOV'
ROOT_DIR = os.getcwd()

FILE_TYPES = {
    'img': ['.jpg', '.jpeg', '.png', '.gif', '.heic', '.nef','.webp', '.svg', '.ico', '.heatmap'],

    'doc': ['.pdf', '.doc', '.docx', '.txt', '.odt', '.pptx'],
    
    'video': ['.mp4', '.avi', '.mkv', '.wmv', '.webm', '.m4v', '.flv', '.mpg'],

    'audio': ['.3ga', '.aac', '.ac3', '.aif', '.aiff',
         '.alac', '.amr', '.ape', '.au', '.dss',
         '.flac', '.flv', '.m4a', '.m4b', '.m4p',
         '.mp3', '.mpga', '.ogg', '.oga', '.mogg',
         '.opus', '.qcp', '.tta', '.voc', '.wav',
         '.wma', '.wv'],

    'zip': ['.zip', '.rar', '.tar', '.bz2', '.7z', '.gz', '.xz', '.tar.gz', '.tgz', '.zipx'],

    'raw': ['.cr2', '.nef', '.raf', '.mov', '.dng', '.raf'],

    'settings': ['.properties', 'ini', '.config', '.cfg', '.conf', '.yml', '.yaml'],

    'text': ['.txt', '.md', '.log', '.json', '.csv', '.xml'],

    'code': ['.py', '.bat', '.sh', '.c', '.cpp', '.h', '.java', '.js', '.ts', '.php', '.html', '.css', '.scss', '.xmp'],
    'other': ['.lrprev', '.dat', '.db', '.dbf', '.mdb', '.sqlite', '.sqlite3', '.exe'],  # For any other file type
    'ignored': ['.trashinfo', '.lnk', '.plist', '.shadow','directoryStoreFile','indexArrays', 'indexBigDates','indexCompactDirectory', 'indexDirectory','indexGroups','indexHead', 'indexIds','indexPositions', 'indexPostings','indexUpdates', 'shadowIndexGroups','shadowIndexHead', 'indexPositionTable','indexTermIds', 'shadowIndexArrays','shadowIndexCompactDirectory', 'shadowIndexDirectory','shadowIndexTermIds', '.updates', '.loc', '.state', '.37', '.tmp', '.pyc'],
    'dupes': []  # For duplicate files
}


SPECIAL_FOLDERS = {
    'OSRS': "./Random/OSRS",
    'OBS': "./Videos/OBS",
    'Screenshots': "./Pictures/Screenshots"
}

IGNORED_DIRS = ['.Trash-1000']


def main():
    with ExecutionTimer():
        return 
if __name__ == '__main__': 
    main()