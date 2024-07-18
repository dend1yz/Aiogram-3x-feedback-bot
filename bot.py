from aiogram import types, Dispatcher, Bot
from aiogram.types import ParseMode
from config import ADMIN_ID, GREETING_TEXT, GREETING_IMAGE_URL, BOT_TOKEN
from database import Database
from middleware import BanMiddleware
from admin import register_admin_handlers

bot = Bot(token=BOT_TOKEN)

db = Database()

dp = Dispatcher(bot)

dp.middleware.setup(BanMiddleware())

async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    db.add_user(user_id, username)

    await message.answer_photo(photo=GREETING_IMAGE_URL, caption=GREETING_TEXT, parse_mode=ParseMode.HTML)

async def message_handler(message: types.Message):
    if message.from_user.id == ADMIN_ID and message.text.startswith('/'):
        return

    await message.forward(ADMIN_ID)
    user_info = f"@{message.from_user.username}" if message.from_user.username else f"UserID: {message.from_user.id}"
    await bot.send_message(ADMIN_ID, f"Сообщение от {user_info}")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(message_handler, content_types=types.ContentType.ANY)
    register_admin_handlers(dp)
