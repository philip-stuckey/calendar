from abc import ABC, abstractmethod
from datetime import date, time, timedelta
from events import Event
from dataclasses import dataclass

class Period(ABC):
    @abstractmethod
    def iter(self, start, end):
        pass

@dataclass
class RecurringEvents:
    start_date: date
    period: Period
    time: time
    description: str
    end_date: date = date.max
    
    def _new_event(self, date):
        return Event(date, self.time, self.description)

    def list(self, end: date):
        start = self.start_date
        end = min(end, self.end_date)
        for date in self.period.iter(start,end):
            yield self._new_event(start)

@dataclass
class DayPeriod(Period):
    days: int
    def _timedelta(self):
        return timedelta(days=self.days)

    def iter(self, start, end):
        date=start
        while (date - self._timedelta()) < end:
            yield date 
            date += self._timedelta()

@dataclass
class MonthPeriod(Period):
    months: int
    
    def iter(self, start, end):
        date = start
        while date.year <= end.year and (date.month < end.month or (date.day < end.day and date.month == end.month)): 
            yield date 
            m = date.month + self.months
            date = date.replace(year=date.year + (m//12), month=m%12)

@dataclass
class EndOfMonth(Period):
    def iter(self, start, end):
        for year in range(start.year,end.year):
            for month in range(1,13):
                (_, eom) = calendar.monthrange(year, month)
                yield date(year, month, eom)

