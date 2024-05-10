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


class FileObject:
    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as f:
            self.content = f.read()
    @property
    def size(self):
        return int(os.path.getsize(self.path))
    @property
    def name(self):
        return str(os.path.basename(self.path))
    @property
    def extension(self):
        return str(os.path.splitext(self.path)[-1])
    def __eq__(self, other):
        print(self.content, other.content)
        return self.content == other.content


class ImageObject(FileObject):
    def __init__(self , path):
        super().__init__(path)
    def calculate_hash(self):
        try:
            with Image.open(self.path) as img:
                hash_value = imagehash.average_hash(img)
            return hash_value
        except UnidentifiedImageError as e:
            ERRORS.append(self.path)
            print(f"Error: {e}")
            return None
    @property
    def dimensions(self):
        """
        Calculate the dimensions of the image located at the specified path.
        Returns:
            Tuple[int, int]: width x height of the image in pixels.
        """
        with Image.open(self.path) as img:
            width, height = img.size
        return width, height
    @property
    def exif(self):
        # Open Image
        with Image.open(self.path) as img:
            data = img.getexif()
        return data
    @property
    def capture_date(self):
        # Iterating over all EXIF data fields
        for tag_id in self.exif:
            # Get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = self.exif.get(tag_id)
            # Decode bytes 
            if isinstance(data, bytes):
                data = data.decode()
            if str(tag).startswith('DateTime'):
                return data
        return None

class VideoObject(FileObject):
    def __init__(self, path):
        super().__init__(path)
    @property
    def metadata(self):
        with VideoFileClip(self.path) as clip:
            metadata = {
                "duration": clip.duration,
                "dimensions": (clip.size[0], clip.size[1]),
                "fps": clip.fps,
                "aspect_ratio": clip.aspect_ratio
            }
        return metadata
    @property
    def bitrate(self):
        ffprobe_cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            self.path
        ]
        ffprobe_output = subprocess.check_output(ffprobe_cmd).decode('utf-8')
        metadata = json.loads(ffprobe_output)
        capture_date = metadata['format']['tags'].get('creation_time')
        bit_rate = metadata['format']['bit_rate']
        return bit_rate

def main():
    with ExecutionTimer():
        """         
        for root, _ , files in os.walk(TARGET_DIR):
            folder = root.split(os.sep)[-1]

            for file in files:
                if file in IGNORED_FILES['ignored']:
                    continue
                if file in IGNORED_FILES['code']:
                    continue
                if file in IGNORED_FILES['text']:
                    continue
                if file in IGNORED_FILES['settings']:
                    continue
                if file in IGNORED_FILES['dupes']:
                    continue
 """


        file1 = TARGET_DIR #ImageObject("/mnt/hdd/IMPORTANT_MEDIA/from_4tb_hdd/from_windows/Pictures/Photography/Processed/DSC_0265.png")
        # file2 = ImageObject("/mnt/hdd/IMPORTANT_MEDIA/from_4tb_hdd/from_windows/Pictures/Photography/Processed/Truck1.png")
        # print(f'HASH:{file1.calculate_hash() == file2.calculate_hash()}')
        # print(f'DIMENSIONS:{file1.dimensions == file2.dimensions}\n{file1.dimensions}, {file2.dimensions}')
        # print(f'CAPTURE_DATE:{file1.capture_date == file2.capture_date}\n{file1.capture_date}, {file2.capture_date}')
        # print('\n\n')
        # print(f'EXIF:{file1.exif}, {file2.exif}')
        # print(f'SIZE:{file1.size == file2.size}\n{ByteConverter.convert_bytes(file1.size)}, {ByteConverter.convert_bytes(file2.size)}') 
 
        path = TARGET_DIR #"/mnt/hdd/IMPORTANT_MEDIA/from_4tb_hdd/from_windows/Videos/OBS/CSGO/dm_scoutx20.mp4"
        clip = VideoObject(path)
        print(clip.metadata)
        print(clip.bitrate)

if __name__ == '__main__': 
    main()