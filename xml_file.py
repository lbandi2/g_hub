import xml.etree.ElementTree as ET
from datetime import datetime
import os
from dotenv import load_dotenv
from utils import download_file

load_dotenv()

HOST = os.getenv('HOST_IP')
URL1 = f"http://{HOST}:12321/device/dev00000001"
URL2 = f"http://{HOST}:12321/device/5D2C3B20"
FILENAME1 = "logitech1.xml"
FILENAME2 = "logitech2.xml"

def parse_file(filename):
    battery = dict()
    try:
        xml_file = ET.parse(filename)
        xml_file_root = xml_file.getroot()

        battery["error"] = "-"
        battery["timestamp"] = datetime.timestamp(datetime.now())
        battery["last_update"] = datetime.strftime(datetime.now(), "%m/%d/%Y %H:%M:%S")
        battery["name"] = xml_file_root[1].text
        battery["is_charging"] = xml_file_root[5].text
        battery["hours_remaining"] = int(float(xml_file_root[4].text))
        battery["level"] = int(xml_file_root[3].text.split(".")[0])

    except FileNotFoundError:
        battery["error"] = "System Tray app is not running"
        battery["timestamp"] = datetime.timestamp(datetime.now())
        battery["last_update"] = datetime.strftime(datetime.now(), "%m/%d/%Y %H:%M:%S")
        battery["name"] = "-"
        battery["is_charging"] = "-"
        battery["hours_remaining"] = "-"
        battery["level"] = "-"

    return battery

def battery_info():
    download_file(URL1, FILENAME1)
    info = parse_file(f'./data/{FILENAME1}')
    return info

print(battery_info())