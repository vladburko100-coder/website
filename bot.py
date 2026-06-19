import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN-BOT')
CHAT_ID = os.getenv('CHAT-ID')
bot = Bot(token=TOKEN)

router = Router()


@router.message(Command('start'))
async def handle_message(message: types.Message):
    await message.answer("Привет! Я бот, который получает запросы на записи по маникюру!")


async def send_application(phone: str, name: str, fullname: str):
    message_text = f"🆕 **Новая запись на маникюр!**\n\n"
    message_text += f"👤 **Имя:** {name}\n"
    message_text += f"👥 **Фамилия:** {fullname}\n"
    message_text += f"📞 **Телефон:** {phone}\n"

    await bot.send_message(chat_id=CHAT_ID, text=message_text, parse_mode="Markdown")


async def main():
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
