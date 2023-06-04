from abc import ABC, abstractmethod
from datetime import date, time, timedelta
from events import Event
from dataclasses import dataclass

class Period(ABC):
    @abstractmethod
    def next(self, date):
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
        while start <= end:
            yield self._new_event(start)
            start = self.period.next(start)

@dataclass
class DayPeriod(Period):
    days: int
    def next(self, date):
        return date + timedelta(days=self.days)

@dataclass
class MonthPeriod(Period):
    months: int
    def next(self, date):
        m = date.month + self.months
        return date.replace(year=date.year + (m//12), month=m%12)

@dataclass
class EndOfMonth(Period):
    def next(self, date):
        (_, eom) = calendar.monthrange(date.year, date.month)
        if date.day == eom:
            date = date.replace(day=1)
            date = MonthPeriod(1).next(date)
            (_, eom) = calendar.monthrange(date.year, month)

        return date.replace(day=eom)

