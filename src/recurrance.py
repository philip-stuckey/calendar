from abc import ABC, abstractmethod
from datetime import date, time, timedelta
from events import Event
from dataclasses import dataclass

class Period(ABC):

    @abstractmethod
    def update(old: date) -> date:
        pass

    def iter(self, start, end):
        date=start
        while date < end:
            yield date
            try:
                date = self.update(date)
            except ValueError:
                return  # this is going to bite me in the ass someday

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
    
    def update(self, old: date) -> date:
        return old + self._timedelta()

@dataclass
class MonthPeriod(Period):
    months: int
    
    def update(self, old: date) -> date:
        m = old.month + self.months
        return old.replace(year=old.year + (m//12), month=m%12)

@dataclass
class EndOfMonth(Period):
    def eom(self, date):
        (_, eom) = calendar.monthrange(year, month)
        return date.replace(day=eom)

    def update(self, old: date) -> date:
        m = date.month+1
        y = date.year + (m//12)
        (_, eom) = calendar.monthrange(y,m)
        return date(y,m,eom)

    def iter(self, start, end):
        yield from self.Period.iter(self.eom(start), end)
