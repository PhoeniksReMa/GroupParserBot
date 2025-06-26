import os
import logging
import colorlog
from dotenv import load_dotenv
import re

load_dotenv()
chat_id = os.getenv('CHAT_ID')

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))

logger = colorlog.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

async def check_and_send_messages(client, message):
    with open("keys.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    words = [word.strip() for word in content.split(",") if word.strip()]
    pattern = re.compile(r'\b(?:' + '|'.join(words) + r')\w*\b', flags=re.IGNORECASE)

    if message.text is not None:
        logging.info(f'\nПроверка:\n```\n{message.text}\n```\n\n{pattern}\n\n{pattern.search(message.text)}\n')
        if pattern.search(message.text):
            await client.forward_messages(chat_id=chat_id, from_chat_id=message.chat.id, message_ids=message.id)

    elif message.caption is not None:
        logging.info(f'\nПроверка:\n```\n{message.caption}\n```\n\n{pattern}\n\n{pattern.search(message.caption)}\n')
        if pattern.search(message.caption):
            await client.forward_messages(chat_id=chat_id, from_chat_id=message.chat.id, message_ids=message.id)

    elif message.text is None or message.caption is None:
        logging.error(f'\nНе получилось получить текст! {message}\n')

async def check_command(client, message):
    with open("keys.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    words = [word.strip() for word in content.split(",") if word.strip()]

    if message.chat.id == int(chat_id):
        if message.text == 'Ключи':
            logging.info(f'Текущий список ключей: {words}')
            await client.send_message(chat_id=chat_id, text=f'Текущий список ключей: {words}')

        elif re.compile(r"^Изменить:", flags=re.IGNORECASE).search(message.text):
            parts = message.text.split(":", 1)
            after_colon = parts[1].strip()

            with open("keys.txt", "w", encoding="utf-8") as f:
                f.write(after_colon)

            logging.info(f'Ключи изменены. Новый список: {after_colon}')
            await client.send_message(chat_id=chat_id, text=f'Ключи изменены. Новый список: {after_colon}')

        elif re.compile(r"^Добавить:", flags=re.IGNORECASE).search(message.text):
            parts = message.text.split(":", 1)
            after_colon = parts[1].strip()
            new_words = content + ', ' + after_colon
            with open("keys.txt", "w", encoding="utf-8") as f:
                f.write(new_words)
            logging.info(f'Ключи изменены. Новый список: {new_words}')
            await client.send_message(chat_id=chat_id, text=f'Ключи изменены. Новый список: {new_words}')