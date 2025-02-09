import logging
import yt_dlp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import os
import uuid
from aiogram.types.input_file import FSInputFile

# Встановлюємо токен (заміни на свій)
TOKEN = "7552419100:AAEih_b7hX4hHoNv_f1iAP-IAoIIOKJTmGE"

# Створюємо асинхронну функцію для ініціалізації бота та сесії
async def main():
    # Створюємо об'єкти бота
    bot = Bot(token=TOKEN)
    
    # Створюємо диспетчер
    dp = Dispatcher()

    # Налаштовуємо логування
    logging.basicConfig(level=logging.INFO)

    # Логування старту бота
    @dp.message(Command("start"))
    async def start_command(message: Message):
        logging.info(f"Команда /start отримана від {message.from_user.username}")
        await message.reply("Привіт! Я бот, який допоможе скачати відео.")

    # Обробка команди /vid
    @dp.message(Command("vid"))
    async def download_video(message: Message):
        logging.info(f"Команда /vid отримана від {message.from_user.username}")

        args = message.text.split()
        
        if len(args) < 2:
            logging.warning("Не було надіслано посилання.")
            await message.reply("❌ Надішли посилання після команди /vid")
            return

        url = args[1]
        logging.info(f"Обробка посилання: {url}")

        try:
            # Генеруємо унікальне ім'я для відео
            unique_filename = f"video_{uuid.uuid4().hex}.mp4"

            # Налаштування yt-dlp
            ydl_opts = {
                'format': 'best[ext=mp4]',
                'outtmpl': unique_filename,
                'quiet': True
            }

            # Завантаження відео
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            logging.info(f"Завантаження завершено. Відправка відео ({unique_filename})...")

            # Використовуємо FSInputFile для файлу на диску
            video_file = FSInputFile(unique_filename)
            await message.reply_video(video_file)

            # Видаляємо файл після відправки
            os.remove(unique_filename)

        except Exception as e:
            logging.error(f"Помилка при обробці: {e}")
            await message.reply(f"❌ Помилка: {e}")

    # Запуск бота
    logging.info("Бот запущений...")
    await dp.start_polling(bot)

# Запуск асинхронної функції
if __name__ == "__main__":
    asyncio.run(main())
    