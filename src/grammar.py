from parsy import regex, seq, any_char, string
import datetime

dash = string('-')
digits=regex('\d+').map(int)
digits2 = regex('\d\d').map(int)

date_fmt=seq(
        year=regex('\d{4}').map(int),
        month=dash>>digits2,
        day=dash>>digits2
).combine_dict(datetime.date)

colon = string(':')
time_fmt=seq(
        hour=digits2,
        minute=colon>>digits2,
        second=(colon>>digits2).optional(0)
).combine_dict(datetime.time)

timesep = string(' ')
fieldsep = string('\t')

import events
description=any_char.many().concat().map(str.strip)
event_format = seq(
        date=date_fmt, 
        time=(timesep>>time_fmt).optional(), 
        description=fieldsep>>description
).combine_dict(events.Event)

# 1995-05-15 12m Robert's Birthday
# 2023-06-14  7d 18:30 D&D
# 2020-02-29 48m leap day
import recurrance

day_period=(digits<<string('d')).map(recurrance.DayPeriod)
month_period=(digits<<string('m')).map(recurrance.MonthPeriod)
period = day_period | month_period

recurrance_format = seq(
        start_date=date_fmt,
        time=(timesep>>time_fmt).optional(),
        period=timesep>>period,
        end_date=date_fmt.optional(default=datetime.date.max),
        description=fieldsep>>description
).combine_dict(recurrance.RecurringEvents)

line_format = event_format | recurrance_format
