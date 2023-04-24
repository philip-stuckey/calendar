import calendar
from datetime import date, time, timedelta
from dataclasses import dataclass
from grammar import date_fmt, time_fmt
from more_itertools import pairwise
from math import floor
@dataclass
class AppCalendar:
    events: list[date]
    
    # Define ANSI escape codes for highlighting dates
    ANSI_GREEN = "\033[42m"  # Highlight today's date in green
    ANSI_YELLOW = "\033[43m"  # Highlight other dates in yellow
    ANSI_RESET = "\033[0m"  # Reset text color
    
    @staticmethod
    def from_file(file_path):
        with open(file_path, 'r') as cal_file:
            dates = [date_fmt.parse_partial(event)[0] for event in cal_file]
            return AppCalendar(dates)

    def print_year_calendar(self, year):
        for start in range(1,13,3):
            for bits in zip(*(self.format_month(year, start+offset).split('\n') for offset in (0,1,2))):
                print('   '.join(bits))
            print()


    def print_month_calendar(self, year, month):
        print(self.format_month(year,month))

    @staticmethod
    def _time_range(start=time.min, stop=time.max, step=timedelta(minutes=30)):
        t = datetime.combine(datetime.today(), start)
        end = datetime.combine(datetime.today(), stop)
        while t < end:
            yield t
            t += step


    def format_events(events):
        count = len(events)
        total_space = len(day_name)
        space = total_space/count
        return '/'.join(event.description[0:space].center(space) for event in events)

    def format_day(self, day: date, time_range):
        day_name = calendar.day_name[date.weekday()]
        yield day_name

        events = [event for event in self.events if event.date == day and event.time is not None]
        for start,end in pairwise(time_range):
            hour_events = [event for event in events if start <= event.time < end]
            event_count = len(hour_events)
            if event_count == 0:
                yield ''
            else:
                yield self.format_events(hour_events)


    def format_month(self, year, month):
        return self.format_header(year, month) + '\n' +\
        '\n'.join([self.format_row(row,month,year) for row in calendar.monthcalendar(year, month)])

    def format_header(self, year, month):
        return (calendar.month_name[month] +' '+ str(year)).center(20)+\
            '\n'+calendar.weekheader(2) + ' '

    # Define a function to format a single calendar row as a string
    def format_row(self, row, month, year):
        formatted_row = ""
        for day in row:
            if day == 0:
                # Add spaces for days outside of the current month
                formatted_row += "   "
            elif date(year, month, day) == date.today():
                # Highlight today's date in green
                formatted_row += f"{self.ANSI_GREEN}{day:2}{self.ANSI_RESET} "
            elif date(year, month, day) in self.events:
                # Highlight other dates in yellow
                formatted_row += f"{self.ANSI_YELLOW}{day:2}{self.ANSI_RESET} "
            else:
                # Add unhighlighted day to string
                formatted_row += f"{day:2} "
        return formatted_row.ljust(20)



