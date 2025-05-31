from aiogram import types, Dispatcher
from database import cursor, conn
from utils.localization import get_string
import json, os

# Load supported languages from data/languages.json
with open(os.path.join('data', 'languages.json'), 'r', encoding='utf-8') as f:
    LANGUAGES = json.load(f)

from config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT
import psycopg2

def register_handlers(dp, lang_manager=None):
    @dp.message_handler(commands=['language'])
    async def language_cmd(msg: types.Message):
        user_id = msg.from_user.id
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        buttons = []
        for code in LANGUAGES.keys():
            buttons.append(types.InlineKeyboardButton(code.upper(), callback_data=f"lang_{code}"))
        keyboard.add(*buttons)
        await msg.answer(get_string(user_id, 'choose_language'), reply_markup=keyboard)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('lang_'))
    async def change_language(call: types.CallbackQuery):
        user_id = call.from_user.id
        lang_code = call.data.split('_', 1)[1]
        cursor.execute("UPDATE users SET language_code=%s WHERE id=%s", (lang_code, user_id))
        conn.commit()
        await call.answer(get_string(user_id, 'language_changed').replace("{lang}", lang_code.upper()))
        await call.message.edit_text(get_string(user_id, 'welcome').replace("{name}", call.from_user.first_name))

def get_user_language(user_id):
    cursor.execute("SELECT language_code FROM users WHERE id=%s", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else 'en'
