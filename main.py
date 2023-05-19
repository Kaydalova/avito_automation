import json
import os
import random
import time
from datetime import datetime

import requests
import schedule
import yaml
from dotenv import load_dotenv

from constants import (GRANT_TYPE, TOKEN_URL, USER_ID,
                       WEEKDAYS_00_TO_0859_ANSWERS,
                       WEEKDAYS_19_TO_2359_ANSWERS, WEEKEND_ANSWERS,
                       WORKING_HOURS_ANSWERS)

MESSEGE_URL = f"https://api.avito.ru/messenger/v2/accounts/{USER_ID}/chats"
BASE_URL = "https://api.avito.ru/messenger/"

load_dotenv()


def refresh_token():
    """
    Время действия токена ограничено — 24 часа с момента его получения.
    """
    data = {
        "grant_type": GRANT_TYPE,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET")
    }
    req_token = requests.post(TOKEN_URL, data)
    data = json.loads(req_token.text)
    to_yaml = {"token": data["access_token"]}

    with open("token.yml", "w") as file:
        yaml.dump(to_yaml, file)


def get_all_chats(headers):
    try:
        params = {
            "unread_only": "true"
        }
        chats = requests.get(MESSEGE_URL, headers=headers, params=params)
        return json.loads(chats.text)
    except Exception as e:
        print(e)


def read_message(chat_id, headers):
    url = f"https://api.avito.ru/messenger/v1/accounts/{USER_ID}/chats/{chat_id}/read"

    try:
        chats = requests.post(url, headers=headers)
        print(chats)
    except Exception as e:
        print(e)


def send_message(chat_id, headers):
    url = f"https://api.avito.ru/messenger/v1/accounts/{USER_ID}/chats/{chat_id}/messages"
    if datetime.now().weekday() > 4:
        text = random.choice(WEEKEND_ANSWERS)
    else:
        time = str(datetime.now().time())
        if "09:00" <= time <= "18:59":
            text = random.choice(WORKING_HOURS_ANSWERS)
        elif "19:00" <= time <= "23:59":
            text = random.choice(WEEKDAYS_19_TO_2359_ANSWERS)
        else:
            text = random.choice(WEEKDAYS_00_TO_0859_ANSWERS)
    try:
        data = {
            "message": {
                "text": "Здравствуйте! Мы ответим вам в ближайшее время!"},
            "type": text}
        chats = requests.post(url, headers=headers, data=json.dump(data))
        print(chats)
    except Exception as e:
        print(e)


def get_chat_messages(chat_id, headers):
    url = f"https://api.avito.ru/messenger/v3/accounts/{USER_ID}/chats/{chat_id}/messages/"
    try:
        chats = requests.get(url, headers=headers)
        return json.loads(chats.text)
    except Exception as e:
        print(e)


def check_upcoming_and_answer():
    with open("token.yml") as file:
        token = yaml.safe_load(file)["token"]
    headers = {
        "Content_Type": "application/json",
        "Authorization": f"Bearer {token}"}
    chats = get_all_chats(headers)
    for chat in chats['chats']:
        author_id = chat["last_message"]["author_id"]
        if author_id == 0:
            continue
        chat_id = chat["id"]
        update_time = int(time.time()) - chat["updated"]
        if update_time < 300:
            messages = get_chat_messages(chat_id, headers)
            if len(messages["messages"]) == 1 and messages["messages"][0]["direction"] == "in":
                send_message(chat_id, headers)


def main():
    schedule.every(23).hours.do(refresh_token())
    schedule.every(2).minute.do(check_upcoming_and_answer())

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
