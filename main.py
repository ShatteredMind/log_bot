from log_checker import LogChecker
from bot import LogFileBot
from settings import *

import time


def main():
    bot = LogFileBot(BOT_TOKEN, CHAT_ID, PROXY_URL)
    log_checker = LogChecker(LOG_FILE_PATH)
    while True:
        message = log_checker.process()
        if message:
            bot.notify(message)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
