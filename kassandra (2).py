# -*- coding: utf-8 -*-

import csv
import re
from dateutil.parser import parse

STUCK_YEAR = 2022
DATE_FORMAT = "%Y-%m-%d"


def parse_date(str):
    for rus, eng in (('янв', 'jan'), ('фев', 'feb'), ('мар', 'mar'), ('апр', 'apr'), ('ма', 'may'), ('июн', 'jun'), ('июл', 'jul'), ('авг', 'aug'), ('сен', 'sep'), ('окт', 'oct'), ('ноя', 'nov'), ('дек', 'dec')):
        str = re.sub(r'\b' + rus + r'\w*', eng, str, flags=re.IGNORECASE)
    try:
        return parse(str)
    except:
        return None


def load_events(file):
    events = []
    with open(file, encoding='utf-8') as f:
        for row in csv.reader(f):
            if len(row) == 0:
                # Пустая строка
                continue
            when = parse_date(row[0])
            what = ', '.join(row[1:])
            if not when:
                print("Непонятная дата:", row[0])
                continue
            when = when.replace(year=STUCK_YEAR)
            events.append((when, what))
    return events


def find_events(events, when):
    found = []
    for e in events:
        if e[0].month == when.month:
            found.append(e[1])
    return found


if __name__ == '__main__':
    events = load_events('kassandra.csv')
    print(f"Мне открылись знания о {len(events)} событиях в {STUCK_YEAR} году!")

    while (True):
        when = input("\nКогда? ")
        if not when:
            print("Ок, я ухожу")
            break
        when = parse_date(when)
        if not when:
            print("Непонятно. Попробуйте ещё раз")
            continue
        if when.year != STUCK_YEAR:
            print("У нас каленадрь на", STUCK_YEAR)
            when = when.replace(year=STUCK_YEAR)
        print("Значит", when.strftime(DATE_FORMAT))
        predict = find_events(events, when)
        if predict:
            for what in predict:
                print("  ", what)
        else:
            print("Будущее покрыто мраком")
