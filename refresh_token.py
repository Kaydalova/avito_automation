import json
import logging
import os
from exceptions import TokenRefreshException

import requests
import yaml

from config import configure_logging
from constants import GRANT_TYPE, TOKEN_URL


def refresh_token():
    """
    Функция посылает запрос на обновление токена
    и записывает его в файл token.yml.
    Время действия токена ограничено — 24 часа с момента его получения.
    """
    logging.info('refresh_token')
    data = {
        "grant_type": GRANT_TYPE,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET")
    }
    try:
        token = requests.post(TOKEN_URL, data)
        data = json.loads(token.text)
        to_yaml = {"token": data["access_token"]}
    except Exception as e:
        raise TokenRefreshException(f'Ошибка получения токена. {e}')

    try:
        with open("token.yml", "w") as file:
            yaml.dump(to_yaml, file)
            logging.info('Токен успешно обновлен')
    except Exception as e:
        logging.warning(f'Ошибка обновления токена {e}')


def main():
    configure_logging()
    refresh_token()


if __name__ == "__main__":
    main()
