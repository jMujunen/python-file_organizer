#!/usr/bin/env python3


from ExecutionTimer import ExecutionTimer
from ByteConverter import ByteConverter
from ProgressBar import ProgressBar

ERRORS = []

ROOT_DIR = os.getcwd()


# TODO: Make this a config file
# ------------------------------
SPECIAL_FOLDERS = {
    'OSRS': "./Random/OSRS",
    'OBS': "./Videos/OBS",
    'Screenshots': "./Pictures/Screenshots"
}

IGNORED_DIRS = ['.Trash-1000']
# -------------------------------
def main():
    with ExecutionTimer():
        return 

if __name__ == '__main__': 
    main()