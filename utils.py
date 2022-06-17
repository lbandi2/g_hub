import os
import requests

def dir_exist(path):
    return os.path.isdir(path)

def make_dir(path):
    if not dir_exist(path):
        try:
            os.mkdir(path)
        except OSError:
            print (f"Failed to create directory '{path}'")
        else:
            print(f"Creating folder '{path}'..")

def download_file(url, filename):
    if os.path.exists(f"./data/{filename}"):
        os.remove(f"./data/{filename}")
    try:
        counter = 1
        while True:
            print(url)
            file = requests.get(url)
            if "G703" in file.content.decode(encoding="utf-8"):
                with open(f'./data/{filename}', "wb") as f:
                    f.write(file.content)
                break
            else:
                if counter > 9:
                    url = url[:-2] + str(counter)
                else:
                    url = url[:-1] + str(counter)
                counter += 1
                pass
    except:
        print("Logitech System Tray app is not running.")
