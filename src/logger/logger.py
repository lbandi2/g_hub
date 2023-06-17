import logging
from logging.handlers import TimedRotatingFileHandler

from utils import make_dir

def set_logger(filename, keep_backups=10) -> None:
    make_dir('logs')

    format = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(format)
    handler = TimedRotatingFileHandler(f'./logs/{filename}.log', 
                                        when="midnight", 
                                        interval=1, 
                                        encoding='utf8', 
                                        backupCount=keep_backups)
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

# set_logger()