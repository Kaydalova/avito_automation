# avito_automation

***
Скрипт позволяет настроить автоответчик в Авито для вашего профиля.
Автоответ повысить ваш внутренний рейтинг авито и сделает профиль более дружелюбным для потенциальных клиентов:
- быстрая реакция на входящие сообщения даже в нерабочее время. Потенциальный клиент не остается без ответа, не будет раздражен из-за длительного ожидания.
- разный текст сообщения в зависимости от дня недели и времени суток

Скрипт готов к работе и снабжен логированием.
***

## Tecnhologies:
- Python 3.8
- Nginx
- Docker

### Как пользоваться скриптом:
- Скопируйте проект на свой ПК
```
git clone git@github.com:Kaydalova/avito_automation.git
```
- Перейдите в директорию проекта и создайте .env файл со следующим наполнением
```
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
USER_ID = XXXXXXXXX
```
- Создаем и активируем виртуальное окружение, устанавливаем необходимые модули:
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
- Кастомизировать список возможных сообщений для отправки можно в файле constants.py

#### Запуск скрипта через cron
Cron — инструмент Unix-систем для планирования выполнения команд на определённое время.
- Для отображения содержимого crontab-файла текущего пользователя используйте команду:
```
crontab -l
```

- Для редактирования заданий пользователя есть команда:
```
crontab -e
```

- Если эта команда выполняется в первый раз, вам предложат выбрать редактор для Cron:
```
no crontab for sk - using an empty one

Select an editor. To change later, run 'select-editor'.
 1. /bin/nano <---- простейший
 2. /usr/bin/vim.basic
 3. /usr/bin/vim.tiny
 4. /bin/ed

Choose 1-4 [1]:
```
- После выбора редактора откроется crontab-файл. В этом файле как раз нужно перечислять одну за другой все команды.
Ниже приведены несколько примеров cron-заданий.

- Чтобы выполнять команду каждую минуту, задание должно быть такое:
```
* * * * *  cd /root/avito_automation/ && /root/avito_automation/venv/bin/python /root/avito_automation/main.py >/root/avito_automation/cronlog.txt 2>&1
```
- Так же будем обновлять токен раз в 12 часов:
```
0 */12 * * * cd /root/avito_automation/ && /root/avito_automation/venv/bin/python /root/avito_automation/refresh_token.py >/root/avito_automation/cronlog.txt 2>&1
```
### Автор
[Александра Кайдалова](https://t.me/kaydalova)
