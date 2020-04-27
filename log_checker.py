import asyncio


class LogChecker(object):

    def __init__(self, file_name, bot, timeout=0.5, search_string='Internal Server Error'):
        self.mes = []
        self.bot = bot
        self.timeout = timeout
        self.file_name = file_name
        self.search_string = search_string

    async def process(self):
        file = open(self.file_name)
        new_lines = self.follow(file, self.filter_on_search_string())
        async for item in new_lines:
            self.bot.notify(item)
            self.mes.clear()

    def filter_on_search_string(self):
        while True:
            line = (yield)
            self.mes.append(line)

    def traceback_was_added(self):
        if len(self.mes) > 2:
            # 4 spaces and not '\t'
            no_space_after = not self.mes[-1].startswith(' ')
            four_spaces_before = self.mes[-2].startswith('    ')
            search_string_in_title = self.search_string in self.mes[0]
            return search_string_in_title and four_spaces_before and no_space_after

    async def follow(self, log_file, a):
        log_file.seek(0, 2)
        # init coroutine
        next(a)
        while True:
            line = log_file.readline()
            if not line:
                await asyncio.sleep(self.timeout)
                continue
            a.send(line)
            if self.traceback_was_added():
                yield "".join(self.mes)
