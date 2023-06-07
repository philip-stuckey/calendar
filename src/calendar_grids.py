from dataclasses import dataclass
from datetime import date
import calendar

ANSI_GREEN = "\033[42m"  # Highlight today's date in green
ANSI_YELLOW = "\033[43m"  # Highlight other dates in yellow
ANSI_RED = "\033[41m"
ANSI_RESET = "\033[0m"  # Reset text color

def hilight(string, color):
    return color + string + (ANSI_RESET if color != '' else '')

@dataclass
class MonthGrid:

    year: int
    month: int
    events: list[date]
    color: bool = True

    def important_days(self) -> int:
        for event in self.events:
            if event.year == self.year and event.month == self.month:
                yield event.day

    @property
    def today(self) -> int:
        today = date.today()
        if today.year==self.year and today.month==self.month:
            return today.day
        else:
            return -1
    
    def grid_header(self):
        return f"{calendar.month_name[self.month]} {self.year}".center(20)

    def day_color(self, day):
        if not self.color:
            return ''

        if day == self.today and day in self.important_days():
            return ANSI_RED
        elif day == self.today:
            return ANSI_GREEN
        elif day in self.important_days():
            return ANSI_YELLOW
        else:
            return ''

    def format_day(self, day: int):
        day_str = str(day).rjust(2) if day != 0 else '  '
        return hilight(day_str, self.day_color(day))

    def format_row(self, row):
        return ' '.join(map(self.format_day, row))

    def month_grid(self):
        yield self.grid_header()
        yield calendar.weekheader(2) 
        for row in calendar.monthcalendar(self.year, self.month):
            yield self.format_row(row)
    
    def __str__(self):
        return '\n'.join(self.month_grid())


@dataclass
class YearGrid:
    year: int
    events: set[date]
    color: bool = True
    cols=3
    
    def grid_for(self, month):
        return MonthGrid(self.year, month, self.events, self.color)

    def line_iterator(self):
        for start in range(1,13, self.cols):
            offsets = range(self.cols)
            months = [self.grid_for(month=start+offset) for offset in offsets]
            for row in zip(*map(MonthGrid.month_grid, months)):
                yield (' '*3).join(row)

            yield ''

    def __str__(self):
        return "\n".join(self.line_iterator())

