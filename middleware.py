from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from database import Database

db = Database()

class BanMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        if db.is_user_banned(user_id):
            await message.answer("Вы забанены и не можете отправлять сообщения.")
            return
        return data
