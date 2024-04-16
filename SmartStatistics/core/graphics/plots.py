import matplotlib.pyplot as plt
from aiogram.types import Message
from PIL import Image
from aiogram.types.input_file import FSInputFile
from aiogram import types
from io import BytesIO
import telegram as tg
from telegram.ext import Updater, CommandHandler
import numpy as np
import main
import io
import aiofiles


async def bar_chart(df, message: Message):
    plt.figure(figsize=(10, 10))
    plt.bar(df["User"], df["Result"])
    plt.title('Most popular users')
    plt.xlabel('Users')
    plt.ylabel('Number of messages')
    plt.savefig(f'graph{message.chat.id}.jpg')
    # plt.show()
    photo = FSInputFile(rf'graph{message.chat.id}.jpg')
    await main.bot.send_photo(chat_id=message.chat.id, photo=photo)


async def bar_chart_active(df, message: Message):
    plt.figure(figsize=(10, 10))
    plt.bar(df["Timezone"], df["Result"])
    plt.title('Most popular time')
    plt.xlabel('Timezone')
    plt.ylabel('Number of messages')
    plt.savefig(f'graph-time-{message.chat.id}.jpg')
    # plt.show()
    photo = FSInputFile(f'graph-time-{message.chat.id}.jpg')
    await main.bot.send_photo(chat_id=message.chat.id, photo=photo)


async def pie_chart(df, message: Message):
    plt.figure(figsize=(10, 10))
    plt.pie(df['Count'], labels=df['Message'], autopct='%1.1f%%')
    plt.title('Most popular messages')
    plt.savefig(f'graph{message.chat.id}.jpg')
    # plt.show()
    photo = FSInputFile(rf'graph{message.chat.id}.jpg')
    await main.bot.send_photo(chat_id=message.chat.id, photo=photo)


async def pie_chart_content(df, message: Message):
    plt.figure(figsize=(10, 10))
    plt.pie(df['Count'], labels=df['Content'], autopct='%1.1f%%')
    plt.title('Most popular content types')
    plt.savefig(f'graph-content-{message.chat.id}.jpg')
    # plt.show()
    photo = FSInputFile(f'graph-content-{message.chat.id}.jpg')
    await main.bot.send_photo(chat_id=message.chat.id, photo=photo)