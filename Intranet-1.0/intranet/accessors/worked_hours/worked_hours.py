# -*- coding: utf-8 -*-
"""
worked_hours_accessor
=====================

Date: 2015-08-28

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.accessors.worked_hours.week_hours import WeekHoursAccessor
from intranet.model.worked_hours.worked_hours import WorkedHours

try:
    _("")
except TypeError:
    _ = lambda x: x


class WorkedHoursAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(WorkedHoursAccessor, self).__init__(WorkedHours, session=session)
        self.week_hours_accessor = WeekHoursAccessor(session)

    def setup(self):
        pass

    def get_week_hours(self, week_hours_uid):
        return self.week_hours_accessor.get_week_hours(week_hours_uid)

    def get_worked_hours(self, uid):
        """
        Get a worked_hours given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: WorkedHours
        :return: The OpenHours.
        """
        return super(WorkedHoursAccessor, self)._get_record(uid)

    def get_by_label(self, label):
        return self.session.query(WorkedHours).filter(WorkedHours.label == label).one()

    def get_worked_hours_list(self, filter_cond=None, order_by_cond=None):
        """
        Get a filtered the list of open hourss.

        :param filter_cond: SQL Alchemy filter predicate.
        :param order_by_cond: SQL Alchemy Order-by condition.
        :rtype: list[WorkedHours]
        :return: list of open hourss.
        """
        return self._get_record_list(filter_cond=filter_cond, order_by_cond=order_by_cond)

    def insert_worked_hours(self, position, week_hours_uid, label, description):
        """
        Append a hours of the open.

        :type position: int
        :param position: Relative position.
        :param week_hours_uid: UID of the week hours.
        :type label: unicode
        :param label: Display name => used in selection.
        :type description: unicode
        :param description: Description => used in tooltip.
        """
        with transaction.manager:
            week_hours = self.get_week_hours(week_hours_uid)
            worked_hours = WorkedHours(position, label, description)
            worked_hours.week_hours = week_hours
            self.session.add(worked_hours)

    def update_worked_hours(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :param kwargs: keywords arguments: "position", "label", "description".
        :rtype: WorkedHours
        :return: The updated OpenHours.
        """
        return super(WorkedHoursAccessor, self)._update_record(uid, **kwargs)

    def delete_worked_hours(self, uid):
        """
        Delete the worked_hours.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: WorkedHours
        :return: The old OpenHours.
        """
        return super(WorkedHoursAccessor, self)._delete_record(uid)
