from dotenv import load_dotenv
from pyrogram import Client, filters
from decouple import config
from pyrogram.types import Message
from utilits import check_and_send_messages, check_command


load_dotenv()
api_id = config('API_ID')
api_hash = config('API_HASH')
phone = config('PHONE')
login = config('LOGIN')

bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)


@bot.on_message(filters.channel)
async def channel_handler(client: Client, message: Message):
    await check_and_send_messages(client, message)

@bot.on_message(filters.reply)
async def reply_handler(client: Client, message: Message):
    await check_and_send_messages(client, message)

@bot.on_message(filters.forwarded)
async def forwarded_handler(client: Client, message: Message):
    await check_and_send_messages(client, message)

@bot.on_message(filters.text)
async def text_handler(client: Client, message: Message):
    await check_command(client, message)

bot.run()
