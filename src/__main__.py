from grammar import line_format, date_fmt, time_fmt
from calendar_printing import AppCalendar
from dataclasses import dataclass
from pathlib import Path

from events import Event
import calendar
from datetime import datetime, timedelta, date as _date

from database import DataBase

class App:
    database: DataBase()

    def year(self, year=_date.today().year):
        '''
        show the monthly calendar for each month of the whole year
        '''
        AppCalendar.from_file(self.path).print_year_calendar(year)

    def month(self, month=_date.today().month, year=_date.today().year):
        '''
        show the monthly calendar, today is highlighted green, each day with an event is highlighted orange
        '''
        AppCalendar.from_file(self.path).print_month_calendar(year, month)

    def week(self, today=None):
        today = _date.today() if today is None else _date.fromisoformat(today)
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        w = max(map(len, calendar.day_name))
        for event in self.database.list(start_of_week, end_of_week):
            print(
                calendar.day_name[event.date.weekday()].ljust(w), 
                event.time.isoformat() if event.time is not None else ' '*8, 
                event.description
            )
                   

    def day(self, date=_date.today()):
        AppCalendar.from_file(self.path).print_day_calendar(date)

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
        today = _date.today()
        print(today.isoformat())
        for event in self.database.list(end=date.today():
            print(event._time_str(), event.description)

    def list(self):
        '''
        list upcoming events in chronological order
        '''
        for event in self.database.list()
            print(event)

if __name__ == '__main__':
    from fire import Fire
    Fire(App)
