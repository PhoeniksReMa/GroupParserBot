from pyrogram import Client, filters
from decouple import config
from pyrogram.types import Message
import re


api_id = config('API_ID')
api_hash = config('API_HASH')
phone = config('PHONE')
login = config('LOGIN')
chat_id = 432475414

bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)



@bot.on_message(filters.text)
async def echo_handler(client: Client, message: Message):
    with open("keys.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    words = [word.strip() for word in content.split(",") if word.strip()]
    pattern = re.compile(r'(' + r'|'.join(words) + r')', flags=re.IGNORECASE)

    if message.chat.id == chat_id:

        if message.text == 'Ключи':
            print(f'Текущий список ключей: {words}')
            await client.send_message(chat_id=chat_id, text=f'Текущий список ключей: {words}')

        if re.compile(r"^Изменить:", flags=re.IGNORECASE).search(message.text):
            parts = message.text.split(":", 1)
            after_colon = parts[1].strip()

            with open("keys.txt", "w", encoding="utf-8") as f:
                f.write(after_colon)

            print(f'Ключи изменены. Новый список: {after_colon}')
            await client.send_message(chat_id=chat_id, text=f'Ключи изменены. Новый список: {after_colon}')

        if re.compile(r"^Добавить:", flags=re.IGNORECASE).search(message.text):
            parts = message.text.split(":", 1)
            after_colon = parts[1].strip()
            new_words = content + ', ' + after_colon
            with open("keys.txt", "w", encoding="utf-8") as f:
                f.write(new_words)
            print(f'Ключи изменены. Новый список: {new_words}')
            await client.send_message(chat_id=chat_id, text=f'Ключи изменены. Новый список: {new_words}')

    if pattern.search(message.text):
        await client.forward_messages(chat_id=chat_id, from_chat_id=message.chat.id, message_ids=message.id)



bot.run()