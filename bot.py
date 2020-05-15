from telegram.ext import Updater

import time


class LogFileBot(object):

    def __init__(self, token, chat_id, parse_mode, proxy_url):
        self.chat_id = chat_id
        self.parse_mode = parse_mode
        self.updater = Updater(token, use_context=True, request_kwargs={'proxy_url': proxy_url})

    def notify(self, message):
        self.updater.bot.send_message(chat_id=self.chat_id, text=message, parse_mode=self.parse_mode)
