GRANT_TYPE = 'client_credentials'

USER_ID = 131226714
TOKEN_URL = 'https://api.avito.ru/token'

# Текст ответа в будни в рабочее время с 09:00 до 18:59
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

# Текст в будни в нерабочее время:С 19:00 по 23:59
WEEKDAYS_19_TO_2359_ANSWERS = [
    """Здравствуйте. Получили ваше сообщение.
    Мы работаем с 09:00 до 19:00. Ответим Вам завтра утром.""",
    """Здравствуйте. Мы работаем с 09:00 до 19:00.
    Обязательно ответим Вам завтра утром.""",
    """Здравствуйте. Работаем с 09:00 до 19:00.
    Обязательно ответим вам завтра утром, после 09:00."""
]

# Текст в будни в нерабочее время с 00:00 по 08:59
WEEKDAYS_00_TO_0859_ANSWERS = [
    """Здравствуйте. Получили ваше сообщение.
    Мы работаем с 09:00 до 19:00. Ответим Вам утром, после 09:00.""",
    """Здравствуйте. Мы работаем с 09:00 до 19:00.
    Обязательно ответим вам после 09:00.""",
    """Здравствуйте. Работаем с 09:00 до 19:00.
    Ответим Вам после 09:00."""]
