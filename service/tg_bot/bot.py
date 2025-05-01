import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from db import engine, User  # User — SQLAlchemy-модель CustomUser
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TG_BOT_TOKEN"))
dp = Dispatcher(bot)

SessionLocal = sessionmaker(bind=engine)

@dp.message_handler(commands=['start'])
async def start(message: Message):
    session = SessionLocal()
    phone = message.contact.phone_number if message.contact else None

    if not phone:
        await message.reply("Пожалуйста, отправьте свой номер телефона через кнопку")
        return

    user = session.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if not user:
        await message.reply("Пользователь с таким телефоном не найден.")
        return

    user.telegram_id = message.from_user.id
    session.commit()
    session.close()

    await message.reply("Вы успешно зарегистрированы в системе!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
