import asyncio
import os
from asyncio import sleep
from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.errors import UserDeactivated

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, url_engine


api_id: str = os.getenv("API_ID", "")
api_hash: str = os.getenv("API_HASH", "")
phone_number: str = os.getenv("PHONE_NUMBER", "")

engine = create_engine(url=url_engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create client-user-bot
app = Client(
    "task_test_bot",
    api_id=api_id,
    api_hash=api_hash,
    phone_number=phone_number,
)


@app.on_message(filters=filters.private)
async def handle_message(client, message) -> None:
    """Обработчик событий на получение сообщения."""
    user_id: str = str(message.from_user.id)
    # На всякий случай проверим что это не мы пишем сами себе
    if user_id != (await client.get_me()).id:
        users_with_status = (
            session.query(User)
            .filter_by(user_id=user_id)
            .order_by(User.id.desc())
            .first()
        )
        if users_with_status:
            # Если пользователь есть в БД
            text_low = message.text.lower()
            count_msg = users_with_status.count_msg
            if "прекрасно" in text_low or "ожидать" in text_low:
                # Если были найдены, то вся воронка прекращается.
                user = session.query(User).filter_by(user_id=user_id).first()
                user.status = "finished"
                user.status_updated_at = datetime.now()
                user.stop_word = True
                session.commit()
            elif "триггер1" in text_low and count_msg == 2:
                # Если мы вводим "триггер1" после первого сообщения,
                # но до того момента как придет второе сообщение, то пропустим
                # второе сообщение и начнем ждать сразу третье сообщение.
                await step_3(user_id)
        else:
            # Если пользователя нет в БД
            await step_1(user_id)
    return


async def step_1(user_id: str) -> None:
    """Шаг первый. Производим запись в БД т.к. пользователь новый.
    Через 6 минут отправляем сообщение, если не было стоп слова."""
    next_time_msg = (
        # datetime.now() + timedelta(minutes=6)
        datetime.now()
        + timedelta(minutes=1)
    ).replace(second=0, microsecond=0)
    new_user = User(
        user_id=user_id,
        next_time_msg=next_time_msg,
        count_msg=1,
    )
    session.add(new_user)
    session.commit()


async def step_2(user_id: str) -> None:
    """Шаг второй. Обновляем время статуса в БД, через 39 минут
    отправляем сообщение, если не было стоп слова или не введен 'триггер1'"""
    next_time_msg = (
        # datetime.now() + timedelta(minutes=39)
        datetime.now()
        + timedelta(minutes=5)
    ).replace(second=0, microsecond=0)
    user = session.query(User).filter_by(user_id=user_id).first()
    user.status_updated_at = datetime.now()
    user.next_time_msg = next_time_msg
    user.count_msg = 2
    session.commit()


async def step_3(user_id: str) -> None:
    """Шаг второй. Обновляем время статуса в БД, через 1 день 2 часа
    отправляем сообщение, если не было стоп слова."""
    next_time_msg = (
        # datetime.now() + timedelta(days=1, hours=2)
        datetime.now()
        + timedelta(minutes=1)
    ).replace(second=0, microsecond=0)
    user = session.query(User).filter_by(user_id=user_id).first()
    user.status = "finished"
    user.status_updated_at = datetime.now()
    user.next_time_msg = next_time_msg
    user.count_msg = 3
    session.commit()


async def check_status() -> None:
    """Функция которая зациклена в "while True".
    Проверяет время для отправки нужных сообщений"""
    await sleep(5)
    while True:
        date_time = datetime.now().replace(second=0, microsecond=0)
        select_query = (
            session.query(User)
            .filter(
                (~User.stop_word)
                & (~User.send_msg)
                & (User.next_time_msg == date_time)
                & (User.status != "dead")
            )
            .all()
        )
        if select_query:
            for user in select_query:
                try:
                    if user.count_msg == 1:
                        await app.send_message(
                            chat_id=user.user_id, text="Текст1"
                        )
                        await step_2(user.user_id)
                    elif user.count_msg == 2:
                        await app.send_message(
                            chat_id=user.user_id, text="Текст2"
                        )
                        await step_3(user.user_id)
                    elif user.count_msg == 3:
                        await app.send_message(
                            chat_id=user.user_id, text="Текст3"
                        )
                        user_update = (
                            session.query(User)
                            .filter_by(user_id=user.user_id)
                            .first()
                        )
                        user_update.status = "finished"
                        user_update.status_updated_at = datetime.now()
                        user_update.send_msg = True
                        user_update.count_msg = 4
                        session.commit()

                except UserDeactivated:
                    user_update = (
                        session.query(User)
                        .filter_by(user_id=user.user_id)
                        .first()
                    )
                    user_update.status = "dead"
                    user_update.status_updated_at = datetime.now()
                    session.commit()
        await sleep(10)


if __name__ == "__main__":
    asyncio.gather(check_status())
    app.run()
