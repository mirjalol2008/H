from aiogram import types, Dispatcher
from database import cursor, conn
from utils.localization import get_string

async def feedback_cmd(msg: types.Message):
    user_id = msg.from_user.id
    text = msg.get_args().strip()
    if not text:
        await msg.answer(get_string(user_id, 'feedback_usage'))
        return
    cursor.execute("INSERT INTO feedback (user_id, message) VALUES (%s, %s)", (user_id, text))
    conn.commit()
    await msg.answer(get_string(user_id, 'feedback_thanks'))

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(feedback_cmd, commands=['feedback'])
