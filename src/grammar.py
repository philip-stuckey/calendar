from parsy import regex, seq, any_char, string
import datetime

dash = string('-')

digits2 = regex('\d\d').map(int)

date_fmt=seq(
        year=regex('\d{4}').map(int),
        month=dash>>digits2,
        day=dash>>digits2
).combine_dict(datetime.date)

colon = string(':')
time_fmt=seq(
        hour=digits2
        minute=colon>>digits2,
        second=(colon>>digits2).optional(0)
).combine_dict(datetime.time)

timesep = string(' ')
fieldsep = string('\t')
description=any_char.many().concat()
line_format = seq(date_fmt, (timesep>>time_fmt).optional(), fieldsep>>description)


