from typing import Optional, Iterator
from bot import LogFileBot

from utils import line_contains_date

import asyncio


class LogChecker(object):

    def __init__(self,
                 file_name: str,
                 bot: LogFileBot,
                 timeout: float = 0.5,
                 get_traceback: bool = True,
                 search_string: Optional[str] = None) -> None:
        self.mes = []
        self.bot = bot
        self.timeout = timeout
        self.file_name = file_name
        self.get_traceback = get_traceback
        self.search_string = search_string

    def __repr__(self) -> str:
        return f"Chat ID: {self.bot.chat_id}. Search String: {self.search_string}"

    async def process(self) -> None:
        file = open(self.file_name)
        new_messages = self.follow(file, self.append_line())
        async for message in new_messages:
            self.bot.notify(message)
            self.mes.clear()

    def append_line(self) -> None:
        while True:
            line = (yield)
            self.mes.append(line)

    def traceback_was_added(self) -> bool:
        if len(self.mes) > 2:
            # 4 spaces and not '\t'
            no_space_after = not self.mes[-1].startswith(' ')
            four_spaces_before = self.mes[-2].startswith('    ')
            date_in_line = line_contains_date(self.mes[0])
            return date_in_line and four_spaces_before and no_space_after
        return False

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
                yield "".join(self.mes)

    __str__ = __repr__
