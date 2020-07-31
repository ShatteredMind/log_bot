
from dotenv import load_dotenv

import os

load_dotenv()

DATABASE_URI = f'postgresql://{os.getenv("USER")}:' \
               f'{os.getenv("PASSWORD")}@{os.getenv("HOST")}:' \
               f'{os.getenv("PORT")}/{os.getenv("DB_NAME")}'

BOT_TOKEN = os.getenv("BOT_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")
CHAT_ID = os.getenv("CHAT_ID")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")
