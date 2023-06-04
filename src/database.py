from dataclasses import dataclass
from pathlib import Path
from datetime import date, timedelta
import calendar
from events import Event

def weekof(date: date):
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    return (start_of_week, end_of_week)

@dataclass
class DataBase:
    calendar: Path = Path('~/Calendar/calendar').expanduser()
    
    def events(self):
        with open(self.calendar, 'r') as file:
            return map(Event.from_line, sorted(file))

    def list(self, start: date = date.today(), end: date = date.max):
        occuresin = lambda event: event.date >= start and event.date <=end
        return filter(occuresin, self.events())

    def year(self, year: int):
        return self.list(date(year,1,1), date(year, 12, 31))

    def month(self, year: int, month: int):
        (_, days_in_month) = calendar.monthrange(year, month)
        start_of_month = date(year, month, 1)
        end_of_month = date(year, month, days_in_month)
        return self.list(start_of_month, end_of_month)

    def weekof(self, date):
        start_of_week, end_of_week  = weekof(date)
        return self.list(start_of_week, end_of_week)
    
    def day(self, date):
        return self.list(start=date, end=date)

