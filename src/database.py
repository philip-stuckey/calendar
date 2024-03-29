import calendar
from pathlib import Path
from datetime import date, timedelta
from itertools import chain
from operator import attrgetter

from grammar import event_format, file_format
from events import Event
from recurrance import RecurringEvents

def weekof(date: date):
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    return (start_of_week, end_of_week)

class DataBase:
    
    def load(self, calendar_path):
        self.path = Path(calendar_path).expanduser()
        self.events=[]
        self.recurrances=[]
        items = file_format.parse(self.path.read_text())
        for item in items:
            if isinstance(item,Event):
                self.events.append(item)
            elif isinstance(item, RecurringEvents):
                self.recurrances.append(item)
            else:
                raise ValueError("unknown object type in file")
        self.events.sort(key=lambda x: x.date)

    def add(self, event: Event):
        with open(self.path, 'a') as cal_file:
            print(event, file=cal_file)

    def _singular_events(self):
        yield from self.events

    def _recurring_events(self, end: date):
        for recurrance in self.recurrances:
            yield from recurrance.list(end)
    
    def _all_events(self, end: date):
        yield from self._singular_events()
        yield from self._recurring_events(end)

    def list(self, start=date.today(), end=date.max):
        occuresin = lambda e: e.date >= start and e.date < end
        all_events = list(self._all_events(end))
        filtered = [e for e in all_events if occuresin(e)] 
        ordered = sorted(filtered, key=lambda e: e.date)
        return ordered                        

    def year(self, year: int):
        return self.list(date(year,1,1), date(year, 12, 31))

    def month(self, year: int, month: int):
        (_, days_in_month) = calendar.monthrange(year, month)
        start_of_month = date(year, month, 1)
        end_of_month = date(year, month, days_in_month)
        return self.list(start_of_month, end_of_month)
   
    def day(self, date):
        return self.list(date, date+timedelta(days=1))
