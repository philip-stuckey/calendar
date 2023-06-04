import calendar
from pathlib import Path
from datetime import date, timedelta
from itertools import chain
from operator import attrgetter

from grammar import event_format, line_format
from events import Event
from recurrance import RecurringEvents

def weekof(date: date):
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    return (start_of_week, end_of_week)

class DataBase:
    
    def load(self, calendar_path):
        path = Path(calendar_path).expanduser()
        self.events=[]
        self.recurrances=[]
        with open(path, 'r') as file:
            for line in sorted(file):
                match line_format.parse(line):
                    case e if isinstance(e,Event):
                        self.events.append(e)
                    case r if isinstance(r, RecurringEvents):
                        self.recurrances.append(e)
                    case _ :
                        raise ValueError("unknown object type in file")


    def list(self, start: date = date.today(), end: date = date.max):
        occuresin = lambda event: event.date >= start and event.date <=end
        return filter(
                occuresin, 
                chain(
                    self.events, 
                    *(rec.list(end) for rec in self.recurrances)
                )
            ) 
    
    def list_dates(self,start,end):
        return map(attrgetter('date'), self.list(start, end))

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

