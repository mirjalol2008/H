from aiogram import types, Dispatcher
from database import cursor, conn
from utils.anilist_api import get_anime_info
from utils.localization import get_string

async def add_watch(msg: types.Message):
    user_id = msg.from_user.id
    query = msg.get_args().strip()
    if not query:
        await msg.answer(get_string(user_id, 'addwatch_usage'))
        return
    anime = get_anime_info(query)
    if not anime:
        await msg.answer(get_string(user_id, 'anime_not_found'))
        return
    anime_id = anime['id']
    anime_title = anime['title']
    try:
        cursor.execute("INSERT INTO watchlist (user_id, anime_id, anime_title) VALUES (%s, %s, %s)",
                       (user_id, anime_id, anime_title))
        conn.commit()
        response = get_string(user_id, 'added_watch').replace("{title}", anime_title).replace("{score}", str(anime['score']))
        await msg.answer(response)
    except psycopg2.IntegrityError:
        conn.rollback()
        await msg.answer(get_string(user_id, 'already_in_watchlist'))

async def remove_watch(msg: types.Message):
    user_id = msg.from_user.id
    query = msg.get_args().strip()
    if not query:
        await msg.answer(get_string(user_id, 'removewatch_usage'))
        return
    anime = get_anime_info(query)
    if not anime:
        await msg.answer(get_string(user_id, 'anime_not_found'))
        return
    anime_id = anime['id']
    cursor.execute("DELETE FROM watchlist WHERE user_id=%s AND anime_id=%s", (user_id, anime_id))
    conn.commit()
    await msg.answer(get_string(user_id, 'removed_watch').replace("{title}", anime['title']))

async def list_watch(msg: types.Message):
    user_id = msg.from_user.id
    cursor.execute("SELECT anime_title FROM watchlist WHERE user_id=%s", (user_id,))
    rows = cursor.fetchall()
    if not rows:
        await msg.answer(get_string(user_id, 'watchlist_empty'))
        return
    titles = [row[0] for row in rows]
    text = get_string(user_id, 'watchlist_list') + "\n" + "\n".join(titles)
    await msg.answer(text)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(add_watch, commands=['addwatch'])
    dp.register_message_handler(remove_watch, commands=['removewatch'])
    dp.register_message_handler(list_watch, commands=['watchlist'])
