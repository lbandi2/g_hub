import logging
from dataclasses import asdict

from utils import file_exist, check_process, list_files
from src.db.db import DB
from src.battery.battery import BatteryKey, BatteryFile

logger = logging.getLogger()


class LGHUB:
    LGHUB_FILES = '%PROGRAMFILES%/LGHUB/lghub.exe'
    PROCESS = 'lghub.exe'

    def __init__(self):
        self.db = self.get_db()
        self.data = self.get_data()
        self.error = '-'

    def get_db(self):
        return DB()

    @property
    def is_installed(self):
        return file_exist(self.LGHUB_FILES)

    @property
    def is_running(self):
        return check_process(self.PROCESS)

    def is_valid(func):
        def wrapper(self):
            if all([self.is_installed, self.is_running]):
                # message = "LGHUB is installed and running"
                # logger.debug(message)
                pass
            if not self.is_installed:
                message = "LGHUB is not installed"
                logger.warning(message)
                self.error = message
            elif not self.is_running:
                message = "LGHUB is not running"
                logger.warning(message)
                self.error = message
            return func(self)
        return wrapper

    @is_valid
    def get_data(self):
        return self.get_db().read_file()

    @property
    def method(self):
        return 'key' if self.get_db().is_key_in_data() else 'saved json_file'

    def read_battery(self):
        if self.method == 'key':
            # info = BatteryKey(self.get_data())
            # return info
            return BatteryKey(self.get_data())
        elif self.method == 'saved json_file':
            info = BatteryFile(self.get_data())
            file = list_files().split('/')[-1]
            logger.info(f"DB key {info.json_key} not found")
            logger.info(f"Reading battery info from json file: {file}")
            return info
        else:
            message = "[LGHUB] No method was specified for reading the battery info"
            logger.critical(message)
            raise ValueError(message)

    def data_to_publish(self):
        battery = self.read_battery()
        data = asdict(battery.content())
        data['last_refresh'] = battery.last_refresh
        data['error'] = battery.error if battery.error else self.error
        data['used_method'] = f"key: {battery.json_key}" if self.method == 'key' else 'saved json_file'
        return data
