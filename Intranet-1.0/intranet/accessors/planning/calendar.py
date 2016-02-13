# -*- coding: utf-8 -*-
"""
calendar_accessor
=====================

Date: 2015-08-28

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

import sqlalchemy.exc
import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor, LOG
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.pointage.order_cat import OrderCatAccessor
from intranet.accessors.positioning import calc_places
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
                      background_color=unicode,
                      border_color=unicode,
                      text_color=unicode,
                      class_name=unicode)
    defaults = dict(position=1,
                    label=None,
                    description=None,
                    week_hours_uid=None,
                    background_color=Calendar.BACKGROUND_COLOR,
                    border_color=Calendar.BORDER_COLOR,
                    text_color=Calendar.TEXT_COLOR,
                    class_name=None)
    return converters[field](value) if value else defaults[field]


class CalendarAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(CalendarAccessor, self).__init__(Calendar, session=session)
        self.week_hours_accessor = WeekHoursAccessor(session)
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
        """
        Get a calendar by label, raise an exception if missing.

        :type label: unicode
        :param label: Calendar label to search for in the database.
        :rtype: Calendar
        :return: The matching calendar.
        """
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

    def insert_calendar(self, week_hours_uid, label, description,
                        background_color=None, border_color=None, text_color=None, class_name=None):
        """
        Append worked hours.

        :param week_hours_uid: UID of the week hours.
        :type label: unicode
        :param label: Display name => used in selection.
        :type description: unicode
        :param description: Description => used in tooltip.
        :param background_color: Event's background color (if any)
        :param border_color: Event's border color (if any)
        :param text_color: Event's text color (if any)
        :param class_name: Event's CSS class name (if any), see: project's category ``project_cat``.
        """
        week_hours_uid = convert_value("week_hours_uid", week_hours_uid)
        label = convert_value("label", label)
        description = convert_value("description", description)
        background_color = convert_value("background_color", background_color)
        border_color = convert_value("border_color", border_color)
        text_color = convert_value("text_color", text_color)
        class_name = convert_value("class_name", class_name)
        calendar = Calendar(0, label, description,
                            background_color, border_color, text_color, class_name)
        calendar.week_hours_uid = week_hours_uid
        self.insert_calendar_after(None, calendar)

    def insert_calendar_after(self, position, calendar, *calendars):
        records = [calendar] + list(calendars)
        existing = self.session.query(Calendar).order_by(Calendar.position).all()
        places = calc_places([e.position for e in existing], position, len(records))
        with transaction.manager:
            for place, record in zip(places, records):
                record.position = place
                self.session.add(record)

    def update_calendar(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :type uid: int or str or unicode
        :param uid: UID of the record.
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
