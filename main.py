import os

from pyrogram import Client

api_id = os.getenv("API_ID", "")
api_hash = os.getenv("API_HASH", "")
bot_token = os.getenv("TOKEN", "")

app = Client(
    "test_task_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token
)


@app.on_message()
async def hello(client, message) -> None:
    await message.reply("Привет, я бот!")
    return

app.run()
