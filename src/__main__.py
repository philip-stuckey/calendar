from grammar import line_format, date_fmt, time_fmt
from calendar_grids import MonthGrid, YearGrid
from events import Event

from operator import attrgetter

import calendar
from datetime import date as _date, timedelta

from database import DataBase, weekof

def daterange(start: _date, end: _date, delta=timedelta(days=1)):
    while start < end:
        yield start
        start += delta

class App:

    @property
    def cal_path(self):
        return self._cal_path

    @cal_path.setter
    def cal_path(self, path):
        self._cal_path = path
        self._database.load(path)

    def __init__(self, cal_path="~/Calendar/calendar", color=True):
        self._database = DataBase()
        self._database.load(cal_path)
        self._cal_path = cal_path
        self.color=color


    def year(self, year=_date.today().year):
        '''
        show the monthly calendar for each month of the whole year
        '''
        event_dates = list(map(attrgetter('date'), self._database.year(year)))
        print(YearGrid(year, events=event_dates, color=self.color))

    def month(self, month=_date.today().month, year=_date.today().year):
        '''
        show the monthly calendar, today is highlighted green, each day with an event is highlighted orange
        '''
        event_dates = map(attrgetter('date'), self._database.month(year, month))
        print(MonthGrid(year, month, events=list(event_dates), color=self.color))

    def week(self, today=None):
        today = _date.today() if today is None else _date.fromisoformat(today)
        w = 3
        (sow, eow) = weekof(today)

        print(f"{sow.isoformat()}/{eow.isoformat()}".center(21))
        for event in self._database.weekof(today):
            print(
                calendar.day_name[event.date.weekday()][:w].ljust(w), 
                event.time.strftime('%H:%M') if event.time is not None else ' '*5,
                event.description
            )

    def add(self, date,  *tokens):
        '''
        add a new event to the calendar file
        '''
        date = date_fmt.parse(date)
        (time, description) = time_fmt.optional().parse_partial(' '.join(tokens))
        self._database.add(Event(date, time, description))

    def today(self):
        return self.day()

    def day(self, date=None):
        date = _date.fromisoformat(date) if date is not None else _date.today()
        print(date.isoformat())
        for event in self._database.day(date):
            print(event._time_str(), event.description)
    
    def agenda(self, start=None, end=None):
        start = _date.today() if start is None else _date.fromisoformat(start)
        end = start + timedelta(days=7) if end is None else _date.fromisoformat(end)
        for date in daterange(start, end):
            header_fmt = f'%Y-%m-%d %a {"(today)" if date == _date.today() else ""}'
            print(date.strftime(header_fmt))
            for event in self._database.day(date):
                print(
                    ' '*5,
                    event.time.strftime('%H:%M') if event.time is not None else ' '*5,
                    event.description
                )


    def list(self, start, end):
        '''
        list upcoming events in chronological order
        '''
        start = _date.fromisoformat(start)
        end = _date.fromisoformat(end)
        for event in self._database.list(start,end):
            print(event)

if __name__ == '__main__':
    from fire import Fire
    Fire(App)
