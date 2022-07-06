import os
import requests
import psutil
import time
import json
import datetime
import csv

def read_csv(file):
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return list(csv_reader)

def get_content(url):
    try:
        file = requests.get(url)
        if "G703" in file.content.decode(encoding="utf-8"):
            return file.content.decode(encoding="utf-8")
    except:
        print("Logitech System Tray app is not running.")

def sanitize_path(path):
    return path.replace('/', '\\')

def file_from_path(path):
    path = sanitize_path(path)
    filename = path.split('\\')[-1]
    return filename

def check_process(path):
    filename = file_from_path(path)
    pids = psutil.pids()
    for item in pids:
        p = psutil.Process(item)
        if filename.lower() in p.name().lower():
            return True
    return False

def get_process_ids(name):
    ids = []
    for item in psutil.pids():
        p = psutil.Process(item)
        if name.lower() in p.name().lower():
            ids.append(p.pid)
    if ids != []:
        return ids
    return None

def kill_process(name, wait=3):
    pids = get_process_ids(name)
    if pids is not None:
        for pid in pids:
            p = psutil.Process(pid)
            p.terminate()
            print(f"Process {p.name()} killed")
            time.sleep(wait)
    else:
        print("Process not found")

def run_process(path, kill_previous=True, wait=0):
    path = sanitize_path(path)
    filename = file_from_path(path)
    if kill_previous:
        kill_process(filename)
    os.startfile(path)
    time.sleep(wait)

def dir_exist(path):
    return os.path.isdir(path)

def file_exist(filename):
    file_path = os.path.expandvars(filename)
    return os.path.isfile(file_path)

def make_dir(path):
    if not dir_exist(path):
        try:
            os.mkdir(path)
        except OSError:
            print (f"Failed to create directory '{path}'")
        else:
            print(f"Creating folder '{path}'..")

def list_files(dir='data'):
    if dir_exist(dir):
        if os.listdir(f'{dir}/.') != []:
            return f"./{dir}/{os.listdir(f'{dir}/.')[0]}"
        else:
            return None

def delete_last_file():
    if dir_exist('data'):
        filename = list_files()
        if list_files() is not None:
            if file_exist(filename):
                os.remove(filename)

def save_file(content):
    make_dir('data')
    delete_last_file()
    date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_path = f'./data/last_read-{date}.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def load_file():
    if dir_exist('data'):
        if not list_files():
            return False
        else:
            filename = list_files()
            if file_exist(filename):
                with open(filename) as f:
                    return json.load(f)
    return False

