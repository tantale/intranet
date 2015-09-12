# -*- coding: utf-8 -*-
"""
calendar_accessor
=====================

Date: 2015-08-28

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

import sqlalchemy.exc
from sqlalchemy.sql.functions import func
import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor, LOG
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.pointage.order_cat import OrderCatAccessor
from intranet.model.planning.calendar import Calendar

try:
    _("")
except TypeError:
    _ = lambda x: x


def convert_value(field, value):
    converters = dict(position=int,
                      label=unicode,
                      description=unicode,
                      week_hours_uid=int,
                      employee_uid=int,
                      background_color=unicode,
                      border_color=unicode,
                      text_color=unicode,
                      class_name=unicode)
    defaults = dict(position=1,
                    label=None,
                    description=None,
                    week_hours_uid=None,
                    employee_uid=None,
                    background_color=Calendar.BACKGROUND_COLOR,
                    border_color=Calendar.BORDER_COLOR,
                    text_color=Calendar.TEXT_COLOR,
                    class_name=None)
    return converters[field](value) if value else defaults[field]


class CalendarAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(CalendarAccessor, self).__init__(Calendar, session=session)
        self.week_hours_accessor = WeekHoursAccessor(session)
        self.employee_accessor = EmployeeAccessor(session)
        self.order_cat_accessor = OrderCatAccessor(session)

    def setup(self, week_hours_uid):
        LOG.info(u"Setup the default calendar...")
        try:
            with transaction.manager:
                week_hours = self.week_hours_accessor.get_week_hours(week_hours_uid)
                week_hours.calendar_list.extend([
                    Calendar(1, _(u"Calendrier principal"), _(u"Calendrier principal commun à toute de l’entreprise"))
                ])
        except sqlalchemy.exc.IntegrityError as exc:
            LOG.warning(exc)
            # setup already done.
            transaction.abort()

    def get_week_hours(self, week_hours_uid):
        return self.week_hours_accessor.get_week_hours(week_hours_uid)

    def get_week_hours_list(self, filter_cond=None, order_by_cond=None):
        return self.week_hours_accessor.get_week_hours_list(filter_cond=filter_cond, order_by_cond=order_by_cond)

    def get_employee(self, employee_uid):
        return self.employee_accessor.get_employee(employee_uid)

    def get_employee_list(self, filter_cond=None, order_by_cond=None):
        return self.employee_accessor.get_employee_list(filter_cond=filter_cond, order_by_cond=order_by_cond)

    def get_calendar(self, uid):
        """
        Get a calendar given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: Calendar
        :return: The OpenHours.
        """
        return super(CalendarAccessor, self)._get_record(uid)

    def get_by_label(self, label):
        return self.session.query(Calendar).filter(Calendar.label == label).one()

    def get_calendar_list(self, filter_cond=None, order_by_cond=None):
        """
        Get a filtered the list of worked hours.

        :param filter_cond: SQL Alchemy filter predicate.
        :param order_by_cond: SQL Alchemy Order-by condition.
        :rtype: list[Calendar]
        :return: list of worked hours.
        """
        return self._get_record_list(filter_cond=filter_cond, order_by_cond=order_by_cond)

    def insert_calendar(self, week_hours_uid, label, description, employee_uid=None,
                        background_color=None, border_color=None, text_color=None, class_name=None):
        """
        Append worked hours.

        :param week_hours_uid: UID of the week hours.
        :type label: unicode
        :param label: Display name => used in selection.
        :type description: unicode
        :param description: Description => used in tooltip.
        """
        week_hours_uid = convert_value("week_hours_uid", week_hours_uid)
        label = convert_value("label", label)
        description = convert_value("description", description)
        employee_uid = convert_value("employee_uid", employee_uid)
        background_color = convert_value("background_color", background_color)
        border_color = convert_value("border_color", border_color)
        text_color = convert_value("text_color", text_color)
        class_name = convert_value("class_name", class_name)
        with transaction.manager:
            last_position = self.session.query(func.max(Calendar.position)).scalar() or 0
            calendar = Calendar(last_position + 1, label, description,
                                background_color, border_color, text_color, class_name)
            calendar.week_hours_uid = week_hours_uid
            calendar.employee_uid = employee_uid
            self.session.add(calendar)

    def update_calendar(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :param kwargs: keywords arguments: "position", "label", "description".
        :rtype: Calendar
        :return: The updated OpenHours.
        """
        kwargs = {key: convert_value(key, value) for key, value in kwargs.iteritems()}
        return super(CalendarAccessor, self)._update_record(uid, **kwargs)

    def delete_calendar(self, uid):
        """
        Delete the calendar.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: Calendar
        :return: The old OpenHours.
        """
        return super(CalendarAccessor, self)._delete_record(uid)
