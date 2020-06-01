from src.log_checker import LogChecker
from src.bot import LogFileBot
from settings import *

import asyncio


def main():
    bot = LogFileBot(BOT_TOKEN, CHAT_ID, 'Markdown', PROXY_URL)
    log_checker = LogChecker(LOG_FILE_PATH, bot)
    loop = asyncio.get_event_loop()
    loop.create_task(log_checker.process())
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()
