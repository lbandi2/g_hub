import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import math

from utils import load_file, save_file

logger = logging.getLogger()


@dataclass
class BatteryInfo:
    timestamp: datetime = (datetime.now() - timedelta(hours=5)).timestamp()
    level: int = 0
    hours_remaining: int = 0
    millivolts: int = 0
    is_charging: bool = False
    last_update: datetime = None


class Battery:
    JSON_KEY = 'battery/g703hero/percentage'
    BATTERY_HOURS = {'100' : 39}

    def __init__(self, data: dict, method = None, json_key = JSON_KEY) -> None:
        self.data = data
        self.method = method
        self.json_key = json_key
        self.error = None

    @property
    def last_refresh(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def hours_remaining(self, num):
        return round(math.floor(num * self.BATTERY_HOURS['100'] / 100))

    def content(self):
        pass


class BatteryKey(Battery):
    JSON_KEY = 'battery/g703hero/percentage'

    def __init__(self, data: dict, method='key') -> None:
        super().__init__(data, method)
        logger.info(f"Reading battery info from db key: {self.JSON_KEY}")
        self.save_file()

    def content(self):
        content = self.read_from_key()
        return content

    # def save_file(self):
    #     save_file(asdict(self.content()), dir='data', filename_prefix='new_file')

    def is_same_as_file(self, data):
        json_data = load_file()
        return json_data == data

    def save_file(self):
        new_data = asdict(self.content())
        if not self.is_same_as_file(new_data):
            save_file(asdict(self.content()), dir='data', filename_prefix='new_file')
            logger.debug("Collected info is new, saving json to file")
        else:
            logger.debug("Collected info matches the info in json file, not saving")

    def read_from_key(self):
        data = self.data[self.json_key]
        is_charging = 'isCharging' in data
        level = data.get('percentage')
        hours_remaining = self.hours_remaining(level)
        millivolts = data.get('millivolts')
        timestamp = datetime.timestamp((datetime.strptime(data.get('time'), '%Y-%m-%dT%H:%M:%SZ') - timedelta(hours=5)))
        last_update = (datetime.fromtimestamp(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        content = BatteryInfo(
            timestamp, 
            level,
            hours_remaining,
            millivolts,
            is_charging,
            last_update
            )
        return content


class BatteryFile(Battery):
    def __init__(self, data: dict, method='json_file') -> None:
        super().__init__(data, method)

    def content(self):
        content = self.read_from_file()
        return content

    def read_from_file(self):
        file = load_file(dir='data')
        if not file:
            content = BatteryInfo()
            message = 'No info from db key nor json file'
            logger.warning(message)
            self.error = message
        else:
            is_charging = file.get('is_charging')
            level = file.get('level')
            hours_remaining = file.get('hours_remaining')
            millivolts = file.get('millivolts')
            timestamp = file.get('timestamp')
            last_update = file.get('last_update')

            content = BatteryInfo(
                timestamp, 
                level,
                hours_remaining,
                millivolts,
                is_charging,
                last_update
                )
        return content
