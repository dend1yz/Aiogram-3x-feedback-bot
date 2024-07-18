from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import ADMIN_ID, BOT_TOKEN
from database import Database
from kb import user_manage_kb
from aiogram import Bot

bot = Bot(token=BOT_TOKEN)

db = Database()

class AnswerState(StatesGroup):
    waiting_for_message = State()

async def user_info(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        args = message.get_args().split()
        if len(args) != 1:
            await message.answer("Использование: /user <user_id/@username>")
            return

        user_id_or_username = args[0]
        user_info = db.get_user_info(user_id_or_username)
        if user_info:
            user_id, username, is_banned = user_info[1], user_info[2], user_info[3]
            status = "Забанен" if is_banned else "Активен"
            await message.answer(f"UserID: {user_id}\nUsername: {username}\nСтатус: {status}",
                                 reply_markup=user_manage_kb(user_id))
        else:
            await message.answer("Пользователь не найден.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

async def ban_user(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ADMIN_ID:
        user_id = int(callback_query.data.split(":")[1])
        db.ban_user(user_id)
        await callback_query.answer("Пользователь забанен.")
        await callback_query.message.edit_reply_markup(reply_markup=user_manage_kb(user_id))

async def unban_user(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ADMIN_ID:
        user_id = int(callback_query.data.split(":")[1])
        db.unban_user(user_id)
        await callback_query.answer("Пользователь разблокирован.")
        await callback_query.message.edit_reply_markup(reply_markup=user_manage_kb(user_id))

async def ask_for_answer(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.id == ADMIN_ID:
        user_id = int(callback_query.data.split(":")[1])
        await state.update_data(user_id=user_id)
        await callback_query.message.answer("Отправьте сообщение пользователю.")
        await AnswerState.waiting_for_message.set()

async def send_answer(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        user_data = await state.get_data()
        user_id = user_data['user_id']
        await bot.send_message(user_id, message.text)
        await message.answer("Ответ отправлен пользователю.")
        await state.finish()

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(user_info, commands=["user"], state="*")
    dp.register_callback_query_handler(ban_user, Text(startswith="ban:"))
    dp.register_callback_query_handler(unban_user, Text(startswith="unban:"))
    dp.register_callback_query_handler(ask_for_answer, Text(startswith="answer:"))
    dp.register_message_handler(send_answer, state=AnswerState.waiting_for_message)
