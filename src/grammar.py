from parsy import regex, seq, any_char, string
import datetime

dash = string('-')

date_fmt=seq(
        year=regex('\d{4}').map(int),
        month=(dash>>regex('\d\d')).map(int),
        day=(dash>>regex('\d\d')).map(int)
).combine_dict(datetime.date)

colon = string(':')
time_fmt=seq(
        hour=regex('\d\d').map(int),
        minute=(colon>>regex('\d\d')).map(int),
        second=(colon>>regex('\d\d')).map(int).optional(0)
).combine_dict(datetime.time)

timesep = string(' ')
fieldsep = string('\t')
description=any_char.many().concat()
line_format = seq(date_fmt, (timesep>>time_fmt).optional(), fieldsep>>description)


