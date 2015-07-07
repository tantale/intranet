"""
:module: intranet.tests.accessors.test_event_interval
:date: 2013-10-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>

Test case of 'intranet.accessors.event_interval' module.
"""
from __future__ import print_function
import collections
import datetime
import pprint
import unittest

from intranet.accessors.pointage.event_interval import datetime_interval, \
    find_first_event_interval, find_excluding_intervals, intersect_intervals



#==============================================================================
# Demonstration
#==============================================================================

def get_tz_offset():
    delta = datetime.datetime.utcnow() - datetime.datetime.now()
    if delta.days >= 0:
        return delta.seconds / 60  # > 0
    else:
        return (delta.seconds - 86400) / 60  # < 0


Event = collections.namedtuple('Event', ['event_start', 'event_end'])


def create_event(day, start, end, tz_offset):
    """
    @param day: day's date in ISO 8601 format: "%Y-%m-%d"

    @param start: event's start hour in format: "%H:%M"

    @param end: event's end hour in format: "%H:%M"

    @param tz_offset: time-zone offset in minutes for the current locale.

    @return: event object
    """
    date = datetime.datetime.strptime(day, "%Y-%m-%d").date()
    hour_start = datetime.datetime.strptime(start, "%H:%M").time()
    hour_end = datetime.datetime.strptime(end, "%H:%M").time()
    tz_delta = datetime.timedelta(minutes=tz_offset)
    event_start_local = datetime.datetime.combine(date, hour_start)
    event_end_local = datetime.datetime.combine(date, hour_end)
    return Event(event_start=event_start_local + tz_delta,
                        event_end=event_end_local + tz_delta)


def parse_hours(hours):
    hour_interval = hours.split(" - ")
    time = lambda hour: datetime.datetime.strptime(hour, "%H:%M").time()
    return tuple(map(time, hour_interval))


def format_hours(hour_interval, tz_offset):
    tz_delta = datetime.timedelta(minutes=tz_offset)
    local_interval = (hour_interval[0] - tz_delta, hour_interval[1] - tz_delta)
    msg_fmt = "{interval[0]:%Y-%m-%d} {interval[0]:%H:%M}-{interval[1]:%H:%M}"
    return msg_fmt.format(interval=local_interval)


class TestDemo(unittest.TestCase):
    """
    Demonstration test case
    """

    def test_find_first_event_interval(self):
        tzo = get_tz_offset()
        tzd = datetime.timedelta(minutes=int(tzo))

        event_list = [create_event("2013-10-09", "8:30", "10:00", tzo),
                      create_event("2013-10-09", "10:00", "11:00", tzo),
                      create_event("2013-10-09", "11:00", "12:30", tzo),
                      # one available: "14:00" - "15:35"
                      create_event("2013-10-09", "15:35", "17:35", tzo),
                      # one available: "17:35" - "17:45"
                      create_event("2013-10-11", "08:00", "16:00", tzo)]
        pprint.pprint(event_list)

        open_hours_dict = {1: [parse_hours("14:00 - 17:45")],
                           2: [parse_hours("8:30 - 12:30"),
                               parse_hours("14:00 - 17:45")],
                           3: [parse_hours("8:30 - 12:30"),
                               parse_hours("14:00 - 17:45")],
                           4: [parse_hours("8:30 - 12:30"),
                               parse_hours("14:00 - 17:45")],
                           5: [parse_hours("8:30 - 12:30"),
                               parse_hours("14:00 - 17:30")],
                           6: [],
                           7: []}
        pprint.pprint(open_hours_dict)

        day = datetime.datetime.strptime("2013-10-09", "%Y-%m-%d").date()
        first_hour = datetime.time(8, 0)
        event_interval = find_first_event_interval(day, first_hour, event_list,
                                                   open_hours_dict, tzd)
        pprint.pprint(format_hours(event_interval, tzo))
        expected = (datetime.datetime(2013, 10, 9, 13, 0),
                    datetime.datetime(2013, 10, 9, 14, 35))
        self.assertEqual(event_interval, expected)

        # -- another case => first_hour
        event_list.append(create_event("2013-10-09", "14:00", "15:35", tzo))
        event_list.append(create_event("2013-10-09", "17:35", "17:45", tzo))
        event_interval = find_first_event_interval(day, first_hour, event_list,
                                                   open_hours_dict, tzd)
        pprint.pprint(format_hours(event_interval, tzo))
        expected = (datetime.datetime(2013, 10, 9, 7, 0),
                    datetime.datetime(2013, 10, 9, 8, 0))
        self.assertEqual(event_interval, expected)


#==============================================================================
# Unit tests
#==============================================================================

class TestEventInterval(unittest.TestCase):
    """
    Test case of 'EventInterval' class.
    """

    def test_datetime_interval(self):
        day = datetime.date(2013, 10, 9)
        hour_interval = datetime.time(8, 0), datetime.time(10, 35)
        tz_delta = datetime.timedelta(minutes=-120)  # 2h
        actual = datetime_interval(day, hour_interval, tz_delta)
        expected = (datetime.datetime(2013, 10, 9, 6, 0),
                    datetime.datetime(2013, 10, 9, 8, 35))
        self.assertEqual(actual, expected)

    def test_find_excluding_intervals(self):
        min_value = 0
        max_value = 30

        test_case_list = [([], [(0, 30)]),
                          ([(15, 25)], [(0, 15), (25, 30)]),
                          ([(5, 15), (20, 25)], [(0, 5), (15, 20), (25, 30)]),
                          ([(5, 15), (5, 10), (20, 25)], [(0, 5), (15, 20), (25, 30)]),  # @IgnorePep8
                          ([(5, 10), (5, 15), (20, 25)], [(0, 5), (15, 20), (25, 30)]),  # @IgnorePep8
                          ([(5, 15), (10, 15), (20, 25)], [(0, 5), (15, 20), (25, 30)]),  # @IgnorePep8
                          ([(10, 15), (5, 15), (20, 25)], [(0, 5), (15, 20), (25, 30)]),  # @IgnorePep8
                          ([(5, 15), (7, 12), (20, 25)], [(0, 5), (15, 20), (25, 30)]),  # @IgnorePep8
                          ([(0, 15)], [(15, 30)]),
                          ([(15, 30)], [(0, 15)]),
                          ([(0, 30)], [])]
        for test_case in test_case_list:
            i, j = test_case
            pprint.pprint((i, j))
            actual = find_excluding_intervals(i, min_value, max_value)
            self.assertEqual(actual, j)

    def test_intersect_intervals(self):
        test_case_list = [[(10, 20), (10, 20), (10, 20)],
                          [(10, 20), (15, 20), (15, 20)],
                          [(10, 20), (20, 25), None],
                          [(15, 20), (10, 20), (15, 20)],
                          [(15, 20), (15, 20), (15, 20)],
                          [(15, 20), (20, 25), None],
                          [(20, 25), (10, 20), None],
                          [(20, 25), (15, 20), None],
                          [(20, 25), (20, 25), (20, 25)]]
        for test_case in test_case_list:
            i, j, k = test_case
            pprint.pprint((i, j, k))
            actual = intersect_intervals(i, j)
            self.assertEqual(actual, k)


if __name__ == "__main__":
    unittest.main()
