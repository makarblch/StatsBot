from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Get statistics'),
        ],
        [
            KeyboardButton(text='Stop list'),
            KeyboardButton(text='Choose period')
        ],
        [
            KeyboardButton(text='Stop'),
            KeyboardButton(text='Continue')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='Choose action'
)

stoplist_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Add new words'),
            KeyboardButton(text='Remove words')
        ],
        [
            KeyboardButton(text='Back'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='Choose action'
)

period_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Add start date'),
            KeyboardButton(text='Add end date')
        ],
        [
            KeyboardButton(text='Back'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='Choose action'
)

stats_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Users'),
            KeyboardButton(text='Messages')
        ],
        [
            KeyboardButton(text='Active time'),
            KeyboardButton(text='Content')
        ],
        [
            KeyboardButton(text='Change number n'),
            KeyboardButton(text='Back')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='Choose statistics',
)

user_stats_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Active users'),
            KeyboardButton(text='Users info json')
        ],
        [
            KeyboardButton(text='Total number'),
            KeyboardButton(text='ERR')
        ],
        [
            KeyboardButton(text='Back'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='Choose users statistics',
)

