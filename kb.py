from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def user_manage_kb(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    ban_button = InlineKeyboardButton(text="Бан", callback_data=f"ban:{user_id}")
    unban_button = InlineKeyboardButton(text="Разбан", callback_data=f"unban:{user_id}")
    answer_button = InlineKeyboardButton(text="Ответить", callback_data=f"answer:{user_id}")
    keyboard.add(ban_button, unban_button, answer_button)
    return keyboard
