import asyncio
from os import environ
from pyrogram import Client, filters, idle
from pyrogram.types import Message 
from typing import Any
from dotenv import load_dotenv
load_dotenv()

loop = asyncio.get_event_loop()

# Get Values from .env file
class Var(object):
    API_ID=int(environ.get('API_ID'))
    API_HASH=str(environ.get('API_HASH'))
    BOT_TOKEN=str(environ.get('BOT_TOKEN'))

Bot=Client('my_account', Var.API_ID, Var.API_HASH, bot_token=Var.BOT_TOKEN)

@Bot.on_message(
    filters.private &
    (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ))
async def download_handler(client: Client, message: Message):
    print('message received')
    media=get_media_from_message(message)
    with open(str(getattr(media, "file_name", "None")), "wb") as file:
        async for chunk in client.stream_media(message=media, limit=2):
            file.write(chunk)
    print('Done')


# Code was Taken from EverythingSuckz's file_properties.py file
# https://github.com/EverythingSuckz/TG-FileStreamBot/blob/main/WebStreamer/utils/file_properties.py
def get_media_from_message(message: "Message") -> Any:
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    )
    for attr in media_types:
        media = getattr(message, attr, None)
        if media:
            return media

async def main():
    await Bot.start()
    print('Bot Started')
    await idle()

loop.run_until_complete(main())
