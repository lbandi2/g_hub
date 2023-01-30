import logging
import atexit
import os

from runsingle import runSingle
from publish import publish_to_mqtt
from logger import set_logger

## Needs LGHUB from Logitech installed and running

#
# This program reads the info provided by LGHUB
#
# - reads battery information from sqlite db stored by LGHUB
# - reports battery status to mqtt
#

a = runSingle("lock.ignore") # prevents script from running more than once at the same time

set_logger(filename='main', keep_backups=10)
logger = logging.getLogger()

def log_program_exit():
    logger.info("Exiting main program")

def main():
    logger.info("Starting main program")
    atexit.register(log_program_exit)
    publish_to_mqtt(broker=os.getenv('MQTT_BROKER'), 
                    user=os.getenv('MQTT_USER'), 
                    password=os.getenv('MQTT_PASS'))

if __name__ == '__main__':
    main()