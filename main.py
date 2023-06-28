import json
import logging
import os
import random
import time
from datetime import datetime

import pytz
import requests
import yaml
from dotenv import load_dotenv

from config import configure_logging
from constants import (GET_CHAT_MESSAGES_URL, MESSEGE_URL, SEND_URL, TIME_ZONE,
                       WEEKDAYS_00_TO_0859_ANSWERS,
                       WEEKDAYS_19_TO_2359_ANSWERS, WEEKEND_ANSWERS,
                       WORKING_HOURS_ANSWERS)
from refresh_token import refresh_token

load_dotenv()

USER_ID = os.getenv("USER_ID")


def get_headers():
    """
    Функция получает сохраненный в файле token.yml токен
    и возвращает headers, необходимые для отправки запросов.
    """
    logging.info('get_headers')
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
    logging.info('get_all_chats')
    params = {"unread_only": "true"}
    try:
        chats = requests.get(
            MESSEGE_URL.format(USER_ID=USER_ID),
            headers=headers,
            params=params)
        return json.loads(chats.text)
    except (ConnectionError,
            TimeoutError,
            requests.exceptions.ConnectionError) as e:
        logging.warning(
            f'Ошибка при работе функции get_all_chats-{e}')
        try:
            time.sleep(100)
            refresh_token()
            headers = get_headers()
            chats = requests.get(
                MESSEGE_URL.format(USER_ID=USER_ID),
                headers=headers,
                params=params)
            return json.loads(chats.text)
        except Exception:
            logging.warning(
                f'Неудачный хэндлинг ConnectionError -{Exception}')
    except Exception as e:
        logging.warning(f'Новая ошибка при работе функции get_all_chats - {e}')


def send_message(chat_id, headers):
    """
    Функция отправляет сообщение. с текстом в зависимости от времени отправки.
    """
    logging.info('send_message')
    tz = pytz.timezone(TIME_ZONE)
    if datetime.now(tz).weekday() > 4:
        text = random.choice(WEEKEND_ANSWERS)
    else:
        time = str(datetime.now(tz).time())
        logging.info(f'time = {time}')

        if "10:00" <= time <= "17:59":
            logging.info('"10:00" <= time <= "17:59"')
            text = random.choice(WORKING_HOURS_ANSWERS)
        elif "18:00" <= time <= "23:59":
            logging.info('"18:00" <= time <= "23:59"')
            text = random.choice(WEEKDAYS_19_TO_2359_ANSWERS)
        else:
            logging.info('else')
            text = random.choice(WEEKDAYS_00_TO_0859_ANSWERS)
    try:
        data = {
            "message": {
                "text": text},
            "type": "text"}
        chats = requests.post(
            url=SEND_URL.format(USER_ID=USER_ID, chat_id=chat_id),
            headers=headers,
            data=json.dumps(data))
        logging.info(f'Сообщение отправлено! {text}, {chat_id}, {chats}')
    except Exception as e:
        logging.warning(f'Ошибка при работе функции send_message - {e}')


def get_chat_messages(chat_id, headers):
    """
    Функция получает все сообщения в конкретном чате (chat_id).
    """
    logging.info('get_chat_messages')
    try:
        chats = requests.get(
            url=GET_CHAT_MESSAGES_URL.format(USER_ID=USER_ID, chat_id=chat_id),
            headers=headers)
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
    logging.info('check_chat')
    author_id = chat["last_message"]["author_id"]
    if author_id == 0:
        return False

    update_time = int(time.time()) - chat["updated"]
    logging.info(f'time.time() = {time.time()}')
    logging.info(f'chat["updated"] = {chat["updated"]}')
    logging.info(f'update_time = {update_time}')

    if update_time < 300:
        chat_id = chat["id"]
        messages = get_chat_messages(chat_id, headers=get_headers())
        last_message = messages["messages"][0]
        for message in messages["messages"]:
            if (message["direction"] == "out" and (
                    message["created"]) > int(time.time()-10800)):
                logging.info(
                    f'В чате {chat_id} уже велась переписка.\
                        Последнее сообщение {last_message}')
                return False
        logging.info(f'Нужно ответить на сообщение chat_id {chat_id},\
                     text = {last_message["content"]["text"]}')
    return True


def check_upcoming_and_answer():
    logging.info('check_upcoming_and_answer')
    headers = get_headers()
    chats = get_all_chats(headers)
    try:
        chats = chats["chats"]
    except KeyError as e:
        logging.warning(f'KeyError {e}')
        refresh_token()
        headers = get_headers()
        chats = get_all_chats(headers)
        chats = chats["chats"]

    try:
        if len(chats) > 0:
            logging.info('Сообщение есть')
            for chat in chats:
                if check_chat(chat):
                    chat_id = chat["id"]
                    send_message(chat_id, headers)
        else:
            logging.info('Входящих сообщений нет')
    except Exception as e:
        logging.warning(
            f'Ошибка при работе check_upcoming_and_answer - {e}')


def main():
    configure_logging()
    check_upcoming_and_answer()


if __name__ == "__main__":
    main()
