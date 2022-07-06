import os
import sqlite3
import json
from datetime import datetime, timedelta
import math
from utils import save_file, load_file, check_process, file_exist

DB_FILE_PATH = '%LOCALAPPDATA%/LGHUB/settings.db'
LGHUB_FILES = '%PROGRAMFILES%/LGHUB/lghub.exe'
BATTERY_HOURS = {'100' : 39}

def get_ts(time_string):
    return datetime.timestamp(datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ'))

def hours_remaining(num):
    return round(math.floor(num * BATTERY_HOURS['100'] / 100))

def fetch_data(db_file):
    try:
        file_path = os.path.expandvars(db_file)
        sqlite_connection = sqlite3.connect(file_path)
        cursor = sqlite_connection.cursor()

        for row in cursor.execute('SELECT FILE from DATA'):
            json_data = json.loads(row[0])

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

        return json_data

def parse_data(json_data):
    battery_info = {}
    lghub_is_running = check_process('lghub.exe')
    error_msg = '-'
    is_charging = False
    if 'battery/g703hero/percentage' in json_data:
        data = json_data['battery/g703hero/percentage']
        if 'isCharging' in data:
            is_charging = data['isCharging']
        used_method = 'key: battery/g703hero/percentage'
        battery_info['level'] = data['percentage']
        battery_info['hours_remaining'] = hours_remaining(data['percentage'])
        battery_info['millivolts'] = data['millivolts']
        ts = get_ts(data['time'])
        battery_info['timestamp'] = ts
        battery_info['last_update'] = (datetime.fromtimestamp(ts) - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')
        battery_info['is_charging'] = is_charging
        save_file(battery_info)
    elif 'battery/g703hero/percentage' not in json_data:
        if not load_file(): # if json file is not present
            used_method = '-'
            battery_info['level'] = 0
            battery_info['hours_remaining'] = 0
            battery_info['millivolts'] = 0
            battery_info['timestamp'] = datetime.timestamp(datetime.now())
            battery_info['last_update'] = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%Y-%m-%d %H:%M:%S')
            battery_info['is_charging'] = is_charging
        else:
            data = load_file() # load json file when present
            used_method = 'saved json_file'
            battery_info['level'] = data['level']
            battery_info['hours_remaining'] = hours_remaining(data['level'])
            battery_info['millivolts'] = data['millivolts']
            battery_info['timestamp'] = data['timestamp']
            battery_info['last_update'] = (datetime.fromtimestamp(data['timestamp']) - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')
            battery_info['is_charging'] = data['is_charging']
    else:
        raise Exception("No data returned from DB query.")
    battery_info['used_method'] = used_method

    if not file_exist(LGHUB_FILES):
        error_msg = 'LGHUB is not installed'
    if not lghub_is_running:
        error_msg = 'LGHUB is not running'
    if not load_file():
        error_msg = 'Waiting for update'

    battery_info['error'] = error_msg
    return battery_info

def battery_info():
    data = fetch_data(DB_FILE_PATH)
    return parse_data(data)

if __name__ == '__main__':
    print(battery_info())

