from pathlib import Path

BASE_DIR = Path(__file__).parent

# LOGGING
LOG_DIR = 'logs'
LOG_FILE = 'avito.log'
TIME_ZONE = 'Europe/Moscow'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'


GRANT_TYPE = 'client_credentials'

# URLS
TOKEN_URL = 'https://api.avito.ru/token'
BASE_URL = "https://api.avito.ru/messenger/"
MESSEGE_URL = "https://api.avito.ru/messenger/v2/accounts/{USER_ID}/chats"
READ_URL = "https://api.avito.ru/messenger/v1/accounts/{USER_ID}/chats/{chat_id}/read"
SEND_URL = "https://api.avito.ru/messenger/v1/accounts/{USER_ID}/chats/{chat_id}/messages"
GET_CHAT__MESSAGES_URL = "https://api.avito.ru/messenger/v3/accounts/{USER_ID}/chats/{chat_id}/messages/"

THREE_HOURS_IN_SECONDS = 10800

# Текст ответа в будни в рабочее время с 10:00 до 17:59
WORKING_HOURS_ANSWERS = [
    """Здравствуйте. Получили ваше сообщение.
Как только освободимся – сразу Вам ответим.""",
    "Добрый день, скоро Вам ответим.",
    "Доброго дня, ответим Вам в ближайшее время."]


# Текст в выходные с 00:00 по 23:59
WEEKEND_ANSWERS = [
    """Здравствуйте. Получили ваше сообщение.
Мы работаем с понедельника по пятницу. Ответим Вам в понедельник утром.""",
    """Здравствуйте. Мы работаем с Пн по Пт.
Выходные Сб и Вс. Обязательно ответим Вам в Пн утром.""",
    """Здравствуйте. Работаем с Пн по Пт.
Выходные дни Сб и Вс. Обязательно ответим вам утром в Пн."""]

# Текст в будни в нерабочее время:С 18:00 по 23:59
WEEKDAYS_19_TO_2359_ANSWERS = [
    """Здравствуйте. Получили ваше сообщение.
Мы работаем с 10:00 до 18:00. Ответим Вам завтра утром.""",
    """Здравствуйте. Мы работаем с 10:00 до 18:00.
Обязательно ответим Вам завтра утром.""",
    """Здравствуйте. Работаем с 10:00 до 18:00.
Обязательно ответим вам завтра утром, после 10:00."""
]

# Текст в будни в нерабочее время с 00:00 по 09:59
WEEKDAYS_00_TO_0859_ANSWERS = [
    """Здравствуйте. Получили ваше сообщение.
Мы работаем с 10:00 до 18:00. Ответим Вам утром, после 10:00.""",
    """Здравствуйте. Мы работаем с 10:00 до 18:00.
Обязательно ответим вам после 10:00.""",
    """Здравствуйте. Работаем с 10:00 до 18:00.
Ответим Вам после 10:00."""]
