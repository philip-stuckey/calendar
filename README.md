# Calendar

I made the calendar program that I wanted to see in the world.
It works a bit like the unix `cal` command, but it highlights dates
that it finds in a text file.

That text file is a line-oriented database of events, which are a date-time 
and a description separated by tabs.

## installation

it has a requirements.txt, but this is a minimum-effort project designed for my 
system, so you may need to tweak it

## use
there are about 4 commands at the moment

     add
       add a new event to the calendar file

     list
       list upcoming events in chronological order

     month
       show the monthly calendar, today is highlighted green, each day with an event is highlighted orange

     year
       show the monthly calendar for each month of the whole year


