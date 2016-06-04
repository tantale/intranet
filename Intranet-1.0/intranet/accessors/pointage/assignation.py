# -*- coding: utf-8 -*-
"""
assignation
=============

Date: 2016-02-23

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
import datetime
import logging
import math

import sqlalchemy.exc
import transaction

from intranet.accessors import BasicAccessor
from intranet.model import Assignation
from intranet.model.planning.calendar import Calendar
from intranet.model.planning.planning_event import PlanningEvent
from intranet.model.pointage.employee import Employee
from intranet.model.pointage.order import Order
from intranet.model.pointage.order_phase import OrderPhase

LOG = logging.getLogger(__name__)


class AssignationAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(AssignationAccessor, self).__init__(Assignation, session=session)

    def get_assignation(self, uid):
        """
        Get a assignation by UID.

        :type uid: int | str | unicode
        :param uid: Assignation UID.
        :rtype: Assignation
        :return: The matching assignation.
        :raise sqlalchemy.orm.exc.NoResultFound: if the record is not found.
        """
        return super(AssignationAccessor, self)._get_record(uid)

    def insert_assignation(self, employee_uid, order_phase_uid, assigned_hours, rate_percent,
                           start_date_utc, end_date_utc):
        """
        Assign a employee to a task (order phase).

        :type employee_uid: int
        :param employee_uid: Selected employee UID.
        :type order_phase_uid: int
        :param order_phase_uid: Current Task UID.
        :type assigned_hours: float
        :param assigned_hours: Number of estimated work hours assigned to the employee to accomplish this task.
        :type rate_percent: float
        :param rate_percent: Current rate: 0.005 <= rate_percent <= 1.0
        :type start_date_utc: datetime.datetime
        :param start_date_utc: Start date UTC.
        :type end_date_utc: datetime.datetime or None
        :param end_date_utc: End date UTC.
        :raise sqlalchemy.exc.IntegrityError: If an error occurs.
        """
        try:
            with transaction.manager:
                assignation = Assignation(assigned_hours, rate_percent, start_date_utc, end_date_utc)
                assignation.employee_uid = employee_uid
                assignation.order_phase_uid = order_phase_uid
                self.session.add(assignation)
        except sqlalchemy.exc.IntegrityError:
            transaction.abort()
            raise

    def update_assignation(self, uid, assigned_hours, rate_percent, start_date_utc, end_date_utc):
        """
        Update the assignation of an employee.

        :type uid: int | str | unicode
        :param uid: Assignation UID.
        :type assigned_hours: float
        :param assigned_hours: Number of estimated work hours assigned to the employee to accomplish this task.
        :type rate_percent: float
        :param rate_percent: Current rate: 0.005 <= rate_percent <= 1.0
        :type start_date_utc: datetime.datetime
        :param start_date_utc: Start date UTC.
        :type end_date_utc: datetime.datetime
        :param end_date_utc: End date UTC.
        :raise sqlalchemy.exc.IntegrityError: If an error occurs.
        """
        try:
            super(AssignationAccessor, self)._update_record(uid,
                                                            assigned_hours=assigned_hours,
                                                            rate_percent=rate_percent,
                                                            start_date=start_date_utc,
                                                            end_date=end_date_utc)
        except sqlalchemy.exc.IntegrityError:
            transaction.abort()
            raise

    def delete_assignation(self, assignation_uid):
        super(AssignationAccessor, self)._delete_record(assignation_uid)

    def plan_assignation(self, assignation_uid, tz_delta, minutes=15, max_months=4):
        try:
            with transaction.manager:
                assignation = self.get_assignation(assignation_uid)
                return assignation.plan_assignation(tz_delta, minutes, max_months)
        except sqlalchemy.exc.IntegrityError:
            transaction.abort()
            raise
