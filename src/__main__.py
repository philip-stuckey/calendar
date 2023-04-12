from grammar import line_format, date_fmt, time_fmt
from calendar_printing import AppCalendar
from dataclasses import dataclass

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
    cal_path="share/calendar"

    def year(self, year=datetime.date.today().year):
        '''
        show the monthly calendar for each month of the whole year
        '''
        AppCalendar.from_file(self.cal_path).print_year_calendar(year)

    def month(self, month=datetime.date.today().month, year=datetime.date.today().year):
        '''
        show the monthly calendar, today is highlighted green, each day with an event is highlighted orange
        '''
        AppCalendar.from_file(self.cal_path).print_month_calendar(year, month)

    def add(self, date,  *tokens):
        '''
        add a new event to the calendar file
        '''
        date = date_fmt.parse(date)
        (time, _) = time_fmt.optional().parse_partial(tokens[0])
        description = ' '.join(tokens[(0 if time is None else 1):])
        with open(self.cal_path, 'a') as cal_file:
            print(
                    date.isoformat()+('' if time is None else (' ' + time.isoformat())),
                    description,
                    sep='\t', 
                    file=cal_file
            )

    def list(self):
        '''
        list upcoming events in chronological order
        '''
        today = datetime.date.today()
        with open(self.cal_path, "r") as cal_file:
            for line in sorted(cal_file):
                event = Event.from_line(line)
                if event.date > today:
                    print(event)


if __name__ == '__main__':
    from fire import Fire
    Fire(App)
