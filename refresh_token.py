import json
import os

import requests
import yaml
from dotenv import load_dotenv

from constants import GRANT_TYPE

load_dotenv()

token_url = 'https://api.avito.ru/token'

data = {
    "grant_type": GRANT_TYPE,
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("CLIENT_SECRET")
}
req_token = requests.post(token_url, data)
data = json.loads(req_token.text)
to_yaml = {"token": data["access_token"]}

with open("token.yml", "w") as file:
    yaml.dump(to_yaml, file)
