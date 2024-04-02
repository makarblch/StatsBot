from aiogram.types import Message, InputFile, FSInputFile
import main
from core.pyrogram.methods import get_chat_members
from core.functions.json_parser import serialize
from datetime import datetime


async def chat_members(message: Message):
    chat = await main.bot.get_chat(message.chat.id)
    members = await get_chat_members(chat.id)
    res = serialize(members)
    with open(f'member-{chat.id}.json', 'w', encoding='utf-8') as file:
        file.write(res)
    file = FSInputFile(f'member-{chat.id}.json')
    await main.bot.send_document(chat.id, file)


async def members_number(message: Message):
    chat = await main.bot.get_chat(message.chat.id)
    members = await get_chat_members(chat.id)
    await message.answer(f'Total number of members: {len(members)}')


async def members_number_return(message: Message):
    chat = await main.bot.get_chat(message.chat.id)
    members = await get_chat_members(chat.id)
    return len(members)


async def chat_member_messages(results, message: Message):
    chat = await main.bot.get_chat(message.chat.id)
    with open(f'member-message-{chat.id}.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join([str(i[0]) + ': ' + str(i[1]) for i in results]))
    file = FSInputFile(f'member-message-{chat.id}.txt')
    await main.bot.send_document(chat.id, file)


async def get_stoplist(message: Message):
    with open(f'stoplist-{message.chat.id}.txt', 'r') as file:
        stoplist = list(map(lambda x: x.strip('\n'), file.readlines()))
    return stoplist


async def check_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


async def get_period(message: Message):
    with open(f'period-{message.chat.id}.txt', 'r') as file:
        dates = file.read().strip().split(';')
    # print(dates[0], dates[1])
    return [dates[0], dates[1]]


async def get_timezone(time: str):
    if '00:00:00' <= time < '04:00:00':
        return 0
    elif '04:00:00' <= time < '08:00:00':
        return 1
    elif '08:00:00' <= time < '12:00:00':
        return 2
    elif '12:00:00' <= time < '16:00:00':
        return 3
    elif '16:00:00' <= time < '20:00:00':
        return 4
    else:
        return 5


async def set_timezone(val: int):
    if val == 0:
        return '12 AM - 4 AM'
    elif val == 1:
        return '4 AM - 8 AM'
    elif val == 2:
        return '8 AM - 12 PM'
    elif val == 3:
        return '12 PM - 16 PM'
    elif val == 4:
        return '16 PM - 20 PM'
    else:
        return '20 PM - 12 AM'
