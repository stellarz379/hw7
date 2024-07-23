import logging
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import token
from logging import basicConfig, INFO
import requests
import time, aioschedule

bot = Bot(token=token)
dp = Dispatcher()
basicConfig(level=INFO)

monitoring = False
chat_id = None

async def get_btc_price():
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    respones = requests.get(url=url).json()
    price = respones.get('price')
    if price:
        return f"Стоимость биткоина" 
    else:
        return f"Не удалось "