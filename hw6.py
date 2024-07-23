import logging
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import TOKEN, SMTP_USER, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT
bot = Bot(token=TOKEN)
dp = Dispatcher()

conn = sqlite3.connect('emails.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS emails
              (id INTEGER PRIMARY KEY, email TEXT, subject TEXT, message TEXT)''')
conn.commit()


class Form(StatesGroup):
    EMAIL = State()
    SUBJECT = State()
    MESSAGE = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.EMAIL)
    await message.answer("Привет! Пожалуйста, отправьте ваш Gmail адрес")


@dp.message(Form.EMAIL)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Form.SUBJECT)
    await message.answer("Теперь введите тему письма")

@dp.message(Form.SUBJECT)
async def get_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(Form.MESSAGE)
    await message.answer("И наконец, введите ваше сообщение")

@dp.message(Form.MESSAGE)
async def get_message(message: Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    data = await state.get_data()
    
    email = data['email']
    subject = data['subject']
    message_text = data['message_text']

    cursor.execute("INSERT INTO emails (email, subject, message) VALUES (?, ?, ?)", (email, subject, message_text))
    conn.commit()

    try:
        send_email(email, subject, message_text)
        await message.reply("Ваше сообщение успешно отправлено и сохранено в базе данных.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при отправке письма: {str(e)}")

    await state.clear()

def send_email(to_email, subject, message_text):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message_text, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except RuntimeError:
        print("Exit")
    finally:

        conn.close()
