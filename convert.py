# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import datetime
from icalendar import Calendar, Event, vRecur
import pytz

__author__ = 'nsaje'

weekday_names = ['ponedeljek', 'torek', 'sreda', u'četrtek', 'petek']


def convert(content):
    print content
    soup = BeautifulSoup(content)
    entries = [cell.span.text for cell in
               soup.find_all(name='td', attrs={'class': 'allocated'})]
    #entries = [entries[1]]

    entries = [filter(lambda x: len(x) > 0,
                      map(lambda x: x.strip(),
                          e.split('\n')))
               for e in entries]
    print entries

    d = datetime.datetime(datetime.date.today().year - 1, 1, 1,
                          tzinfo=pytz.timezone('Europe/Ljubljana'))
    d = d - datetime.timedelta(d.weekday())  # find monday

    cal = Calendar()
    cal.add('prodid', '-//FRiCal//SL')
    cal.add('version', '2.0')

    for e in entries:
        dt_tokens = e[0].split(' ')  # u'sreda 08:00 - 11:00'
        weekday = weekday_names.index(dt_tokens[0])
        time_start = int(dt_tokens[1].split(':')[0])
        time_end = int(dt_tokens[3].split(':')[0])
        d_start = d + datetime.timedelta(days=weekday, hours=time_start)
        d_end = d + datetime.timedelta(days=weekday, hours=time_end)
        summary = "%s; %s" % (e[2], e[1])
        description = "%s\n%s" % (e[3], '\n'.join(e[4:]))

        event = Event()
        event.add('dtstart', d_start)
        event.add('dtend', d_end)
        event.add('dtstamp', d)
        event.add('rrule', vRecur(freq='daily', interval=7))
        event.add('summary', summary)
        event.add('description', description)
        cal.add_component(event)

    return cal.to_ical()

if __name__ == "__main__":
    url = "http://urnik.fri.uni-lj.si/allocations?student=63100349&timetable=159&timetable=168"
    import urllib2
    f = urllib2.urlopen(url)
    #f = open('testSource.html')
    content = f.read()

    print convert(content)
