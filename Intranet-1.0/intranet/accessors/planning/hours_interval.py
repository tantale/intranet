# -*- coding: utf-8 -*-
"""
HoursInterval accessor
======================

Date: 2015-07-14

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

import datetime

import sqlalchemy.exc
import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.model.planning.hours_interval import HoursInterval
from intranet.model.planning.week_day import WeekDay

try:
    _("")
except TypeError:
    def _(x):
        return x


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

    def setup(self, week_hours_uid):
        # -- default hours intervals of the week (in local time)
        wh_dict = {1: [None,
                       (datetime.time(14, 0), datetime.time(17, 45))],
                   2: [(datetime.time(8, 30), datetime.time(12, 30)),
                       (datetime.time(14, 0), datetime.time(17, 45))],
                   3: [(datetime.time(8, 30), datetime.time(12, 30)),
                       (datetime.time(14, 0), datetime.time(17, 45))],
                   4: [(datetime.time(8, 30), datetime.time(12, 30)),
                       (datetime.time(14, 0), datetime.time(17, 45))],
                   5: [(datetime.time(8, 30), datetime.time(12, 30)),
                       (datetime.time(14, 0), datetime.time(17, 30))],
                   6: [(datetime.time(8, 30), datetime.time(12, 30)),
                       None],
                   7: []}
        try:
            with transaction.manager:
                week_hours = self.week_hours_accessor.get_week_hours(week_hours_uid)
                week_days = {wd.iso_weekday: wd for wd in self.get_week_day_list()}
                day_periods = {dp.position: dp for dp in week_hours.day_period_list}
                for weekday, periods in wh_dict.iteritems():
                    for position, interval in enumerate(periods, 1):
                        if interval:
                            self.insert_hours_interval(week_days[weekday].uid,
                                                       day_periods[position].uid,
                                                       start_hour=interval[0],
                                                       end_hour=interval[1])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()  # abort() is required here, why?...

    def get_hours_interval(self, week_day_uid, day_period_uid):
        """
        Get a hours_interval given its UID.

        :param week_day_uid:
        :param day_period_uid:
        :rtype: HoursInterval
        :return: The HoursInterval.
        """
        uid = (week_day_uid, day_period_uid)
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

    def get_hours_interval_table(self, week_hours_uid):
        week_day_list = self.get_week_day_list(order_by_cond=WeekDay.iso_weekday)
        week_hours = self.week_hours_accessor.get_week_hours(week_hours_uid)
        return week_hours.get_hours_interval_table(week_day_list)

    def insert_hours_interval(self, week_day_uid, day_period_uid, start_hour, end_hour):
        with transaction.manager:
            hours_interval = HoursInterval(start_hour, end_hour)
            hours_interval.week_day_uid = week_day_uid
            hours_interval.day_period_uid = day_period_uid
            self.session.add(hours_interval)

    def update_hours_interval(self, week_day_uid, day_period_uid, **kwargs):
        """
        Update the fields of a given record.

        :param week_day_uid: Hours interval composite UID.
        :param day_period_uid: Hours interval composite UID.
        :param kwargs: keywords arguments: "position", "label", "description".
        :rtype: HoursInterval
        :return: The updated HoursInterval.
        """
        uid = week_day_uid, day_period_uid
        return super(HoursIntervalAccessor, self)._update_record(uid, **kwargs)

    def delete_hours_interval(self, week_day_uid, day_period_uid):
        """
        Delete the hours_interval.

        :param week_day_uid: Hours interval composite UID.
        :param day_period_uid: Hours interval composite UID.
        :rtype: HoursInterval
        :return: The old HoursInterval.
        """
        uid = week_day_uid, day_period_uid
        return super(HoursIntervalAccessor, self)._delete_record(uid)

    def edit_hours_interval(self, week_day_uid, day_period_uid, start_hour, end_hour):
        """
        Edit the hour interval in-place.

        :param week_day_uid: Hours interval composite UID.
        :param day_period_uid: Hours interval composite UID.
        :param start_hour: start hour.
        :param end_hour: end hour.
        :return: Status of the edition: "updated", "deleted", "inserted" or "ignored".
        """
        uid = int(week_day_uid), int(day_period_uid)
        record = self.session.query(self.record_class).get(uid)
        if record:
            if start_hour and end_hour:
                self._update_record(uid, start_hour=start_hour, end_hour=end_hour)
                return dict(status=u'updated', start_hour=start_hour.isoformat(), end_hour=end_hour.isoformat())
            else:
                self._delete_record(uid)
                return dict(status=u'deleted')
        else:
            if start_hour and end_hour:
                self.insert_hours_interval(week_day_uid, day_period_uid, start_hour, end_hour)
                return dict(status=u'inserted', start_hour=start_hour.isoformat(), end_hour=end_hour.isoformat())
            else:
                return dict(status=u'ignored')
