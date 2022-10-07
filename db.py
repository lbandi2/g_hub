import os
import json
import sqlite3

from utils import file_exist, save_file


class DB:
    DB_FILE_PATH = '%LOCALAPPDATA%/LGHUB/settings.db'
    JSON_KEY = 'battery/g703hero/percentage'

    def __init__(self):
        self.file_path = self.DB_FILE_PATH
        self.data = self.read_file()
        self.key = self.JSON_KEY

    def path_exist(func):
        def wrapper(self):
            if file_exist(self.file_path):
                return func(self)
            else:
                raise ValueError(f"[DB] File not found: '{self.file_path}'")
        return wrapper

    @path_exist
    def read_file(self):
        try:
            file_path = os.path.expandvars(self.DB_FILE_PATH)
            sqlite_connection = sqlite3.connect(file_path)
            cursor = sqlite_connection.cursor()
            for row in cursor.execute('SELECT FILE from DATA'):
                json_data = json.loads(row[0])
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        except:
            print("Something unexpected happened reading from sqlite table")
        finally:
            if sqlite_connection:
                sqlite_connection.close()
            return json_data

    def is_key_in_data(self):
        return self.key in self.data

    # def format_info(self):
    #     battery = {}

    # def save_content(self):
    #     if self.is_key_in_data():
    #         save_file(self.data)

