from aiogram import types, Dispatcher
from utils.anilist_api import get_anime_info
from utils.localization import get_string

async def search_anime(msg: types.Message):
    user_id = msg.from_user.id
    query = msg.get_args().strip()
    if not query:
        await msg.answer(get_string(user_id, 'search_usage'))
        return
    anime = get_anime_info(query)
    if not anime:
        await msg.answer(get_string(user_id, 'anime_not_found'))
        return
    text = f"<b>{anime['title']}</b>\n"            f"Reyting: {anime['score']}/100\n"            f"Mashhurlik: {anime['popularity']}\n" 
    await msg.answer(text)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(search_anime, commands=['search'])
