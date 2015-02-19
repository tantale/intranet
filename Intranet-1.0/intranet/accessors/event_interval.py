"""
:module: intranet.accessors.event_interval
:date: 2013-10-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import datetime

__author__ = "Laurent LAPORTE <llaporte@jouve.fr>"
__version__ = "$Revision: $"
# $Id: $


def datetime_interval(day, hour_interval, tz_delta):
    """
    Create a date/time interval for the current day using the given
    time-zone offset.

    :param day: day's date
    :type day: datetime.date

    :param hour_interval: time's couple (hour_start, hour_end)
    :type hour_interval: tuple(datetime.time, datetime.time)

    :param tz_delta: time-zone delta.
    :type tz_delta: datetime.timedelta

    :return: date/time's couple (datetime_start, datetime_end)
    :rtype: tuple(datetime.datetime, datetime.datetime)
    """
    datetime_start_local = datetime.datetime.combine(day, hour_interval[0])
    datetime_end_local = datetime.datetime.combine(day, hour_interval[1])
    return (datetime_start_local + tz_delta,
            datetime_end_local + tz_delta)


def find_excluding_intervals(intervals, min_value, max_value):
    """
    Find excluding intervals between min and max values.

    :param intervals: intervals list
    :type intervals: list<tuple(start, end)>

    :param min_value: min value

    :param max_value: max value

    :return: new intervals list containing exclusive intervals
    :rtype: list<tuple(start, end)>
    """
    excluding_list = []
    next_start = min_value
    for start, end in sorted(intervals):
        if next_start < start:
            excluding_list.append((next_start, start))
            next_start = end
        elif next_start < end:
            next_start = end
    if next_start < max_value:
        excluding_list.append((next_start, max_value))
    return excluding_list


def intersect_intervals(i, j):
    """
    Calculate intervals intersection.

    :param i: first interval
    :type i: tuple(start, end)

    :param j: second interval
    :type j: tuple(start, end)

    :return: intervals intersection if any, or None
    :rtype: tuple(start, end) or None
    """
    if i[0] <= j[0] < i[1] or j[0] <= i[0] < j[1]:
        return max(i[0], j[0]), min(i[1], j[1])
    else:
        return None


def find_event_intervals(day, event_list, work_hours_dict, tz_delta):
    """
    Find the event intervals available in open hours.

    :param day: day's date
    :type day: datetime.date

    :param event_list: events list with event's start and end date/time (UTC).
    :type event_list: list<Event>

    :param work_hours_dict: dictionary containing the lists of open hours
    grouped by week day (ISO week day).
    Each open hour is a time interval (in local time).

    Example: {1: [(datetime.time(14, 0), datetime.time(17, 45))],
              2: [(datetime.time(8, 30), datetime.time(12, 30)),
                  (datetime.time(14, 0), datetime.time(17, 45))],
              3: [(datetime.time(8, 30), datetime.time(12, 30)),
                  (datetime.time(14, 0), datetime.time(17, 45))],
              4: [(datetime.time(8, 30), datetime.time(12, 30)),
                  (datetime.time(14, 0), datetime.time(17, 45))],
              5: [(datetime.time(8, 30), datetime.time(12, 30)),
                  (datetime.time(14, 0), datetime.time(17, 30))],
              6: [],
              7: []}

    :param tz_delta: time-zone delta from UTC.
    :type tz_delta: datetime.timedelta

    :return: a date/time interval (in UTC) used to create a new event
    :rtype: tuple(start, end)
    """
    # -- date/time intervals for the open hours with the given time-zone offset
    work_hours = work_hours_dict[day.isoweekday()]
    open_list = [datetime_interval(day, interval, tz_delta)
                 for interval in work_hours]

    # -- compute the available dates between the events
    min_datetime = datetime.datetime.combine(day, datetime.time(0)) + tz_delta
    max_datetime = min_datetime + datetime.timedelta(days=1)
    event_interval_list = [(event.event_start, event.event_end)
                           for event in event_list]
    available_list = find_excluding_intervals(event_interval_list,
                                              min_datetime, max_datetime)

    # -- compute intersection with open hours
    intersection_list = []
    for open_interval in open_list:
        for available_interval in available_list:
            interval = intersect_intervals(open_interval, available_interval)
            if interval:
                intersection_list.append(interval)
    return intersection_list


def find_first_event_interval(day, first_hour, event_list, work_hours_dict,
                              tz_delta):
    """
    Find the first event interval available in open hours.

    :param day: day's date
    :type day: datetime.date

    :param first_hour: 1st hour if no available interval is found (local time)
    :type first_hour: datetime.time

    :param event_list: events list with event's start and end date/time (UTC).
    :type event_list: list<Event>

    :param work_hours_dict: dictionary containing the lists of open hours
    grouped by week day (ISO week day).
    Each open hour is a time interval (in local time).

    :param tz_delta: time-zone delta from UTC.
    :type tz_delta: datetime.timedelta

    :return: a date/time interval (in UTC) used to create a new event
    :rtype: tuple(start, end)
    """
    interval_list = find_event_intervals(day, event_list, work_hours_dict,
                                         tz_delta)
    if interval_list:
        # -- return the 1st interval...
        interval_list.sort()
        return interval_list[0]
    else:
        # -- ... or an interval starting at the 1st hour
        event_start = datetime.datetime.combine(day, first_hour) + tz_delta
        event_end = event_start + datetime.timedelta(hours=1)
        return event_start, event_end


def guess_event_duration(day, hour_start, event_list, work_hours_dict,
                         tz_delta):
    """
    Guess the event duration by finding available time intervals
    in the current day.

    :param day: day's date
    :type day: datetime.date

    :param hour_start: start hour of the event (local time)
    :type hour_start: datetime.time

    :param event_list: events list with event's start and end date/time (UTC).
    :type event_list: list<Event>

    :param work_hours_dict: dictionary containing the lists of open hours
    grouped by week day (ISO week day).
    Each open hour is a time interval (in local time).

    :param tz_delta: time-zone delta from UTC.
    :type tz_delta: datetime.timedelta

    :return: The maximum event duration starting at 'hour_start'
    if available, else 1 hour.
    :rtype: datetime.timedelta
    """
    event_start = datetime.datetime.combine(day, hour_start) + tz_delta
    interval_list = find_event_intervals(day, event_list, work_hours_dict,
                                         tz_delta)
    for interval in interval_list:
        if interval[0] <= event_start < interval[1]:
            return interval[1] - event_start  # timedelta
    return datetime.timedelta(hours=1)
