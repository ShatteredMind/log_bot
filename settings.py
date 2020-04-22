from dotenv import load_dotenv

import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")
CHAT_ID = os.getenv("CHAT_ID")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")
