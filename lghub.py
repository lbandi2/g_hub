from dataclasses import asdict

from utils import file_exist, check_process
from db import DB
from battery import BatteryKey, BatteryFile

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
                pass
            if not self.is_installed:
                print("[LGHUB] Program is not installed")
                self.error = "LGHUB is not installed"
            elif not self.is_running:
                print("[LGHUB] Program is not running")
                self.error = "LGHUB is not running"
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
            return BatteryKey(self.get_data())
        elif self.method == 'saved json_file':
            return BatteryFile(self.get_data())
        else:
            raise ValueError("[LGHUB] No method was specified")

    def data_to_publish(self):
        battery = self.read_battery()
        data = asdict(battery.content())
        data['last_refresh'] = battery.last_refresh
        data['error'] = battery.error if battery.error else self.error
        data['used_method'] = "key: battery/g703hero/percentage" if self.method == 'key' else 'saved json_file'
        return data
