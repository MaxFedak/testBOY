import logging
import asyncio
import uuid
import os
import yt_dlp
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile

TOKEN = "7552419100:AAEih_b7hX4hHoNv_f1iAP-IAoIIOKJTmGE"
WEBHOOK_URL = f"https://bot-video-a18f1b52dae7.herokuapp.com:443/webhook"
PORT = 443

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Give me a link, I will get video for you.")

@dp.message(Command("vid"))
async def download_video(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        logging.warning("No link provided.")
        await message.reply("❌ FORMAT: /vid LINK")
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

async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    logging.info("Webhook deleted")
    await bot.session.close()

def register_webhook(app: web.Application):
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)

async def main():
    app = web.Application()
    register_webhook(app)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    logging.info(f"Starting server on port {PORT}...")
    await site.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
