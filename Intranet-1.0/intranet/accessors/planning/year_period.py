# -*- coding: utf-8 -*-
"""
year_period_accessor
===================

Date: 2015-08-28

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.frequency import FrequencyAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.model.planning.year_period import YearPeriod

try:
    _("")
except TypeError:
    def _(x):
        return x


class YearPeriodAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(YearPeriodAccessor, self).__init__(YearPeriod, session=session)
        self.calendar_accessor = CalendarAccessor(session)
        self.week_hours_accessor = WeekHoursAccessor(session)
        self.frequency_accessor = FrequencyAccessor(session)

    def setup(self):
        pass

    def get_calendar(self, calendar_uid):
        return self.calendar_accessor.get_calendar(calendar_uid)

    def get_week_hours(self, week_hours_uid):
        return self.week_hours_accessor.get_week_hours(week_hours_uid)

    def get_frequency(self, frequency_uid):
        return self.frequency_accessor.get_frequency(frequency_uid)

    def get_year_period(self, uid):
        """
        Get a year_period given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: YearPeriod
        :return: The YearPeriod.
        """
        return super(YearPeriodAccessor, self)._get_record(uid)

    def get_year_period_list(self, filter_cond=None, order_by_cond=None):
        """
        Get a filtered the list of year periods.

        :param filter_cond: SQL Alchemy filter predicate.
        :param order_by_cond: SQL Alchemy Order-by condition.
        :rtype: list[YearPeriod]
        :return: list of year periods.
        """
        return self._get_record_list(filter_cond=filter_cond, order_by_cond=order_by_cond)

    def insert_year_period(self, calendar_uid, week_hours_uid, frequency_uid, start_date, end_date):
        """
        Append a period of the year.

        :type start_date: datetime.date
        :param start_date: Start date of the period (local time).
        :type end_date: datetime.date
        :param end_date: End date of the period (local time).
        :param calendar_uid: UID of the calendar (parent).
        :param week_hours_uid: UID of the week hours.
        :param frequency_uid: UID of the frequency to append.
        :rtype: YearPeriod
        """
        with transaction.manager:
            year_period = YearPeriod(start_date, end_date)
            year_period.calendar_uid = calendar_uid
            year_period.week_hours_uid = week_hours_uid
            year_period.frequency_uid = frequency_uid
            self.session.add(year_period)

    def update_year_period(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :param kwargs: keywords arguments: "position", "label", "description".
        :rtype: YearPeriod
        :return: The updated YearPeriod.
        """
        return super(YearPeriodAccessor, self)._update_record(uid, **kwargs)

    def delete_year_period(self, uid):
        """
        Delete the year_period.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: YearPeriod
        :return: The old YearPeriod.
        """
        return super(YearPeriodAccessor, self)._delete_record(uid)
