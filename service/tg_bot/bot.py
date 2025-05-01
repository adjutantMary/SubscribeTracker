import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, ContactFilter
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from db import engine, User  # Ваша модель SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=os.getenv("TG_BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

SessionLocal = sessionmaker(bind=engine)


@router.message(CommandStart())
async def cmd_start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить телефон", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await message.answer("Пожалуйста, отправьте свой номер телефона:", reply_markup=kb)


@router.message(F.contact)
async def handle_contact(message: Message):
    session = SessionLocal()
    phone = message.contact.phone_number if message.contact else None

    if not phone:
        await message.answer("Не удалось получить номер телефона.")
        return

    user = session.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if not user:
        await message.answer("Пользователь с таким телефоном не найден.")
        session.close()
        return

    user.telegram_id = message.from_user.id
    session.commit()
    session.close()

    await message.answer("✅ Вы успешно зарегистрированы!", reply_markup=None)


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
