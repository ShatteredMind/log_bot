from datetime import datetime, timedelta
from typing import Optional, Iterator

from utils import line_contains_date
from db import session_scope
from models import LogEntry
from bot import LogFileBot

import asyncio


class LogChecker(object):

    def __init__(self,
                 file_name: str,
                 bot: LogFileBot,
                 timeout: float = 0.5,
                 resend_timeout: int = 60,
                 get_traceback: bool = True,
                 search_string: Optional[str] = None) -> None:
        self.bot = bot
        self.timeout = timeout
        self.message_lines = []
        self.file_name = file_name
        self.get_traceback = get_traceback
        self.search_string = search_string
        self.resend_timeout = resend_timeout

    def __repr__(self) -> str:
        return f"Chat ID: {self.bot.chat_id}. Search String: {self.search_string}"

    async def process(self) -> None:
        file = open(self.file_name)
        new_messages = self.follow(file, self.append_line())
        async for message in new_messages:
            self.bot.notify(message)
            self.message_lines.clear()

    def append_line(self) -> None:
        while True:
            line = (yield)
            self.message_lines.append(line)

    def traceback_was_added(self) -> bool:
        if len(self.message_lines) > 2:
            # 4 spaces and not '\t'
            no_space_after = not self.message_lines[-1].startswith(' ')
            four_spaces_before = self.message_lines[-2].startswith('    ')
            date_in_line = line_contains_date(self.message_lines[0])
            return date_in_line and four_spaces_before and no_space_after
        return False

    def process_message(self) -> str:
        traceback = "".join(self.message_lines[2:-1])
        log_message = self.message_lines[0]
        exception_message = self.message_lines[-1].replace('\n', '')
        exception_type = exception_message.split(':')[0]
        url = log_message.split('Error: ')[-1].strip()

        with session_scope() as session:
            existing_entry = session.query(LogEntry) \
                .filter_by(exception_message=exception_message, url=url).first()
            if not existing_entry:
                log_entry = LogEntry(
                    exception_message=exception_message,
                    exception_type=exception_type,
                    traceback=traceback,
                    url=url)
                log_entry.save(session)
            else:
                log_entry = existing_entry
                existing_entry.update(session)

        return log_entry.get_message()

    async def follow(self, log_file, append_line) -> Iterator[str]:
        log_file.seek(0, 2)
        # init coroutine
        next(append_line)
        while True:
            line = log_file.readline()
            if not line:
                await asyncio.sleep(self.timeout)
                continue
            append_line.send(line)
            if self.traceback_was_added():
                yield self.process_message()

    __str__ = __repr__
