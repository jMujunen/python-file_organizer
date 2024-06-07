#!/usr/bin/env python3
"""Get information about files in a directory"""

import os
import sys

from ExecutionTimer import ExecutionTimer

DIRECTORY = os.getcwd()

file_types = {
    'img': ['.jpg', '.jpeg', '.png', '.gif', '.heic', '.nef','.webp', 'svg', ],

    'doc': ['.pdf', '.doc', '.docx', '.txt', '.odt', '.pptx'],

    'video': ['.mp4', '.avi', '.mkv', '.wmv', '.webm', '.m4v'],

    'audio': ['.3ga', '.aac', '.ac3', '.aif', '.aiff',
         '.alac', '.amr', '.ape', '.au', '.dss',
         '.flac', '.flv', '.m4a', '.m4b', '.m4p',
         '.mp3', '.mpga', '.ogg', '.oga', '.mogg',
         '.opus', '.qcp', '.tta', '.voc', '.wav',
         '.wma', '.wv'],

    'zip': ['.zip', '.rar', '.tar', '.bz2', '.7z', '.gz', '.xz', '.tar.gz', '.tgz', '.zipx'],
    'raw': ['.cr2', '.nef', '.raf', '.mov'],

    'text': ['.txt', '.md', '.ini', '.log', '.json', '.csv', '.xml'],

    'code': ['.py', '.bat', '.sh', '.c', '.cpp', '.h', '.java', '.js', '.ts', '.php', '.html', '.css', '.scss'],
    'other': [],  # For any other file type
    'dupes': []  # For duplicate files
}

def count_file_types(directory):
    file_types = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            if file_extension:
                file_extension = file_extension[1:]  # remove the dot from the extension
                if file_extension in file_types:
                    file_types[file_extension] += 1
                    #file_types[file_extension]['count'] += 1
                    #file_types[file_extension]['size'] = int(os.path.getsize(os.path.join(root, file))) + file_types[file_extension]['size']
                else:
                    file_types[file_extension] = 1
                    #file_types[file_extension] = {'count': 1, 'size': int(os.path.getsize(os.path.join(root, file)))}

    return file_types


if __name__ == '__main__':
    if len(sys.argv) > 1:
        DIRECTORY = ''.join(sys.argv[1:])
    with ExecutionTimer():
        file_type_counts = count_file_types(DIRECTORY)
        for file_type, count in file_type_counts.items():
            print(f'{file_type}: {count}')
        #for file_type in file_type_counts.keys():
            #count = file_type_counts[file_type]['count']
            #size = file_type_counts[file_type]['size']

            #print(f"{file_type}: {count} - Size: {ByteConverter.convert_bytes(size)}")
