import os

from pyrogram import Client, filters

app = Client("test_task_bot", bot_token=os.getenv("TOKEN", ""))


@app.on_message(filters.private)
async def hello(client, message) -> None:
    await message.reply("Hello from Pyrogram!")
    return


app.run()
