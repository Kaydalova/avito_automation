import yaml
from constants import BASE_DIR, LOG_DIR, LOG_FILE 
import logging
from logging.handlers import RotatingFileHandler


LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


with open("token.yml") as file:
    token = yaml.safe_load(file)["token"]


def configure_logging():
    log_dir = BASE_DIR / LOG_DIR
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / LOG_FILE
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        # Уровень записи логов.
        level=logging.INFO,
        # Вывод логов в терминал.
        handlers=(rotating_handler, logging.StreamHandler())
    )