import sqlite3
from aiogram.types import Message
import core.functions.queries as qu
import core.functions.small_func as fu
from core.filters.stopworlds import stopword_txt
import re
import os.path


# База данных для сообщений
async def create_database(chat_id: int):
    # Создаем подключение к базе данных
    connection = sqlite3.connect(f'{chat_id}.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    content TEXT NOT NULL,
    date_time TEXT NOT NULL,
    language_code TEXT,
    is_premium INTEGER,
    is_bot INTEGER
    )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS active (
        message_id INTEGER PRIMARY KEY,
        date_time TEXT NOT NULL,
        timezone INTEGER NOT NULL
        )
        ''')
    connection.commit()


async def create_stoplist(chat_id: int):
    stoplist = [i + '\n' for i in stopword_txt]
    if os.path.exists(f'stoplist-{chat_id}.txt'):
        return
    with open(f'stoplist-{chat_id}.txt', 'w') as file:
        file.writelines(stoplist)


async def create_period(chat_id: int):
    if os.path.isfile(f'period-{chat_id}.txt'):
        return
    with open(f'period-{chat_id}.txt', 'w') as file:
        file.write("1970-01-01 00:00:00;2100-01-01 00:00:00")


async def add_message(chat_id: int, message: Message, content: str):
    # if content == 'text' and message.text.lower() in ['get statistics', 'stop', 'continue', 'users', 'messages',
    #                                                  'stop list', 'add new words', 'remove words', 'content',
    #                                                  'back', '/start']:

    connection = sqlite3.connect(f'{chat_id}.db')
    cursor = connection.cursor()
    add_id = message.message_id
    add_user_id = message.from_user.id
    if content == 'text':
        add_text = message.text
    else:
        add_text = content
    month = message.date.month
    if len(str(month)) == 1:
        month = '0' + str(month)
    day = message.date.day
    if len(str(day)) == 1:
        day = '0' + str(day)
    hour = message.date.hour
    if len(str(hour)) == 1:
        hour = '0' + str(hour)
    minute = message.date.minute
    if len(str(minute)) == 1:
        minute = '0' + str(minute)
    add_date = str(message.date.year) + '-' + str(month) + '-' + str(day) + ' ' + str(
        hour) + ':' + str(minute) + ':' + '00'

    timezone = await fu.get_timezone(str(
        hour) + ':' + str(minute) + ':' + '00')

    if message.from_user.language_code is not None:
        add_language = message.from_user.language_code
    else:
        add_language = 'None'
    if message.from_user.is_premium:
        add_is_premium = 1
    else:
        add_is_premium = 0
    if message.from_user.is_bot:
        add_is_bot = 1
    else:
        add_is_bot = 0

    try:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        add_name = first_name + ' ' + last_name
    except:
        if message.from_user.first_name != '':
            add_name = message.from_user.first_name

    cursor.execute(
        'INSERT INTO messages (message_id, user_id, username, message, content, date_time, language_code, is_premium, is_bot) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (
            add_id, add_user_id,
            add_name,
            add_text,
            content,
            add_date,
            add_language,
            add_is_premium,
            add_is_bot))

    cursor.execute(
        'INSERT INTO active (message_id, date_time, timezone) '
        'VALUES (?, ?, ?)',
        (
            add_id, add_date, timezone))
    connection.commit()
    connection.close()


async def users_statistics(message: Message):
    await qu.top_users(message)


async def messages_statistics(message: Message):
    await qu.top_messages(message)


async def add_to_stop_list(message: Message):
    with open(f'stoplist-{message.chat.id}.txt', 'r') as file:
        stoplist = file.readlines()
        words = re.split(';|,| |-|:|\n', message.text)
        print(words)
        for i in words:
            if i == "":
                continue
            word = i.lower() + '\n'
            if word not in stoplist:
                stoplist.append(word)
                print(f"added: {i.lower()}")
        with open(f'stoplist-{message.chat.id}.txt', 'w') as file:
            file.writelines(stoplist)
        # print(stoplist)


async def remove_from_stop_list(message: Message):
    with open(f'stoplist-{message.chat.id}.txt', 'r') as file:
        stoplist = file.readlines()
        words = re.split(';|,| |-|:|\n', message.text)
        print(words)
        for i in words:
            if i == "":
                continue
            word = i.lower() + '\n'
            if word in stoplist:
                stoplist.remove(word)
                print(f"removed: {i.lower()}")

    with open(f'stoplist-{message.chat.id}.txt', 'w') as file:
        file.writelines(stoplist)
        # print(stoplist)


async def add_start_period(message: Message):
    with open(f'period-{message.chat.id}.txt', 'r') as file:
        dates = file.read().split(';')
        res = await fu.check_date_format(message.text)
    with open(f'period-{message.chat.id}.txt', 'w') as file:
        if res:
            await message.answer("Successfully added!")
            file.write(f"{message.text};{dates[1]}")
        else:
            await message.answer("Failed to add!")


async def add_end_period(message: Message):
    with open(f'period-{message.chat.id}.txt', 'r') as file:
        dates = file.read().split(';')
        res = await fu.check_date_format(message.text)
    with open(f'period-{message.chat.id}.txt', 'w') as file:
        if res:
            await message.answer("Successfully added!")
            file.write(f"{dates[0]};{message.text}")
        else:
            await message.answer("Failed to add!")


async def chat_members(message: Message):
    await fu.chat_members(message)


async def number_chat_members(message: Message):
    await fu.members_number(message)


async def activity_statistics(message: Message):
    await qu.top_time(message)


async def err_statistics(message: Message):
    active = await qu.count_users(message)
    total = await fu.members_number_return(message)
    print(f"active: {active}, total: {total}")
    await message.answer(f"Err for this chat over the given period: {active / total}")


async def content_statistics(message: Message):
    await qu.top_content(message)
