from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.utils import executor
from config import BOT_TOKEN
from bot import register_handlers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

register_handlers(dp)

async def on_startup(dp):
    await bot.set_my_commands([
        BotCommand("start", "Запустить бота"),
        BotCommand("user", "Управление пользователями")
    ])

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
