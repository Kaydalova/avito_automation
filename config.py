import datetime
import logging
from logging.handlers import RotatingFileHandler

import pytz

from constants import BASE_DIR, LOG_DIR, LOG_FILE, LOG_FORMAT, TIME_ZONE


class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""
    def converter(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        tzinfo = pytz.timezone(TIME_ZONE)
        return tzinfo.localize(dt)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s


def configure_logging():
    log_dir = BASE_DIR / LOG_DIR
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / LOG_FILE
    logger = logging.root
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5)
    rotating_handler.setFormatter(Formatter(LOG_FORMAT))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(Formatter(LOG_FORMAT))
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    logger.addHandler(rotating_handler)
