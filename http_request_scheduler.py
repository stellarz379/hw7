import logging
import asyncio
import requests
import schedule
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import API_TOKEN

URL = 'http://example.com' 
INTERVAL = 60

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

logging.basicConfig(filename='http_requests.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def perform_request():
    try:
        response = requests.get(URL)
        response.raise_for_status()  
        result = f"Запрос выполнен успешно, статус: {response.status_code}"
        logging.info(result)
        return result
    except requests.RequestException as e:
        logging.error(f"Произошла ошибка: {e}")
        return f"Произошла ошибка: {e}"

@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer("Привет! Я бот, который выполняет HTTP-запросы каждые 60 секунд.")

async def scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def scheduled_request():
    result = perform_request()
    await bot.send_message(chat_id=1767892428, text=result)

async def main():
    schedule.every(INTERVAL).seconds.do(lambda: asyncio.ensure_future(scheduled_request()))
    asyncio.create_task(scheduler())

    await dp.start_polling(bot)

@dp.message(Command('stop'))
async def stop(message:Message):
    global monitoring
    monitoring = False
    await message.answer("HTTP-запросы остановлены")
    

if __name__ == '__main__':
    asyncio.run(main())