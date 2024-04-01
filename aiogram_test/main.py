from aiogram import Bot, Dispatcher, types
from aiogram.methods import SendMessage
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
import logging
import core.keyboards.basic as basic
import core.functions.func as func
from core.settings import settings, flag
from aiogram import F
from aiogram.filters import Command, CommandStart
from core.pyrogram.methods import app
import os.path

# Creating bot, dispatcher and logger
bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")
dp = Dispatcher()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - [%(levelname)s] - %(name)s'
                           '(%(filename)s.%(funcName)s(%(lineno)d) - %(message)s')


class States(StatesGroup):
    waiting_for_button_click = State()
    waiting_for_first_message_add = State()
    waiting_for_first_message_remove = State()
    waiting_for_start_date = State()
    waiting_for_end_date = State()
    waiting_for_continue = State()


@dp.message(F.content_type.in_({ContentType.NEW_CHAT_MEMBERS}))
async def meeting(message: Message):
    await message.answer(text="Hello everyone! Press /start to start using me")


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(text=f'Hello, {message.from_user.first_name}!', reply_markup=basic.main_kb)
    await func.create_stoplist(message.chat.id)
    await func.create_period(message.chat.id)
    await func.create_database(message.chat.id)
    await state.set_state(States.waiting_for_button_click)


@dp.message(F.text.lower() == 'stop')
async def stop_bot(message: Message, state: FSMContext):
    await message.answer("Bot stopped collecting messages until continue pushed")
    await state.set_state(States.waiting_for_continue)


@dp.message(F.text.lower() == 'continue')
async def continue_bot(message: Message, state: FSMContext):
    await message.answer("Bot continued collecting messages")
    await state.set_state(States.waiting_for_button_click)


@dp.message(States.waiting_for_continue)
async def waiting(message: Message):
    await message.answer("Bot doesn't work right now")


@dp.message(F.text.lower() == 'get statistics')
async def statistics_bot(message: Message):
    await message.answer(text=f'Please, choose: ', reply_markup=basic.stats_kb)


@dp.message(F.text.lower() == 'stop list')
async def stop_list_bot(message: Message):
    await message.answer(text=f'Please, choose: ', reply_markup=basic.stoplist_kb)


@dp.message(F.text.lower() == 'add new words')
async def add_new_words(message: Message, state: FSMContext):
    await message.answer("Please, input words using commas as separator")
    await state.set_state(States.waiting_for_first_message_add)


@dp.message(F.text.lower() == 'remove words')
async def remove_words(message: Message, state: FSMContext):
    await message.answer("Please, input words using commas as separator")
    await state.set_state(States.waiting_for_first_message_remove)


@dp.message(States.waiting_for_first_message_add)
async def add_to_stop_list(message: Message, state: FSMContext):
    await func.add_to_stop_list(message)
    await message.answer("Successfully added!")
    await state.set_state(States.waiting_for_button_click)


@dp.message(States.waiting_for_first_message_remove)
async def remove_from_stop_list(message: Message, state: FSMContext):
    await func.remove_from_stop_list(message)
    await message.answer("Successfully removed!")
    await state.set_state(States.waiting_for_button_click)


@dp.message(F.text.lower() == 'choose period')
async def period_bot(message: Message):
    await message.answer(text=f'Please, choose: ', reply_markup=basic.period_kb)


@dp.message(F.text.lower() == 'add start date')
async def add_start_bot(message: Message, state: FSMContext):
    await message.answer("Please, input date in yy-mm-dd hh:mm:ss format")
    await state.set_state(States.waiting_for_start_date)


@dp.message(States.waiting_for_start_date)
async def add_start_date(message: Message, state: FSMContext):
    await func.add_start_period(message)
    await state.set_state(States.waiting_for_button_click)


@dp.message(F.text.lower() == 'add end date')
async def add_stop_bot(message: Message, state: FSMContext):
    await message.answer("Please, input date in yy-mm-dd hh:mm:ss format")
    await state.set_state(States.waiting_for_start_date)


@dp.message(States.waiting_for_end_date)
async def add_end_date(message: Message, state: FSMContext):
    await func.add_end_period(message)
    await state.set_state(States.waiting_for_button_click)


@dp.message(F.text.lower() == 'users')
async def user_statistics_bot(message: Message):
    await message.answer(text=f'Please, choose: ', reply_markup=basic.user_stats_kb)


@dp.message(F.text.lower() == 'active users')
async def messages_bot_active(message: Message):
    await func.users_statistics(message)


@dp.message(F.text.lower() == 'users info json')
async def messages_bot_users(message: Message):
    await func.chat_members(message)


@dp.message(F.text.lower() == 'total number')
async def messages_bot_total(message: Message):
    await func.number_chat_members(message)


@dp.message(F.text.lower() == 'messages')
async def messages_bot(message: Message):
    await func.messages_statistics(message)


@dp.message(F.text.lower() == 'err')
async def messages_bot_err(message: Message):
    await func.err_statistics(message)


@dp.message(F.text.lower() == 'active time')
async def messages_bot_time(message: Message):
    await func.activity_statistics(message)


@dp.message(F.text.lower() == 'content')
async def messages_bot_content(message: Message):
    await func.content_statistics(message)


@dp.message(F.text.lower() == 'back')
async def back(message: Message):
    await message.answer(text='let\'s return to the previous keyboard!', reply_markup=basic.main_kb)


@dp.message(F.photo)
async def get_picture(message: Message):
    if os.path.isfile(f'{message.chat.id}.db'):
        await func.add_message(message.chat.id, message, 'photo')
    else:
        await func.create_database(message.chat.id)


@dp.message(F.content_type.in_({'sticker'}))
async def get_sticker(message: Message):
    if os.path.isfile(f'{message.chat.id}.db'):
        await func.add_message(message.chat.id, message, 'sticker')
    else:
        await func.create_database(message.chat.id)


@dp.message(F.content_type.in_({'video'}))
async def get_sticker(message: Message):
    if os.path.isfile(f'{message.chat.id}.db'):
        await func.add_message(message.chat.id, message, 'video')
    else:
        await func.create_database(message.chat.id)


@dp.message(F.voice)
async def get_voice(message: Message):
    if os.path.isfile(f'{message.chat.id}.db'):
        await func.add_message(message.chat.id, message, 'voice')
    else:
        await func.create_database(message.chat.id)


@dp.message(F.location)
async def get_location(message: Message):
    if os.path.isfile(f'{message.chat.id}.db'):
        await func.add_message(message.chat.id, message, 'location')
    else:
        await func.create_database(message.chat.id)


@dp.message(F.document)
async def get_document(message: Message):
    if os.path.isfile(f'{message.chat.id}.db'):
        await func.add_message(message.chat.id, message, 'document')
    else:
        await func.create_database(message.chat.id)


@dp.message(F.audio)
async def get_audio(message: Message):
    if os.path.isfile(f'{message.chat.id}.db'):
        await func.add_message(message.chat.id, message, 'audio')
    else:
        await func.create_database(message.chat.id)


@dp.message(F.camera)
async def get_audio(message: Message):
    if os.path.isfile(f'{message.chat.id}.db'):
        await func.add_message(message.chat.id, message, 'camera')
    else:
        await func.create_database(message.chat.id)


@dp.message()
async def echo(message: Message):
    if os.path.isfile(f'{message.chat.id}.db'):
        try:
            text = message.text
            await func.add_message(message.chat.id, message, 'text')
        except:
            pass
    else:
        await func.create_database(message.chat.id)


async def main():
    # To avoid multiple repetitions
    await bot.delete_webhook(drop_pending_updates=True)
    await app.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
