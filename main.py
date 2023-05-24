import json
import os
import random
import time
from datetime import datetime
import logging

import requests
import schedule
import yaml
from dotenv import load_dotenv

from constants import (GRANT_TYPE, TOKEN_URL,
                       WEEKDAYS_00_TO_0859_ANSWERS,
                       WEEKDAYS_19_TO_2359_ANSWERS, WEEKEND_ANSWERS,
                       WORKING_HOURS_ANSWERS)
from config import configure_logging
from exceptions import TokenRefreshException

load_dotenv()

USER_ID = os.getenv("USER_ID")
MESSEGE_URL = f"https://api.avito.ru/messenger/v2/accounts/{USER_ID}/chats"


def refresh_token():
    """
    Функция посылает запрос на обновление токена
    и записывает его в файл token.yml.
    Время действия токена ограничено — 24 часа с момента его получения.
    """
    logging.info('Попытка обновления токена')
    data = {
        "grant_type": GRANT_TYPE,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET")
    }
    try:
        req_token = requests.post(TOKEN_URL, data)
        data = json.loads(req_token.text)
        to_yaml = {"token": data["access_token"]}
    except Exception as e:
        raise TokenRefreshException(f'Ошибка получения токена. {e}')

    try:
        with open("token.yml", "w") as file:
            yaml.dump(to_yaml, file)
            logging.info('Токен успешно обновлен')
    except Exception as e:
        logging.warning(f'Ошибка обновления токена {e}')


def get_headers():
    """
    Функция получает сохраненный в файле token.yml токен
    и возвращает headers, необходимые для отправки запросов.
    """
    try:
        with open("token.yml") as file:
            token = yaml.safe_load(file)["token"]
        headers = {
            "Content_Type": "application/json",
            "Authorization": f"Bearer {token}"}
        return headers
    except Exception as e:
        logging.warning(f'Ошибка при работе функции get_headers - {e}')


def get_all_chats(headers):
    """
    Функция отправляет запрос на получение чатов,
    содержащих непрочитанные сообщения и возвращает их.
    """
    try:
        params = {
            "unread_only": "true"
        }
        chats = requests.get(MESSEGE_URL, headers=headers, params=params)
        return json.loads(chats.text)
    except Exception as e:
        logging.warning(f'Ошибка при работе функции get_all_chats - {e}')


def read_message(chat_id, headers):
    """
    Функция отмечает в переданном ей chat_id
    (чате) все входящие сообщения как прочитанные.
    """
    url = f"https://api.avito.ru/messenger/v1/accounts/{USER_ID}/chats/{chat_id}/read"

    try:
        chats = requests.post(url, headers=headers)
        print(chats)
    except Exception as e:
        logging.warning(f'Ошибка при работе функции read_message - {e}')


def send_message(chat_id, headers):
    """
    Функция отправляет сообщение. с текстом в зависимости от времени отправки.
    """
    url = f"https://api.avito.ru/messenger/v1/accounts/{USER_ID}/chats/{chat_id}/messages"
    if datetime.now().weekday() > 4:
        text = random.choice(WEEKEND_ANSWERS)
    else:
        time = str(datetime.now().time())
        if "10:00" <= time <= "17:59":
            text = random.choice(WORKING_HOURS_ANSWERS)
        elif "18:00" <= time <= "23:59":
            text = random.choice(WEEKDAYS_19_TO_2359_ANSWERS)
        else:
            text = random.choice(WEEKDAYS_00_TO_0859_ANSWERS)
    try:
        data = {
            "message": {
                "text": text},
            "type": "text"}
        chats = requests.post(url, headers=headers, data=json.dumps(data))
        logging.info(f'Сообщение отправлено! {text}, {chats}')
    except Exception as e:
        logging.warning(f'Ошибка при работе функции send_message - {e}')


def get_chat_messages(chat_id, headers):
    """
    Функция получает все сообщения в конкретном чате (chat_id).
    """
    url = f"https://api.avito.ru/messenger/v3/accounts/{USER_ID}/chats/{chat_id}/messages/"
    try:
        chats = requests.get(url, headers=headers)
        logging.info('Проверяем сообщения в чате')
        return json.loads(chats.text)
    except Exception as e:
        logging.warning(f'Ошибка при работе функции get_chat_messages - {e}')


def check_chat(chat):
    """
    Функция проверяет чат по пунктам:
    - последнее входящее сообщение было прислано не Авито
    - последнее сообщение было прислано не позднее чем 5 минут назад
    - в чате нет отправленных сообщений, только входящие
    Если чат соответствует критериям, функция возвращает True, иначе False
    """
    author_id = chat["last_message"]["author_id"]
    if author_id == 0:
        return False

    update_time = int(time.time()) - chat["updated"]
    if update_time < 3000:
        chat_id = chat["id"]
        messages = get_chat_messages(chat_id, headers=get_headers())
        for message in messages["messages"]:
            if message["direction"] == "out":
                logging.info(
                    f'В чате {chat_id} уже велась переписка, автоответ не нужен')
                return False
    logging.info('Нужно ответить на сообщение')
    return True


def check_upcoming_and_answer():
    logging.info('Проверяем входящие сообщения')
    chats = get_all_chats(headers=get_headers())
    try:
        chats = chats["chats"]
    except KeyError as e:
        logging.warning(f'Ошибка при работе функции check_upcoming_and_answer - KeyError {e}')
        refresh_token()
        chats = get_all_chats(headers=get_headers())
        chats = chats["chats"]
    try:
        if len(chats) > 0:
            logging.info('Сообщение есть')
            for chat in chats:
                if check_chat(chat):
                    chat_id = chat["id"]
                    send_message(chat_id, headers=get_headers())
        else:
            logging.info('Входящих сообщений нет')
    except Exception as e:
        logging.warning(f'Ошибка при работе функции check_upcoming_and_answer - {e}')


def main():
    configure_logging()
    logging.info('Автоответ запущен')
    schedule.every(23).hours.do(refresh_token)
    schedule.every(1).minutes.do(check_upcoming_and_answer)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
