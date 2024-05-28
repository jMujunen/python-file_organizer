#!/usr/bin/env python3

# rootfs.py - create a minimal root filesystem

import os, sys

from FileSystem import FileTree, FileTreeNode

def make_pictures_tree(tree, root):
    """
    Pictures
    |- Photography
        |- Raw
            |- 2017
            |- 2018
            |- 2019
            |- 2020
            |- 2021
            |- 2022
            |- 2023
            |- 2024
            |- 2025
            |- Other
        |- 2017
        |- 2018
        |- 2019
        |- 2020
        |- 2021
        |- 2022
        |- 2023
        |- 2024
        |- 2025
        |- Other
        |- Childhood

    |- Screenshots
        |- Phone
        |- PC
    |- Phone
        |- 2017
        |- 2018
        |- 2019
        |- 2020
        |- 2021
        |- 2022
        |- 2023
        |- 2024
        |- 2025
        |- Other
    """

    pictures = FileTreeNode('Pictures', '/root/pictures', parent=root)
    tree.add_node(pictures)

    photography = FileTreeNode('Photography', '/root/pictures/photography', parent=pictures)
    tree.add_node(photography)

    photography_dirs =[
            FileTreeNode('Raw', '/root/pictures/photography/raw', parent=photography),
            FileTreeNode('2017', '/root/pictures/photography/2017', parent=photography),
            FileTreeNode('2018', '/root/pictures/photography/2018', parent=photography),
            FileTreeNode('2019', '/root/pictures/photography/2019', parent=photography),
            FileTreeNode('2020', '/root/pictures/photography/2020', parent=photography),
            FileTreeNode('2021', '/root/pictures/photography/2021', parent=photography),
            FileTreeNode('2022', '/root/pictures/photography/2022', parent=photography),
            FileTreeNode('2023', '/root/pictures/photography/2023', parent=photography),
            FileTreeNode('2024', '/root/pictures/photography/2024', parent=photography),
            FileTreeNode('2025', '/root/pictures/photography/2025', parent=photography),
            FileTreeNode('Other', '/root/pictures/photography/other', parent=photography),
            FileTreeNode('Childhood', '/root/pictures/photography/childhood', parent=photography)]
    for dir in photography_dirs:
        tree.add_node(dir)

    raw_dirs = [
            FileTreeNode('2017', '/root/pictures/photography/Raw/2017', parent='Raw'),
            FileTreeNode('2018', '/root/pictures/photography/Raw/2018', parent='Raw'),
            FileTreeNode('2019', '/root/pictures/photography/Raw/2019', parent='Raw'),
            FileTreeNode('2020', '/root/pictures/photography/Raw/2020', parent='Raw'),
            FileTreeNode('2021', '/root/pictures/photography/Raw/2021', parent='Raw'),
            FileTreeNode('2022', '/root/pictures/photography/Raw/2022', parent='Raw'),
            FileTreeNode('2023', '/root/pictures/photography/Raw/2023', parent='Raw'),
            FileTreeNode('2024', '/root/pictures/photography/Raw/2024', parent='Raw'),
            FileTreeNode('2025', '/root/pictures/photography/Raw/2025', parent='Raw'),
            FileTreeNode('Other', '/root/pictures/photography/Raw/other', parent='Raw'),
    ]
    for dir in raw_dirs:
        tree.add_node(dir)

    screenshots = FileTreeNode('Screenshots', '/root/pictures/screenshots', parent=pictures)
    tree.add_node(screenshots)

    Phone = FileTreeNode('Phone',  '/root/pictures/phone', parent=pictures)
    tree.add_node(photography)

    return tree, root




def main():
    tree = FileTree()
    root = FileTreeNode('root', '/')
    tree.add_node(root)

    tree, root = make_pictures_tree(tree, root)

    videos = FileTreeNode('Videos', '/root/videos', parent=root)
    Backups = FileTreeNode('Backups', '/root/backups', parent=root)
    Documents = FileTreeNode('Documents', '/root/documents', parent=root)
    Other = FileTreeNode('Other', '/root/other', parent=root)
    Code = FileTreeNode('Code', '/root/code', parent=root)
    tree.add_node(videos)
    tree.add_node(Backups)
    tree.add_node(Documents)
    tree.add_node(Other)
    tree.add_node(Code)
    tree.traverse()
    return tree, root

"""

STRUCTURE = {
    'Pictures': {
        'Photography': {
            '2018': [],
            '2019': [],
            '2020': [],
            '2021': [],
            '2022': [],
            '2023': [],
            '2024': [],
            'Childhood': [],
            'Other': []
        'Screenshots': [],
    },
    'Videos': {
        'OBS': [],
        'Dashcam': [],
        'Random': [],
        'Nikon': [],
        'Phone': []
    },
    'Backups': {
        'Timeshift': [],
        'Archive': [],
        'Other': []
    },
    'Documents': [],
    'Other': [],
    'Code': {
        'Python': [],
        'C': [],
        'Java': [],
        'HTML/CSS': [],
        
    }
} 
"""