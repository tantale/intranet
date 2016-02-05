"""
:module: intranet.accessors.cal_event
:date: 2013-09-19
:author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
import datetime
import logging

import transaction
from sqlalchemy.sql.expression import and_

from intranet.accessors import BasicAccessor
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.pointage.event_interval import find_first_event_interval, guess_event_duration
from intranet.accessors.pointage.order import OrderAccessor
from intranet.accessors.pointage.order_phase import OrderPhaseAccessor
from intranet.model.pointage.cal_event import CalEvent

LOG = logging.getLogger(__name__)


class CalEventAccessor(BasicAccessor):
    """
    Calendar event's accessor.
    """

    def __init__(self, session=None):
        super(CalEventAccessor, self).__init__(record_class=CalEvent,
                                               session=session)
        self.employee_accessor = EmployeeAccessor(self.session)
        self.order_accessor = OrderAccessor(self.session)
        self.order_phase_accessor = OrderPhaseAccessor(self.session)

    def get_employee(self, employee_uid):
        return self.employee_accessor.get_employee(employee_uid)

    def get_employee_list(self, filter_cond=None, order_by_cond=None):
        return self.employee_accessor.get_employee_list(filter_cond,
                                                        order_by_cond)

    def get_order(self, order_uid):
        return self.order_accessor.get_order(order_uid)

    def get_order_list(self, filter_cond=None, order_by_cond=None):
        return self.order_accessor.get_order_list(filter_cond, order_by_cond)

    def get_order_phase(self, order_phase_uid):
        return self.order_phase_accessor.get_order_phase(order_phase_uid)

    def get_cal_event(self, uid):
        LOG.debug("get_cal_event: {uid!r}".format(uid=uid))
        return self._get_record(uid)

    def get_cal_event_list(self, filter_cond=None, order_by_cond=None):
        LOG.debug("get_cal_event_list")
        return self._get_record_list(filter_cond, order_by_cond)

    def get_day_events(self, employee_uid, day, tz_delta):
        """
        Get the day's events of a given employee.

        :type employee_uid: int
        :param employee_uid: employee's uid

        :param day: day's date (local time)
        :type day: datetime.date

        :param tz_delta: time-zone delta from UTC.
        :type tz_delta: datetime.timedelta

        :return: the event's list.
        :rtype: list<CalEvent>
        """
        day_start_local = datetime.datetime.combine(day, datetime.time(0, 0))
        day_start_utc = day_start_local - tz_delta
        day_end_utc = day_start_utc + datetime.timedelta(days=1)
        filter_cond = and_(CalEvent.employee_uid == employee_uid,
                           CalEvent.event_start >= day_start_utc,
                           CalEvent.event_end <= day_end_utc)
        event_list = self.get_cal_event_list(filter_cond)
        return event_list

    @staticmethod
    def _get_default_work_hours():
        """
        Get the default work hours of any employee.

        :return: dictionary of work hours grouped by week day (ISO week day).
        Each open hour is a time interval (in local time).
        Monday is 1 and Sunday is 7.
        """
        wh_dict = {1: [(datetime.time(13, 30), datetime.time(17, 45))],
                   2: [(datetime.time(8, 0), datetime.time(12, 30)),
                       (datetime.time(13, 30), datetime.time(17, 45))],
                   3: [(datetime.time(8, 0), datetime.time(12, 30)),
                       (datetime.time(13, 30), datetime.time(17, 45))],
                   4: [(datetime.time(8, 0), datetime.time(12, 30)),
                       (datetime.time(13, 30), datetime.time(17, 45))],
                   5: [(datetime.time(8, 0), datetime.time(12, 30)),
                       (datetime.time(13, 30), datetime.time(17, 30))],
                   6: [(datetime.time(8, 0), datetime.time(12, 30)),
                       (datetime.time(13, 30), datetime.time(17, 45))],
                   7: []}
        return wh_dict

    def _get_slots(self, employee_uid, day, tz_delta):
        """
        Get the available slots of the employee at a given date.

        :type employee_uid: int
        :param employee_uid: employee's uid

        :param day: day's date (local time)
        :type day: datetime.date

        :param tz_delta: time-zone delta from UTC.
        :type tz_delta: datetime.timedelta

        :rtype: list[tuple(datetime.time, datetime.time)]
        :return: List of slots. Each slot is a open hour is a time interval (in local time).

            Example: [(datetime.time(8, 0),   datetime.time(12, 30)),
                      (datetime.time(13, 30), datetime.time(17, 45))]
        """
        wh_dict = self._get_default_work_hours()
        return wh_dict[day.isoweekday()]

    def get_event_interval(self, employee_uid, day, tz_delta):
        """
        Find the start date for a new event in a day.

        :type employee_uid: int
        :param employee_uid: employee's uid

        :param day: day's date (local time)
        :type day: datetime.date

        :param tz_delta: time-zone delta from UTC.
        :type tz_delta: datetime.timedelta

        :return: a date/time interval (in UTC) used to create a new event
        :rtype: tuple(start, end)
        """
        # -- 1st hour if no available interval is found (local time)
        first_hour = datetime.time(8, 0)

        # -- events list of the current employee for that day
        event_list = self.get_day_events(employee_uid, day, tz_delta)

        # -- lists of available slots of this day
        slots = self._get_slots(employee_uid, day, tz_delta)

        return find_first_event_interval(day, first_hour, event_list,
                                         slots, tz_delta)

    def get_event_duration(self, employee_uid, day, tz_delta, hour_start):
        """
        Find the start date for a new event in a day.

        :type employee_uid: int
        :param employee_uid: employee's uid

        :param day: day's date (local time)
        :type day: datetime.date

        :param tz_delta: time-zone delta from UTC.
        :type tz_delta: datetime.timedelta

        :param hour_start: start hour of the event (local time)
        :type hour_start: datetime.time

        :return: a date/time interval (in UTC) used to create a new event
        :rtype: tuple(start, end)
        """
        # -- events list of the current employee for that day
        event_list = self.get_day_events(employee_uid, day, tz_delta)

        # -- lists of available slots of this day
        slots = self._get_slots(employee_uid, day, tz_delta)

        return guess_event_duration(day, hour_start, event_list,
                                    slots, tz_delta)

    def insert_cal_event(self, employee_uid, order_phase_uid,
                         event_start, event_end, comment):
        try:
            # NOTE: selection/insertion order is important:
            # first query the foreign objects...
            employee = self.get_employee(employee_uid)
            order_phase = self.get_order_phase(order_phase_uid)
            # ... then create a new calendar event and attach them...
            cal_event = CalEvent(event_start, event_end, comment)
            cal_event.employee = employee
            cal_event.order_phase = order_phase
            # ... and commit.
            transaction.commit()
        except:
            transaction.abort()
            raise
        else:
            return cal_event

    def update_cal_event(self, uid, **kwargs):
        return super(CalEventAccessor, self)._update_record(uid, **kwargs)

    def increase_duration(self, uid, end_timedelta):
        """
        Event has changed in duration.

        :param uid:
        :param end_timedelta:
        """
        LOG.debug("increase_duration: {uid!r}".format(uid=uid))
        event = self._get_record(uid)
        try:
            LOG.debug("before: [{event.event_start}, {event.event_end}]"
                      .format(event=event))
            event.event_end += end_timedelta
            LOG.debug("after:  [{event.event_start}, {event.event_end}]"
                      .format(event=event))
            transaction.commit()
        except:
            transaction.abort()
            raise

    def divide_event(self, uid, days):
        """
        Divide the event and insert a new event for each extra day.

        :param uid: clendar event's UID.
        :type uid: int

        :param days: number of days
        :type days: int
        """
        event = self._get_record(uid)

        def divide(day):
            timedelta = datetime.timedelta(days=day + 1)
            new_event_start = event.event_start + timedelta
            new_event_end = event.event_end + timedelta
            new_event = CalEvent(new_event_start, new_event_end, event.comment)
            new_event.employee_uid = event.employee_uid
            new_event.order_phase = event.order_phase
            return new_event

        try:
            event_list = map(divide, xrange(days))
            self.session.add_all(event_list)
            transaction.commit()
        except:
            transaction.abort()
            raise

    def move_datetime(self, uid, timedelta):
        """
        Event has moved to a different day/time.

        :param uid:
        :param timedelta:
        """
        LOG.debug("move_datetime: {uid!r}".format(uid=uid))
        record = self._get_record(uid)
        try:
            LOG.debug("before: [{record.event_start}, {record.event_end}]"
                      .format(record=record))
            record.event_start += timedelta
            record.event_end += timedelta
            LOG.debug("after:  [{record.event_start}, {record.event_end}]"
                      .format(record=record))
            transaction.commit()
        except:
            transaction.abort()
            raise

    def delete_cal_event(self, uid):
        LOG.debug("delete_cal_event: {uid!r}"
                  .format(uid=uid))
        return self._delete_record(uid)
