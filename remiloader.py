from math import exp
import asyncio
import os
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

def download_video(url: str) -> str:
    filename = "downloaded_video.mp4"
    options = {
        "format": "best[ext=mp4]/best",
        "outtmpl": filename,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [],
        "proxy": "http://127.0.0.1:10809",
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return filename

@dp.message(CommandStart())
async def start_command(message:types.Message):
    await message.answer("Привет! Отправь мне ссылку, и я скачаю ее содержимое! 🌸")

@dp.message(F.text.startswith("http"))
async def download(message:types.Message):
    url = message.text.strip()
    status_msg = await message.answer("Скачиваю...💫")

    try:
        file_path = await asyncio.to_thread(download_video, url)
        await bot.send_video(message.from_user.id, FSInputFile(file_path),caption="Твое видео: ")

        os.remove(file_path)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"Произошла ошибка: {str(e)}")

async def main():
    print("started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())