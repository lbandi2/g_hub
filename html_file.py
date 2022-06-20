import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime
import os
from dotenv import load_dotenv
from utils import download_file, download_html

load_dotenv()

HOST = os.getenv('HOST_IP')
URL = f"http://{HOST}:12321"
FILENAME1 = "logitech1.xml"

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

def get_device_id(filename):
    with open(f"./data/{filename}") as html:
        html_content = BeautifulSoup(html, 'html.parser')
    links = html_content.find_all('a')
    for index, item in enumerate(links):
        if index == 3:
            return item.get('href')

def battery_info():
    download_html(URL + '/devices', "devices.html")
    device_id = get_device_id("devices.html")
    download_file(URL + device_id, FILENAME1)
    info = parse_file(f'./data/{FILENAME1}')
    return info

print(battery_info())