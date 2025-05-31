from aiogram import types, Dispatcher
from utils.localization import get_string

async def stats_cmd(msg: types.Message):
    # Placeholder for admin stats
    await msg.answer("Admin: stats not implemented yet.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(stats_cmd, commands=['stats'])
