from grammar import line_format, date_fmt, time_fmt
from calendar_grids import MonthGrid, YearGrid

from operator import attrgetter

import calendar
from datetime import date as _date

from database import DataBase, weekof

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
        event_dates = list(map(attrgetter('date'), self._database.month(year,
            month)))
        print(MonthGrid(year, month, events=event_dates, color=self.color))

    def week(self, today=None):
        today = _date.today() if today is None else _date.fromisoformat(today)
        w = max(map(len, calendar.day_name))
        (sow, eow) = weekof(today)

        print(f"{sow.isoformat()}/{eow.isoformat()}".center(21))
        for event in self._database.weekof(today):
            print(
                calendar.day_name[event.date.weekday()].ljust(w), 
                event.time.isoformat() if event.time is not None else ' '*8, 
                event.description
            )

    def add(self, date,  *tokens):
        '''
        add a new event to the calendar file
        '''
        date = date_fmt.parse(date)
        (time, description) = time_fmt.optional().parse_partial(' '.join(tokens))
        with open(self.path, 'a') as cal_file:
            print(
                    _date.isoformat()+('' if time is None else (' ' + time.isoformat())),
                    description.strip(),
                    sep='\t', 
                    file=cal_file
            )

    def today(self):
        return self.day()

    def day(self, date=None):
        date = _date.fromisoformat(date) if date is not None else _date.today()
        print(date.isoformat())
        for event in self._database.day(date):
            print(event._time_str(), event.description)

    def list(self):
        '''
        list upcoming events in chronological order
        '''
        for event in self._database.list():
            print(event)

if __name__ == '__main__':
    from fire import Fire
    Fire(App)
