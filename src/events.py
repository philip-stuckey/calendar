import datetime
from dataclasses import dataclass
from grammar import line_format

@dataclass
class Event:
    date: datetime.date
    time: datetime.time
    description: str

    @staticmethod
    def from_line(line: str):
        (date,time,description) = line_format.parse(line)
        return Event(
                date=date,
                time=time,
                description=description.strip()
        )

    def _time_str(self):
        return '' if self.time is None else (' ' + self.time.isoformat())

    def __str__(self):
        return f'{self.date.isoformat()}{self._time_str()}\t{self.description}'


