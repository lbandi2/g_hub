from xml.etree.ElementTree import fromstring, ElementTree
from bs4 import BeautifulSoup
from datetime import datetime
import os
from dotenv import load_dotenv
from utils import get_content, check_process, run_process

load_dotenv()

HOST = os.getenv('HOST_IP')
URL = f"http://{HOST}:12321"
PATH_TO_APP = './LG_SysTray_v2/LGSTrayGUI.exe'
CSV_FILE = './battery_table_g703.csv'

def info_is_zero(content):
    xml_file = ElementTree(fromstring(content))
    xml_file_root = xml_file.getroot()

    if xml_file_root[3].text.split(".")[0] == '0':
        return True
    return False

def parse(content, is_alt=False):
    battery = dict()
    try:
        xml_file = ElementTree(fromstring(content))
        xml_file_root = xml_file.getroot()

        if not is_alt:
            battery["error"] = "-"
            battery["timestamp"] = datetime.timestamp(datetime.now())
            battery["last_update"] = datetime.strftime(datetime.now(), "%m/%d/%Y %H:%M:%S")
            battery["name"] = xml_file_root[1].text
            battery["is_charging"] = xml_file_root[5].text
            battery["hours_remaining"] = int(float(xml_file_root[4].text))
            battery["level"] = int(xml_file_root[3].text.split(".")[0])
        else:
            battery["error"] = "-"
            battery["timestamp"] = datetime.timestamp(datetime.now())
            battery["last_update"] = datetime.strftime(datetime.now(), "%m/%d/%Y %H:%M:%S")
            battery["name"] = xml_file_root[1].text
            battery["is_charging"] = 'False'
            battery["hours_remaining"] = '-'
            battery["level"] = int(xml_file_root[4].text.split(".")[0])

    except:
        battery["error"] = "System Tray app is not running"
        battery["timestamp"] = datetime.timestamp(datetime.now())
        battery["last_update"] = datetime.strftime(datetime.now(), "%m/%d/%Y %H:%M:%S")
        battery["name"] = "-"
        battery["is_charging"] = "-"
        battery["hours_remaining"] = "-"
        battery["level"] = "-"
    return battery

def get_device_ids(content, idx=[0, 3]):
    html_content = BeautifulSoup(content, 'html.parser')
    links = html_content.find_all('a')
    result = []
    for index, item in enumerate(links):
        if index in idx:
            result.append(item.get('href'))
    
    if result != []:
        return result
    else:
        raise ValueError("Problem with LGSTray")

def battery_info():
    if not check_process(PATH_TO_APP):
        run_process(PATH_TO_APP, wait=10)
    devices = get_content(URL + '/devices')
    device_ids = get_device_ids(devices)

    for index, id in reversed(list(enumerate(device_ids))):
        mouse_info = get_content(URL + id)
        if index == 1:
            if info_is_zero(mouse_info):
                continue
                # run_process(PATH_TO_APP, wait=10) # restarts LGSTray if info is zero
            else:
                info = parse(mouse_info)
        elif index == 0:
            info = parse(mouse_info, is_alt=True)
        return info


# devices = get_content(URL + '/devices')
# device_id = get_device_id(devices, index=0)
# content = get_content(URL + device_id)
# print(parse(content, is_alt=True))
print(battery_info())