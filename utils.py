import os
import psutil
import json
import datetime
import csv
from typing import List, Dict

def read_csv(file: str) -> List[Dict]:
    """
    Reads a CSV file and returns a list of items
    """
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return list(csv_reader)

def sanitize_path(path: str) -> str:
    return path.replace('/', '\\')

def file_from_path(path: str) -> str:
    """
    Extracts filename from path
    """
    path = sanitize_path(path)
    filename = path.split('\\')[-1]
    return filename

def check_process(path: str) -> bool:
    """
    Checks if given process is actually running
    """
    filename = file_from_path(path)
    return filename in (process.name() for process in psutil.process_iter())

def dir_exist(path: str) -> bool:
    """
    Checks if a directory exists
    """
    return os.path.isdir(path)

def file_exist(filename: str) -> bool:
    """
    Checks if a file exists
    """
    file_path = os.path.expandvars(filename)
    return os.path.isfile(file_path)

def make_dir(path: str) -> None:
    """
    Creates a directory and informs if not successfull
    """
    if not dir_exist(path):
        try:
            os.mkdir(path)
        except OSError:
            print (f"Failed to create directory '{path}'")
        else:
            print(f"Creating folder '{path}'..")

def list_files(dir='data') -> str:
    """
    Lists files in a given directory
    """
    if dir_exist(dir):
        if os.listdir(f'{dir}/.') != []:
            return f"./{dir}/{os.listdir(f'{dir}/.')[0]}"
        else:
            return None

def delete_last_file(dir='data') -> None:
    """
    Deletes last file created in a given directory
    """
    if dir_exist(dir):
        filename = list_files(dir)
        if list_files(dir) is not None:
            if file_exist(filename):
                os.remove(filename)

def save_file(content: dict, dir='data', filename_prefix='last_read') -> None:
    """
    Creates a dir, deletes last file and saves a file in a given directory
    """
    make_dir(dir)
    delete_last_file(dir)
    date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_path = f'./{dir}/{filename_prefix}-{date}.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def load_file(dir='data') -> json:
    """
    Loads a file from a given directory and returns a json file
    """
    if dir_exist(dir) and list_files():
        filename = list_files()
        if file_exist(filename):
            with open(filename) as f:
                try:
                    return json.load(f)
                except json.decoder.JSONDecodeError:
                    pass
    return False

