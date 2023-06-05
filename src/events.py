import datetime
from dataclasses import dataclass

@dataclass
class Event:
    date: datetime.date
    time: datetime.time
    description: str

    def _time_str(self):
        return '' if self.time is None else (' ' + self.time.isoformat())

    def __str__(self):
        return f'{self.date.isoformat()}{self._time_str()}\t{self.description}'

