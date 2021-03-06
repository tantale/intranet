# -*- coding: utf-8 -*-
"""
day_period_accessor
===================

Date: 2015-07-07

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

import sqlalchemy.exc
import transaction
from sqlalchemy import and_
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.model.planning.day_period import DayPeriod

try:
    _("")
except TypeError:
    def _(x):
        return x


class DayPeriodAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(DayPeriodAccessor, self).__init__(DayPeriod, session=session)
        self.week_hours_accessor = WeekHoursAccessor(session)

    def setup(self, week_hours_uid):
        try:
            with transaction.manager:
                week_hours = self.week_hours_accessor.get_week_hours(week_hours_uid)
                week_hours.day_period_list.extend([
                    DayPeriod(1, _(u"Matin"), _(u"Horaires du matin")),
                    DayPeriod(2, _(u"Après-midi"), _(u"Horaires de l’après-midi")),
                ])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()  # abort() is required here, why?...

    def get_week_hours(self, week_hours_uid):
        return self.week_hours_accessor.get_week_hours(week_hours_uid)

    def get_day_period(self, uid):
        """
        Get a day_period given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: DayPeriod
        :return: The DayPeriod.
        """
        return super(DayPeriodAccessor, self)._get_record(uid)

    def get_by_label(self, week_hours_uid, label):
        filter_cond = and_(DayPeriod.week_hours_uid == week_hours_uid, DayPeriod.label == label)
        return self.session.query(self.record_class).filter(filter_cond).one()

    def get_day_period_list(self, filter_cond=None, order_by_cond=None):
        """
        Get a filtered the list of day periods.

        :param filter_cond: SQL Alchemy filter predicate.
        :param order_by_cond: SQL Alchemy Order-by condition.
        :rtype: list[DayPeriod]
        :return: list of day periods.
        """
        return self._get_record_list(filter_cond=filter_cond, order_by_cond=order_by_cond)

    def insert_day_period(self, week_hours_uid, label, description=None):
        """
        Append a period of the day to the week hours' list of periods.

        :type week_hours_uid: int
        :param week_hours_uid: Week hours UID
        :type label: unicode
        :param label: Display name of the day => used in selection.
        :type description: unicode
        :param description: Description of the day => used in tooltip.
        :rtype: DayPeriod
        :return: The new DayPeriod.
        """
        description = description or _("Période de la journée : {label}").format(label=label)
        with transaction.manager:
            week_hours = self.get_week_hours(week_hours_uid)
            day_period_list = week_hours.day_period_list
            last_position = max(record.position for record in day_period_list) if day_period_list else 0
            day_period = DayPeriod(position=last_position + 1,
                                   label=label,
                                   description=description)
            week_hours.day_period_list.append(day_period)

    def update_day_period(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :param kwargs: keywords arguments: "position", "label", "description".
        :rtype: DayPeriod
        :return: The updated DayPeriod.
        """
        return super(DayPeriodAccessor, self)._update_record(uid, **kwargs)

    def delete_day_period(self, uid):
        """
        Delete the day_period.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: DayPeriod
        :return: The old DayPeriod.
        """
        return super(DayPeriodAccessor, self)._delete_record(uid)
