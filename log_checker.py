import time


class LogChecker(object):

    def __init__(self, file_name, timeout=0.5):
        self.timeout = timeout
        self.file_name = file_name

    def process(self):
        file = open(self.file_name)
        for item in self.follow(file):
            if "Internal Server Error" in item:
                return item
        return None

    def follow(self, log_file):
        log_file.seek(0, 2)
        while True:
            line = log_file.readline()
            if not line:
                time.sleep(self.timeout)
                continue
            yield line
