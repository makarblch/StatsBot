import sqlite3
from aiogram.types import Message
import pandas as pd
import core.graphics.plots as plots
from core.functions.small_func import chat_member_messages, set_timezone
from collections import Counter
import re
from itertools import chain
from core.filters.stopworlds import stopword_txt
from core.functions.small_func import get_stoplist, get_period


async def top_users(message: Message):
    chat_id = message.chat.id
    connection = sqlite3.connect(f'{chat_id}.db')
    cursor = connection.cursor()
    res = await get_period(message)
    cursor.execute(
        'SELECT username, COUNT(*) FROM messages WHERE date_time > ? AND date_time < ? GROUP BY username ORDER BY COUNT(*) DESC',
        (res[0], res[1],))
    results = cursor.fetchall()
    await chat_member_messages(results, message)
    df = pd.DataFrame({
        "User": [i[0] for i in results][:max(10, len(results))],
        "Result": [i[1] for i in results][:max(10, len(results))]
    })
    await plots.bar_chart(df, message)


async def count_users(message: Message):
    chat_id = message.chat.id
    connection = sqlite3.connect(f'{chat_id}.db')
    cursor = connection.cursor()
    res = await get_period(message)
    cursor.execute(
        'SELECT username, COUNT(*) FROM messages WHERE date_time > ? AND date_time < ? GROUP BY username ORDER BY COUNT(*) DESC',
        (res[0], res[1],))
    results = cursor.fetchall()
    return len(results)


async def top_content(message: Message):
    chat_id = message.chat.id
    connection = sqlite3.connect(f'{chat_id}.db')
    cursor = connection.cursor()
    res = await get_period(message)
    cursor.execute(
        'SELECT content, COUNT(*) FROM messages WHERE date_time > ? AND date_time < ? GROUP BY content ORDER BY COUNT(*) DESC',
        (res[0], res[1],))
    results = cursor.fetchall()
    await chat_member_messages(results, message)
    df = pd.DataFrame({
        "Content": [i[0] for i in results],
        "Count": [i[1] for i in results]
    })
    await plots.pie_chart_content(df, message)


async def top_messages(message: Message):
    chat_id = message.chat.id
    connection = sqlite3.connect(f'{chat_id}.db')
    cursor = connection.cursor()
    res = await get_period(message)
    cursor.execute(f'SELECT message FROM messages WHERE date_time > ? AND date_time < ?', (res[0], res[1],))
    stoplist = await get_stoplist(message)
    results = [list(filter(None, re.split(';|,| |-|:|\n', i[0]))) for i in cursor.fetchall()]
    print(results)
    res = list(Counter(i for i in (str(i).lower() for i in list(chain.from_iterable(results))) if
                       i not in stoplist).items())
    res = sorted(res, key=lambda x: x[1], reverse=True)
    print(res)
    df = pd.DataFrame({
        "Message": [i[0] for i in res][:10],
        "Count": [i[1] for i in res][:10]
    })
    await plots.pie_chart(df, message)


async def top_time(message: Message):
    chat_id = message.chat.id
    connection = sqlite3.connect(f'{chat_id}.db')
    cursor = connection.cursor()
    res = await get_period(message)
    cursor.execute(
        'SELECT timezone, COUNT(*) FROM active WHERE date_time > ? AND date_time < ? GROUP BY timezone ORDER BY timezone',
        (res[0], res[1],))
    results = cursor.fetchall()

    res = [[0, 0] for i in range(len(results))]
    for i in range(0, len(results)):
        temp = await set_timezone(results[i][0])
        res[i] = [temp, results[i][1]]

    df = pd.DataFrame({
        "Timezone": [i[0] for i in res],
        "Result": [i[1] for i in res]
    })
    await plots.bar_chart_active(df, message)
