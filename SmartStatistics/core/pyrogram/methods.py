from pyrogram import Client
from core.pyrogram.pyro_settings import api_id, api_hash, bot_token
from core.functions.json_parser import User

app = Client("SmartStatistics", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)


async def get_chat_members(chat_id):
    chat_members = []
    async for member in app.get_chat_members(chat_id):
        if member.user.status is None:
            status = 'None'
        else:
            status = member.user.status.name
        user = User(member.user.first_name, member.user.last_name, status, member.user.is_bot,
                    member.user.is_premium, member.user.language_code)
        chat_members.append(user)
    print(chat_members)
    return chat_members
