from aiogram import types, Dispatcher
from database import cursor, conn
from utils.localization import get_string, set_user_language
from database import create_tables

async def start_cmd(msg: types.Message):
    user = msg.from_user
    cursor.execute("INSERT INTO users (id, first_name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;", (user.id, user.first_name))
    conn.commit()
    text = get_string(user.id, 'welcome').replace("{name}", user.first_name)
    await msg.answer(text)

async def help_cmd(msg: types.Message):
    user = msg.from_user
    text = get_string(user.id, 'help')
    await msg.answer(text)

async def about_cmd(msg: types.Message):
    text = "<b>GenAniBot</b> - barcha anime ma'lumotlari bitta botda! Dasturchi: mirjalol2008"
    await msg.answer(text)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])
    dp.register_message_handler(help_cmd, commands=['help'])
    dp.register_message_handler(about_cmd, commands=['about'])
