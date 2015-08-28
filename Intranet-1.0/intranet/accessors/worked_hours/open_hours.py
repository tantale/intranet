# -*- coding: utf-8 -*-
"""
open_hours_accessor
===================

Date: 2015-08-28

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.accessors.worked_hours.week_hours import WeekHoursAccessor
from intranet.model.worked_hours.open_hours import OpenHours

try:
    _("")
except TypeError:
    _ = lambda x: x


class OpenHoursAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(OpenHoursAccessor, self).__init__(OpenHours, session=session)
        self.week_hours_accessor = WeekHoursAccessor(session)

    def setup(self):
        pass

    def get_week_hours(self, week_hours_uid):
        return self.week_hours_accessor.get_week_hours(week_hours_uid)

    def get_open_hours(self, uid):
        """
        Get a open_hours given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: OpenHours
        :return: The OpenHours.
        """
        return super(OpenHoursAccessor, self)._get_record(uid)

    def get_by_label(self, label):
        self.session.query(OpenHours).filter(OpenHours.label == label).one()

    def get_open_hours_list(self, filter_cond=None, order_by_cond=None):
        """
        Get a filtered the list of open hourss.

        :param filter_cond: SQL Alchemy filter predicate.
        :param order_by_cond: SQL Alchemy Order-by condition.
        :rtype: list[OpenHours]
        :return: list of open hourss.
        """
        return self._get_record_list(filter_cond=filter_cond, order_by_cond=order_by_cond)

    def insert_open_hours(self, week_hours_uid, label, description):
        """
        Append a hours of the open.

        :param week_hours_uid: UID of the week hours.
        :type label: unicode
        :param label: Display name => used in selection.
        :type description: unicode
        :param description: Description => used in tooltip.
        """
        with transaction.manager:
            week_hours = self.get_week_hours(week_hours_uid)
            open_hours = OpenHours(label, description)
            open_hours.week_hours = week_hours
            self.session.add(open_hours)

    def update_open_hours(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :param kwargs: keywords arguments: "position", "label", "description".
        :rtype: OpenHours
        :return: The updated OpenHours.
        """
        return super(OpenHoursAccessor, self)._update_record(uid, **kwargs)

    def delete_open_hours(self, uid):
        """
        Delete the open_hours.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: OpenHours
        :return: The old OpenHours.
        """
        return super(OpenHoursAccessor, self)._delete_record(uid)
