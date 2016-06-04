# -*- coding: utf-8 -*-
"""
Assignation
=============

Date: 2016-01-18

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

import datetime

from babel.dates import format_date
from babel.numbers import format_percent
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.types import Integer, DateTime, Float

from intranet.model import DeclarativeBase
from intranet.model.planning.calendar import Calendar
from intranet.model.planning.planning_event import PlanningEvent


class Assignation(DeclarativeBase):
    """
    Assign an Employee to an OrderPhase with the given rate (percent)
    """
    __tablename__ = 'Assignation'
    __table_args__ = (UniqueConstraint('employee_uid', 'order_phase_uid',
                                       name="order_phase_employee_unique"),
                      CheckConstraint("0.0 <= assigned_hours",
                                      name="assigned_hours_check"),
                      CheckConstraint("0.0 <= rate_percent AND rate_percent <= 1.0",
                                      name="rate_interval_check"),
                      CheckConstraint("end_date IS NULL OR (start_date <= end_date)",
                                      name="date_interval_check"),
                      {'mysql_engine': 'InnoDB'})

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    employee_uid = Column(Integer, ForeignKey('Employee.uid',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                          nullable=True, index=True)
    order_phase_uid = Column(Integer, ForeignKey('OrderPhase.uid',
                                                 ondelete='CASCADE',
                                                 onupdate='CASCADE'),
                             nullable=True, index=True)
    assigned_hours = Column(Float, nullable=False)
    rate_percent = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    employee = relationship('Employee', back_populates='assignation_list')
    order_phase = relationship('OrderPhase', back_populates='assignation_list')
    planning_event_list = relationship('PlanningEvent',
                                       back_populates="assignation",
                                       cascade='all,delete-orphan')

    def __init__(self, assigned_hours, rate_percent, start_date=None, end_date=None):
        self.assigned_hours = assigned_hours
        self.rate_percent = rate_percent
        self.start_date = start_date
        self.end_date = end_date

    @property
    def total_duration(self):
        return sum(pe.event_duration for pe in self.planning_event_list) if self.planning_event_list else None

    @property
    def start_planning_date(self):
        return min(pe.event_start for pe in self.planning_event_list) if self.planning_event_list else None

    @property
    def end_planning_date(self):
        return max(pe.event_end for pe in self.planning_event_list) if self.planning_event_list else None

    def get_assignation(self, tz_offset, locale='fr_FR'):
        tz_delta = datetime.timedelta(minutes=int(tz_offset))
        start_date = (self.start_date - tz_delta).date()
        if self.end_date:
            end_date = (self.end_date - tz_delta).date()
            fmt = u'{employee.employee_name} assigné à {rate_percent} du {start_date} au {end_date}'
            return fmt.format(employee=self.employee,
                              rate_percent=format_percent(self.rate_percent, locale=locale),
                              start_date=format_date(start_date, format='short', locale=locale),
                              end_date=format_date(end_date, format='short', locale=locale))
        fmt = u'{employee.employee_name} assigné à {rate_percent} à partir du {start_date}'
        return fmt.format(employee=self.employee,
                          rate_percent=format_percent(self.rate_percent, locale=locale),
                          start_date=format_date(start_date, format='short', locale=locale))

    def append_planning_event(self, event_start, event_end, tz_delta):
        """
        Append a new event in the assignation planning.

        :type event_start: datetime.datetime
        :param event_start: Start date/time of the event (local time).
        :type event_end: datetime.datetime
        :param event_end: End date/time of the event (local time).
        :type tz_delta: datetime.timedelta
        :param tz_delta: time-zone delta from UTC (tz_delta = utc_date - local_date).
        """
        # Les dates de planification sont en dates/heures UTC.
        event_start_utc = event_start + tz_delta
        event_end_utc = event_end + tz_delta

        # Nous construisons un évènement à partir des dates et des propriétés de la tâche.
        order_phase = self.order_phase
        order = order_phase.order
        fmt = u"{order_uid} – {order_ref}\xa0: {label}"
        label = fmt.format(order_uid=order.uid, order_ref=order.order_ref, label=order_phase.label)
        planning_event = PlanningEvent(label=label,
                                       description=order_phase.description,
                                       event_start=event_start_utc,
                                       event_end=event_end_utc)
        planning_event.calendar = self.employee.calendar
        self.planning_event_list.append(planning_event)

    def plan_assignation(self, tz_delta, minutes=15, max_months=4):
        # -- Si la date de fin n'est pas défini, on fera une exploration sur 4 mois
        #    Les dates sont exprimées en date/heures UTC.
        start_date_utc = self.start_date
        end_date_utc = self.end_date or (start_date_utc + datetime.timedelta(days=max_months * 30.5))

        # -- Attention, les calculs se font sur des dates/heures locales (et non pas UTC).
        start_date = start_date_utc - tz_delta
        end_date = end_date_utc - tz_delta

        # -- La recherche d'un intervalle se fait sur les heures de disponibilité de l'employé.
        #    Le calendrier est celui associé à l'employé.
        calendar = self.employee.calendar
        isinstance(calendar, Calendar)

        # -- La recherche d'un intervalle se fait jour après jour.
        intervals = calendar.find_assignable_event(start_date, end_date, tz_delta,
                                                   self.assigned_hours, self.rate_percent, minutes=minutes)
        for interval in intervals:
            event_start, event_end = interval
            self.append_planning_event(event_start, event_end, tz_delta)
        return intervals
