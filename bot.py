import logging
import yt_dlp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import os
import uuid
from aiogram.types.input_file import FSInputFile

TOKEN = "7552419100:AAEih_b7hX4hHoNv_f1iAP-IAoIIOKJTmGE"

async def main():
    bot = Bot(token=TOKEN)
    
    dp = Dispatcher()

    logging.basicConfig(level=logging.INFO)

    @dp.message(Command("start"))
    async def start_command(message: Message):
        await message.reply("Give ne link, I will get video for you")

    @dp.message(Command("vid"))
    async def download_video(message: Message):

        args = message.text.split()
        
        if len(args) < 2:
            logging.warning("Send link ffs")
            await message.reply("❌FORMAT: /vid LINK")
            return

        url = args[1]

        try:
            unique_filename = f"video_{uuid.uuid4().hex}.mp4"

            ydl_opts = {
                'format': 'best[ext=mp4]',
                'outtmpl': unique_filename,
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            video_file = FSInputFile(unique_filename)
            await message.reply_video(video_file)

            os.remove(unique_filename)

        except Exception as e:
            await message.reply(f"❌ Error: {e}")

    logging.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    