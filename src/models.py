from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime, timedelta

Base = declarative_base()


class LogEntry(Base):
    __tablename__ = 'logentry' # noqa

    id = Column(Integer, primary_key=True)
    traceback = Column(Text)
    url = Column(String(200))
    exception_type = Column(String(40))
    exception_message = Column(String(200))
    notified_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    count = Column(Integer, default=1)

    def __repr__(self) -> str:
        return f"Location: {self.url}\n" \
               f"Last time happened: {self._updated_at}\n" \
               f"Exception: {self.exception_message}\n"

    @property
    def _updated_at(self):
        return datetime.strftime(self.updated_at, '%Y-%m-%d %H:%M:%S')

    @property
    def was_notified(self):
        if self.notified_at:
            return self.notified_at + timedelta(minutes=30) > datetime.now()
        return False

    def get_message(self) -> str:
        wrapped_title = f'*{self.__repr__()}*'
        wrapped_traceback = f'```{self.traceback}```'
        wrapped_exception = f"Count: {self.count}"
        return "".join([wrapped_title, wrapped_traceback, wrapped_exception])

    def save(self, session) -> None:
        session.add(self)

    def update(self, session) -> None:
        if not self.notified_at or not self.was_notified:
            self.notified_at = datetime.now()
        self.count += 1
        session.add(self)
