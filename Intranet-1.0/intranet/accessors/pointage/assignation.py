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
                return self._plan_assignation_transaction(assignation_uid, tz_delta, minutes, max_months)
        except sqlalchemy.exc.IntegrityError:
            transaction.abort()
            raise

    def _plan_assignation_transaction(self, assignation_uid, tz_delta, minutes, max_months):
        assignation = self.get_assignation(assignation_uid)

        # -- Pour rechercher un intervalle de temps qui correspond,
        #    nous allons majorer la durée assigned_hours par le taux rate_percent
        assigned_hours = assignation.assigned_hours
        required_hours = assigned_hours / assignation.rate_percent

        # -- Le plus petit intervalle de temps est de 15 minutes,
        #    il faut donc arrondir la durée en heures à 15 minutes près par excès.
        required_minutes = math.ceil(required_hours * 60.0 / minutes) * minutes

        # -- Si la date de fin n'est pas défini, on fera une exploration sur 4 mois
        #    Les dates sont exprimées en date/heures UTC.
        start_date_utc = assignation.start_date
        end_date_utc = assignation.end_date or (start_date_utc + datetime.timedelta(days=max_months * 30.5))

        # -- Attention, les calculs se font sur des dates/heures locales (et non pas UTC).
        start_date = start_date_utc - tz_delta
        end_date = end_date_utc - tz_delta

        # -- La recherche d'un intervalle se fait sur les heures de disponibilité de l'employé.
        #    Le calendrier est celui associé à l'employé.
        calendar = assignation.employee.calendar
        assert isinstance(calendar, Calendar)

        # -- La recherche d'un intervalle se fait jour après jour.
        nbr_days = (end_date - start_date).days
        for days in xrange(nbr_days):
            curr_date = (start_date + datetime.timedelta(days=days)).date()

            # -- Il nous faut trouver un intervalle de dates dont la durée soit supérieure (ou égale)
            #    à la durée de la tâche.
            intervals = calendar.get_available_intervals(curr_date, tz_delta, minutes=minutes)
            for start, end in intervals:
                event_start = datetime.datetime.combine(curr_date, start)
                event_end = datetime.datetime.combine(curr_date, end)
                duration = event_end - event_start
                total_minutes = duration.total_seconds() / 60.0
                if required_minutes <= total_minutes:
                    # -- OK, on a trouvé un intervalle assez large.
                    #    On peut plannifier la tâche avec la durée assignée (sans taux rate_percent).
                    event_end = event_start + datetime.timedelta(hours=assigned_hours)
                    return self._append_planning_event(assignation, event_start, event_end, tz_delta)

        # todo: segmentation de la durée en portions plus petites

        return None  # fixme: planification impossible => raise

    def _append_planning_event(self, assignation, event_start, event_end, tz_delta):
        # Les dates de planification sont en dates/heures UTC.
        event_start_utc = event_start + tz_delta
        event_end_utc = event_end + tz_delta

        # Nous construisons un évènement à partir des dates et des propriétés de la tâche.
        order_phase = assignation.order_phase
        order = order_phase.order
        fmt = u"{order_uid} – {order_ref}\xa0: {label}"
        label = fmt.format(order_uid=order.uid, order_ref=order.order_ref, label=order_phase.label)
        planning_event = PlanningEvent(label=label,
                                       description=order_phase.description,
                                       event_start=event_start_utc,
                                       event_end=event_end_utc)
        planning_event.calendar = assignation.employee.calendar
        assignation.planning_event_list.append(planning_event)

        # On retourne les dates (heures locale) pour affichage dans le formulaire
        return [event_start, event_end]
