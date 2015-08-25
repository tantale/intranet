# -*- coding: utf-8 -*-
"""
HoursInterval accessor
======================

Date: 2015-07-14

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals
import datetime

import transaction

from tg.i18n import ugettext as _
import sqlalchemy.exc

from intranet.accessors.worked_hours.day_period import DayPeriodAccessor
from intranet.accessors.worked_hours.week_day import WeekDayAccessor
from intranet.accessors import BasicAccessor
from intranet.accessors.worked_hours.week_hours import WeekHoursAccessor
from intranet.model.worked_hours.day_period import DayPeriod
from intranet.model.worked_hours.hours_interval import HoursInterval
from intranet.model.worked_hours.week_day import WeekDay
from intranet.model.worked_hours.week_hours import WeekHours

try:
    _("")
except TypeError:
    _ = lambda x: x


class HoursIntervalAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(HoursIntervalAccessor, self).__init__(HoursInterval, session=session)
        self.week_hours_accessor = WeekHoursAccessor(session)
        self.day_period_accessor = DayPeriodAccessor(session)
        self.week_day_accessor = WeekDayAccessor(session)

    def get_week_hours_list(self, filter_cond=None, order_by_cond=None):
        return self.week_hours_accessor.get_week_hours_list(filter_cond, order_by_cond)

    def get_day_period_list(self, filter_cond=None, order_by_cond=None):
        return self.day_period_accessor.get_day_period_list(filter_cond, order_by_cond)

    def get_week_day_list(self, filter_cond=None, order_by_cond=None):
        return self.week_day_accessor.get_week_day_list(filter_cond, order_by_cond)

    def setup(self):
        # -- default hours intervals of the week (in local time)
        wh_dict = {1: [None,
                       (datetime.time(13, 30), datetime.time(17, 45))],
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
        try:
            with transaction.manager:
                week_hours = self.get_week_hours_list()[0]
                week_days = {wd.weekday: wd for wd in self.get_week_day_list()}
                day_periods = {dp.position: dp for dp in self.get_day_period_list(DayPeriod.week_hours == week_hours)}
                for weekday, periods in wh_dict.iteritems():
                    for position, interval in enumerate(periods, 1):
                        if interval:
                            self.insert_hours_interval(week_hours,
                                                       week_days[weekday],
                                                       day_periods[position],
                                                       start_hour=interval[0],
                                                       end_hour=interval[1])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()  # abort() is required here, why?...

    def get_hours_interval(self, week_hours_uid, week_day_uid, day_period_uid):
        """
        Get a hours_interval given its UID.

        :rtype: HoursInterval
        :return: The HoursInterval.
        """
        uid = (week_hours_uid, week_day_uid, day_period_uid)
        return super(HoursIntervalAccessor, self)._get_record(uid)

    def get_hours_interval_list(self, filter_cond=None, order_by_cond=None):
        """
        Get a filtered the list of day periods.

        :param filter_cond: SQL Alchemy filter predicate.
        :param order_by_cond: SQL Alchemy Order-by condition.
        :rtype: list[HoursInterval]
        :return: list of day periods.
        """
        return self._get_record_list(filter_cond=filter_cond, order_by_cond=order_by_cond)

    def get_hours_interval_table(self, week_hours):
        indexed_intervals = {(i.week_day_uid, i.day_period_uid): i
                             for i in self.get_hours_interval_list(WeekHours.uid == week_hours.uid)}
        return [[indexed_intervals.get((week_day.uid, day_period.uid))
                 for day_period in self.get_day_period_list(DayPeriod.week_hours == week_hours,
                                                            order_by_cond=DayPeriod.position)]
                for week_day in self.get_week_day_list(order_by_cond=WeekDay.weekday)]

    def insert_hours_interval(self, week_hours, week_day, day_period, start_hour, end_hour):
        with transaction.manager:
            hours_interval = HoursInterval(start_hour, end_hour)
            hours_interval.week_hours = week_hours
            hours_interval.week_day = week_day
            hours_interval.day_period = day_period
            self.session.add(hours_interval)

    def update_hours_interval(self, week_hours_uid, week_day_uid, day_period_uid, **kwargs):
        """
        Update the fields of a given record.

        :param kwargs: keywords arguments: "position", "label", "description".
        :rtype: HoursInterval
        :return: The updated HoursInterval.
        """
        uid = week_hours_uid, week_day_uid, day_period_uid
        return super(HoursIntervalAccessor, self)._update_record(uid, **kwargs)

    def delete_hours_interval(self, week_hours_uid, week_day_uid, day_period_uid):
        """
        Delete the hours_interval.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: HoursInterval
        :return: The old HoursInterval.
        """
        uid = week_hours_uid, week_day_uid, day_period_uid
        return super(HoursIntervalAccessor, self)._delete_record(uid)
