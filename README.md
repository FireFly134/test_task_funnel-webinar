# test_task_funnel-webinar

пример `.env` файла, который должен лежать рядом с `Dockerfile`:
```commandline
API_ID=...
API_HASH=...
PHONE_NUMBER="Номер телефона аккаунта телеграм"

# POSTGRES
POSTGRES_DB=Название базы данных
POSTGRES_USER=Имя пользователя БД
POSTGRES_PASSWORD=Пароль пользователя от БД
```

Как получить API_ID и API_HASH? Все просто, проходим по ссылке [my.telegram.org](https://my.telegram.org/).  
Все официально, вводим номер телефона от аккаунта, вводим код подтверждения. 
Код подтверждения приходит на этот аккаунт от телеграм.
После того как прошли авторизацию, заходим [в приложения](https://my.telegram.org/apps),
если приложения нет, то предложит создать.  
После создания будет доступен API_ID и API_HASH и еще дополнительная информация.

### Теперь самое основное, запуск user_bot.  
Тут в принципе всё просто!  
Если у нет докера, установите его... ;)

Открываем консоль, если у вас linux, то проверьте что докер запущен:
`sudo systemctl status docker`, 
если выключен вводи команду:
`sudo systemctl start docker`

На ОС Window проще, запусти программу docker и все.


И после этого, через консоль, проходим в папку с проектом `cd ./путь до проекта/test_task_funnel-webinar/`  
отлично, осталось совсем чуть-чуть.
Вводим команду `sudo docker compose up`  
- если вводим первый раз, то нужно создать образ докера, просто добавь к этой команде `--build`  
- если хочешь чтобы докер запустил проект в режиме демона, добавь еще `-d`

Всё, мы наигрались пора выключать. 
Вводим команду `sudo docker compose down`
P.S.: Если вдруг выдает ошибку из-за того что нет "compose", попробуй `docker-compose`  
P.S.s.: Если ты работаешь на Window и у тебя выдает ошибку "команды `sudo` не существует", просто не используй в команде `sudo` ;)