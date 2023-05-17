from grammar import line_format, date_fmt, time_fmt
from calendar_printing import AppCalendar
from dataclasses import dataclass
from pathlib import Path

import calendar
import datetime

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


class App:
    path=Path("~/calendar").expanduser()

    def year(self, year=datetime.date.today().year):
        '''
        show the monthly calendar for each month of the whole year
        '''
        AppCalendar.from_file(self.path).print_year_calendar(year)

    def month(self, month=datetime.date.today().month, year=datetime.date.today().year):
        '''
        show the monthly calendar, today is highlighted green, each day with an event is highlighted orange
        '''
        AppCalendar.from_file(self.path).print_month_calendar(year, month)

    def week(self, today=None):
        today = datetime.date.today() if today is None else datetime.date.fromisoformat(today)
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=7)
        w = max(map(len, calendar.day_name))
        with open(self.path, 'r') as file:
            for line in sorted(file):
                event = Event.from_line(line)
                if start_of_week <= event.date <= end_of_week:
                    print(
                            calendar.day_name[event.date.weekday()].ljust(w), 
                            event.time.isoformat() if event.time is not None else ' '*8, 
                            event.description
                    )

    def day(self, date=datetime.date.today()):
        AppCalendar.from_file(self.path).print_day_calendar(date)

    def add(self, date,  *tokens):
        '''
        add a new event to the calendar file
        '''
        date = date_fmt.parse(date)
        (time, description) = time_fmt.optional().parse_partial(' '.join(tokens))
        with open(self.path, 'a') as cal_file:
            print(
                    date.isoformat()+('' if time is None else (' ' + time.isoformat())),
                    description.strip(),
                    sep='\t', 
                    file=cal_file
            )

    def today(self):
        today = datetime.date.today()
        print(today.isoformat())
        with open(self.path, 'r') as cal_file:
            for line in sorted(cal_file):
                event = Event.from_line(line)
                if event.date == today:
                    print(event._time_str(), event.description)

    def list(self):
        '''
        list upcoming events in chronological order
        '''
        today = datetime.date.today()
        with open(self.path, "r") as cal_file:
            for line in sorted(cal_file):
                event = Event.from_line(line)
                if event.date > today:
                    print(event)


if __name__ == '__main__':
    from fire import Fire
    Fire(App)
