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
from intranet.accessors.worked_hours.frequency import FrequencyAccessor
from intranet.accessors.worked_hours.week_hours import WeekHoursAccessor
from intranet.accessors.worked_hours.open_hours import OpenHoursAccessor
from intranet.model.worked_hours.year_period import YearPeriod

try:
    _("")
except TypeError:
    _ = lambda x: x


class YearPeriodAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(YearPeriodAccessor, self).__init__(YearPeriod, session=session)
        self.open_hours_accessor = OpenHoursAccessor(session)
        self.week_hours_accessor = WeekHoursAccessor(session)
        self.frequency_accessor = FrequencyAccessor(session)

    def setup(self):
        pass

    def get_open_hours(self, open_hours_uid):
        return self.open_hours_accessor.get_open_hours(open_hours_uid)

    def get_week_hours(self, week_hours_uid):
        return self.week_hours_accessor.get_week_hours(week_hours_uid)

    def get_frequency(self, frequency_uid):
        return self.frequency_accessor.get_frequency(frequency_uid)

    def get_year_period(self, uid):
        """
        Get a day_period given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: YearPeriod
        :return: The YearPeriod.
        """
        return super(YearPeriodAccessor, self)._get_record(uid)

    def get_day_period_list(self, filter_cond=None, order_by_cond=None):
        """
        Get a filtered the list of day periods.

        :param filter_cond: SQL Alchemy filter predicate.
        :param order_by_cond: SQL Alchemy Order-by condition.
        :rtype: list[YearPeriod]
        :return: list of day periods.
        """
        return self._get_record_list(filter_cond=filter_cond, order_by_cond=order_by_cond)

    def insert_day_period(self, open_hours_uid, week_hours_uid, frequency_uid, start_date, end_date):
        """
        Append a period of the year.

        :param open_hours_uid: UID of the open hours (parent).
        :param week_hours_uid: UID of the week hours.
        :param frequency_uid: UID of the frequency to append.
        :rtype: YearPeriod
        """
        with transaction.manager:
            open_hours = self.get_open_hours(open_hours_uid)
            week_hours = self.get_week_hours(week_hours_uid)
            frequency = self.get_frequency(frequency_uid)
            year_period = YearPeriod(start_date, end_date)
            year_period.open_hours = open_hours
            year_period.week_hours = week_hours
            year_period.frequency = frequency
            self.session.add(year_period)

    def update_day_period(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :param kwargs: keywords arguments: "position", "label", "description".
        :rtype: YearPeriod
        :return: The updated YearPeriod.
        """
        return super(YearPeriodAccessor, self)._update_record(uid, **kwargs)

    def delete_day_period(self, uid):
        """
        Delete the day_period.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: YearPeriod
        :return: The old YearPeriod.
        """
        return super(YearPeriodAccessor, self)._delete_record(uid)
