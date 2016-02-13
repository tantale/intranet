# -*- coding: utf-8 -*-
import datetime

FREE_SLOT, BUSY_SLOT = "FREE_SLOT", "BUSY_SLOT"
ALL_SLOTS = [FREE_SLOT, BUSY_SLOT]


def round_datetime(dt, seconds=60):
    """
    Round a date/time to a multiple of a seconds.

    >>> round_datetime(datetime.datetime(2015, 12, 25, 12, 37, 5))
    datetime.datetime(2015, 12, 25, 12, 37)
    >>> round_datetime(datetime.datetime(2015, 12, 25, 12, 37, 55))
    datetime.datetime(2015, 12, 25, 12, 38)
    >>> round_datetime(datetime.datetime(2015, 12, 31, 23, 59, 59))
    datetime.datetime(2016, 1, 1, 0, 0)

    :type dt: datetime.datetime
    :param dt: The date time to round.
    :type seconds: int
    :param seconds: number of seconds to round, default is 1 minute.
    :rtype: datetime.datetime
    :return: The rounded time.
    """
    # number of seconds since midnight
    duration = (dt - dt.min).total_seconds()  # float
    rounding = round(duration / seconds) * seconds
    return dt + datetime.timedelta(0, rounding - duration, -dt.microsecond)


def round_time(a_time, seconds=60):
    today = datetime.date.today()
    dt = datetime.datetime.combine(today, a_time)
    rounded = round_datetime(dt, seconds=seconds)
    return rounded.time()


def create_time_slot(time_interval, slot_type, minutes=15):
    """
    Create the time slots of a given time interval.

    >>> import pprint

    >>> start_time = datetime.time(12, 30, 12)  # rounded to 12:30
    >>> end_time = datetime.time(14, 27, 36)  # rounded to 14:30
    >>> pprint.pprint(create_time_slot((start_time, end_time), BUSY_SLOT))
    ([datetime.time(12, 30),
      datetime.time(12, 45),
      datetime.time(13, 0),
      datetime.time(13, 15),
      datetime.time(13, 30),
      datetime.time(13, 45),
      datetime.time(14, 0),
      datetime.time(14, 15)],
     'BUSY_SLOT')

    >>> pprint.pprint(create_time_slot((start_time, start_time), BUSY_SLOT))
    ([], 'BUSY_SLOT')

    >>> slot = create_time_slot((end_time, start_time), FREE_SLOT)
    >>> slot[0][0]
    datetime.time(14, 30)
    >>> slot[0][-1]
    datetime.time(12, 15)

    :type time_interval: (datetime.time, datetime.time)
    :param time_interval: Start/ time interval (inclusive).
    :type slot_type: str or unicode
    :param slot_type: Slot type: "FREE_SLOT", "BUSY_SLOT"
    :type minutes: int
    :param minutes: number of minutes to round, default is 15 minutes.
    :rtype: list[datetime.time], (str or unicode)
    :return: The slot of times
    """
    seconds = minutes * 60
    start_time, end_time = time_interval
    start_time = round_time(start_time, seconds=seconds)
    end_time = round_time(end_time, seconds=seconds)

    today = datetime.date.today()
    start_dt = datetime.datetime.combine(today, start_time)
    end_dt = datetime.datetime.combine(today, end_time)
    duration = (end_dt - start_dt).seconds

    dt_list = [start_dt + datetime.timedelta(seconds=x) for x in xrange(0, duration, seconds)]
    return [dt.time() for dt in dt_list], slot_type


def create_time_interval(slot, minutes=15):
    """
    Create a time interval from a slot (drop the slot_type).


    >>> slot = ([datetime.time(12, 30),
    ...          datetime.time(12, 45),
    ...          datetime.time(13, 0),
    ...          datetime.time(13, 15),
    ...          datetime.time(13, 30),
    ...          datetime.time(13, 45),
    ...          datetime.time(14, 0),
    ...          datetime.time(14, 15)],
    ...         BUSY_SLOT)
    >>> create_time_interval(slot)
    (datetime.time(12, 30), datetime.time(14, 30))

    >>> create_time_interval(([], BUSY_SLOT)) is None
    True

    :type slot: list[datetime.time], (str or unicode)
    :param slot: The slot of times
    :type minutes: int
    :param minutes: number of minutes to round, default is 15 minutes.
    :rtype: (datetime.time, datetime.time)
    :return: Start/ time interval (inclusive).
    """
    seconds = minutes * 60
    time_list = slot[0]
    if not time_list:
        return None
    start_time = time_list[0]
    end_time = time_list[-1]
    today = datetime.date.today()
    start_dt = datetime.datetime.combine(today, start_time)
    end_dt = datetime.datetime.combine(today, end_time) + datetime.timedelta(seconds=seconds)
    return start_dt.time(), end_dt.time()
