import requests
import json
from constants import USER_ID
import yaml
import time
from urllib.parse import urljoin

MESSEGE_URL = f"https://api.avito.ru/messenger/v2/accounts/{USER_ID}/chats"
BASE_URL = "https://api.avito.ru/messenger/"


def get_all_messeges(headers):
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
    try:
        data = {
            "type": "text",
            "message": {
                "text": "Здравствуйте! Мы ответим вам в ближайшее время!"}}
        chats = requests.post(url, headers=headers, data=data)
        print(chats)
    except Exception as e:
        print(e)


def main():
    with open("token.yml") as file:
        token = yaml.safe_load(file)["token"]
    headers = {
        "Content_Type": "application/json",
        "Authorization": f"Bearer {token}"}

    chats = get_all_messeges(headers)
    for chat in chats['chats']:
        author_id = chat["last_message"]["author_id"]
        if author_id == USER_ID:
            continue
        update_time = int(time.time()) - chat["updated"]
        chat_id = chat["id"]
        send_message(chat_id, headers)


if __name__ == "__main__":
    main()
