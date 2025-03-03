import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import logging
from datetime import datetime
from .config import API_TOKEN, CHECK_INTERVAL, DB_PATH
from .database import Database

# Инициализация базы данных
db = Database(DB_PATH)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Отправь мне URL сайта для мониторинга.")


@dp.message(Command("stop"))
async def cmd_stop(message: types.Message):
    user_id = message.from_user.id
    db.remove_site(user_id)
    await message.answer("Мониторинг остановлен.")


@dp.message()
async def handle_url(message: types.Message):
    url = message.text.strip()
    if not url.startswith(('http://', 'https://')):
        await message.answer("Пожалуйста, отправьте корректный URL (начинающийся с http:// или https://)")
        return

    user_id = message.from_user.id
    db.add_site(user_id, url)
    await message.answer(f"Начинаю мониторинг сайта: {url}")


async def check_site(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return response.status == 200
        except aiohttp.ClientError as e:
            logging.error(f"Error checking site {url}: {e}")
            return False


async def monitoring_task():
    while True:
        sites = db.get_all_sites()
        for user_id, url in sites:
            is_available = await check_site(url)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            status = "доступен ✅" if is_available else "недоступен ❌"

            await bot.send_message(
                user_id,
                f"Статус сайта {url}\nВремя проверки: {current_time}\nСтатус: {status}"
            )

        await asyncio.sleep(CHECK_INTERVAL)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(monitoring_task())
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
