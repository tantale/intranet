# -*- coding: utf-8 -*-
"""
Planning calendar
=================

Module: intranet.model.calendar.calendar

Created on: 2015-08-28
"""
from __future__ import unicode_literals

import datetime
import math
import re

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, CheckConstraint
from sqlalchemy.types import Integer, String, Float

from intranet.accessors.gap_fill import GapFill
from intranet.accessors.time_slot import create_time_slot, FREE_SLOT, BUSY_SLOT, create_time_interval, EMPTY_SLOT
from intranet.model import DeclarativeBase

COLOR_REGEX = ur"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
match_color = re.compile(COLOR_REGEX).match


def checked_color(color):
    if color is None or match_color(color):
        return color
    raise ValueError(color)


class Calendar(DeclarativeBase):
    """
    Calendar management.

    .. versionchanged:: 2.2.0
       Add *planning_event_list* and *year_period_list* relationships.
    """
    __tablename__ = 'Calendar'

    __table_args__ = (CheckConstraint("position > 0", name="position_check"),)  # tuple

    #: Default Event colors: intranet/public/css/fullcalendar.css:264
    BACKGROUND_COLOR = "#3a87ad"
    BORDER_COLOR = "#3a87ad"
    TEXT_COLOR = "#ffffff"

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    position = Column(Float, unique=True, index=True, nullable=False)  # no duplicates
    label = Column(String(length=32), unique=True, nullable=False, index=True)  # no duplicates
    description = Column(String(length=200))

    background_color = Column(String(length=7), nullable=False, default=BACKGROUND_COLOR)
    border_color = Column(String(length=7), nullable=False, default=BORDER_COLOR)
    text_color = Column(String(length=7), nullable=False, default=TEXT_COLOR)
    class_name = Column(String(length=50), nullable=True)

    week_hours_uid = Column(Integer, ForeignKey('WeekHours.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            nullable=False, index=True)

    employee_uid = Column(Integer, ForeignKey('Employee.uid',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                          nullable=True, index=True)

    week_hours = relationship('WeekHours', back_populates='calendar_list')

    employee = relationship("Employee", back_populates="calendar")  # one-to-one

    planning_event_list = relationship('PlanningEvent',
                                       back_populates="calendar",
                                       cascade='all,delete-orphan')

    year_period_list = relationship('YearPeriod',
                                    back_populates="calendar",
                                    cascade='all,delete-orphan')

    def __init__(self, position, label, description,
                 background_color=BACKGROUND_COLOR, border_color=BORDER_COLOR, text_color=TEXT_COLOR, class_name=None):
        """
        Calendar, see: http://fullcalendar.io/docs/event_data/Event_Source_Object/

        :type position: int
        :param position: Relative position.
        :type label: unicode
        :param label: Display name => used in selection.
        :type description: unicode
        :param description: Description => used in tooltip.
        :param background_color: Event's background color (if any)
        :param border_color: Event's border color (if any)
        :param text_color: Event's text color (if any)
        :param class_name: Event's CSS class name (if any), see: project's category ``project_cat``.
        """
        self.position = position
        self.label = label
        self.description = description
        self.background_color = checked_color(background_color)
        self.border_color = checked_color(border_color)
        self.text_color = checked_color(text_color)
        self.class_name = class_name

    def event_source_obj(self):
        """
        http://fullcalendar.io/docs1/event_data/Event_Source_Object/

        :rtype: dict[str|unicode, unicode]
        :return: Event source object as a Python dictionary
        """
        dict_ = dict()
        # -- Standard fields
        dict_['id'] = ('{uid}'.format(uid=self.uid))
        if self.class_name:
            dict_['className'] = self.class_name
        else:
            dict_['backgroundColor'] = self.background_color
            dict_['borderColor'] = self.border_color
            dict_['textColor'] = self.text_color
        return dict_

    def select_week_hours(self, day):
        """
        Select the week hours matching the given day.
        First look in the year periods to find a matching day, then in the default week hours.

        .. versionadded:: 2.2.0

        :type day: datetime.date
        :param day: day date (local time)
        :rtype: intranet.model.planning.week_hours.WeekHours
        :return: The matching week hours instance, may return ``None`` if nothing match.
        """
        week_hours = [year_period.select_week_hours(day) for year_period in self.year_period_list]
        week_hours = filter(None, week_hours)
        return week_hours[0] if week_hours else self.week_hours

    def select_planning_events(self, date_start_utc, date_end_utc):
        """
        Select the planning events which appears in the date interval.

        ::

            --------------[date_start_utc.........date_end_utc[--------->
                [event_start...event_end[
                              [event_start...event_end[
                                            [event_start...event_end[

        .. versionadded:: 2.2.0

        :type date_start_utc: datetime.datetime
        :param date_start_utc: End date/time (UTC) of the interval (exclusive)
        :type date_end_utc: datetime.datetime
        :param date_end_utc: Start date/time (UTC) of the interval (inclusive)
        :rtype: list[intranet.model.planning.planning_event.PlanningEvent]
        :return: The list of matching planning events.
        """
        return [planning_event for planning_event in self.planning_event_list
                if (date_start_utc <= planning_event.event_start < date_end_utc or
                    date_start_utc <= planning_event.event_end < date_end_utc)]

    def get_free_intervals(self, day):
        """
        Get the free time intervals (for time tracking).

        .. versionadded:: 2.2.0

        :type day: datetime.date
        :param day: day date (local time)
        :rtype: list[(datetime.time, datetime.time)]
        :return: An list of time intervals representing the time intervals for this day.
        """
        week_hours = self.select_week_hours(day)
        if not week_hours:
            return []  # sorry
        return week_hours.get_time_intervals(day.isoweekday())

    def get_busy_intervals(self, day, tz_delta):
        """
        Get the busy time intervals (for planing).

        .. versionadded:: 2.2.0

        :type day: datetime.date
        :param day: day date (local time)
        :type tz_delta: datetime.timedelta
        :param tz_delta: time-zone delta from UTC (tz_delta = utc_date - local_date).
        :rtype: list[(datetime.time, datetime.time)]
        :return: An list of time intervals representing the time intervals for this day.
        """
        day_start_local = datetime.datetime.combine(day, datetime.time(0, 0))
        day_start_utc = day_start_local + tz_delta
        day_end_utc = day_start_utc + datetime.timedelta(days=1)
        planning_events = self.select_planning_events(day_start_utc, day_end_utc)
        return [planning_event.get_time_interval(day_start_utc, day_end_utc, tz_delta)
                for planning_event in planning_events]

    def get_available_intervals(self, day, tz_delta, minutes=15):
        """
        Get the available time intervals of the given day.
        Available intervals = free from the current week hours - busy from existing planning events.

        .. versionadded:: 2.2.0

        :type day: datetime.date
        :param day: day date (local time)
        :type tz_delta: datetime.timedelta
        :param tz_delta: time-zone delta from UTC (tz_delta = utc_date - local_date).
        :type minutes: int
        :param minutes: number of minutes to round, default is 15 minutes.
        :rtype: list[(datetime.time, datetime.time)]
        :return: An ordered list of time intervals representing the free time intervals for this day.
        """
        # -- Extract the "FREE" intervals
        free_intervals = self.get_free_intervals(day)

        # -- Extract the "BUSY" intervals
        busy_intervals = self.get_busy_intervals(day, tz_delta)

        # -- Merge "FREE" and "BUSY" intervals
        day_interval = datetime.time.min, datetime.time.max
        day_slots = [create_time_slot(day_interval, EMPTY_SLOT, minutes=minutes)]
        free_slots = [create_time_slot(interval, FREE_SLOT, minutes=minutes)
                      for interval in free_intervals]
        busy_slots = [create_time_slot(interval, BUSY_SLOT, minutes=minutes)
                      for interval in busy_intervals]
        gap_fill = GapFill(day_slots, free_slots, busy_slots)
        available_slots = [slot for slot in gap_fill.colored_slots if slot[1] == FREE_SLOT]
        return filter(None, [create_time_interval(slot, minutes=minutes) for slot in available_slots])

    def find_shift_in_day(self, day, constraint, tz_delta, assigned_hours, rate_percent, minutes=15):
        """
        Find assignable shift in the day.

        .. versionadded:: 2.2.0

        :type constraint: tuple(datetime.datetime, datetime.datetime)
        :param constraint: Start and end date/time (local time)
        :type day: datetime.date
        :param day: The day to search for an available shift.
        :type tz_delta: datetime.timedelta
        :param tz_delta: time-zone delta from UTC (tz_delta = utc_date - local_date).
        :type assigned_hours: float
        :param assigned_hours: Number of assigned hours to the task.
        :type rate_percent: float
        :param rate_percent: Assignation rate in percent: 0 < rate_percent <= 1 (not nul).
        :type minutes: int
        :param minutes: Minimal number of assignable duration.
        :rtype: (datetime.datetime, datetime.datetime)
        :return: A single hours shift or ``None`` if not assignable.
            The couple (event_start, event_end) use date/time (local time).
        """
        # -- Il nous faut trouver un intervalle de dates dont la durée soit supérieure (ou égale)
        #    à la durée de la tâche.
        intervals = self.get_available_intervals(day, tz_delta, minutes=minutes)

        # -- Pour rechercher un intervalle de temps qui correspond,
        #    nous allons majorer la durée assigned_hours par le taux rate_percent
        required_hours = assigned_hours / rate_percent

        # -- Le plus petit intervalle de temps est de 15 minutes,
        #    il faut donc arrondir la durée en heures à 15 minutes près par excès.
        required_minutes = math.ceil(required_hours * 60.0 / minutes) * minutes

        for start, end in intervals:
            event_start = datetime.datetime.combine(day, start)
            event_end = datetime.datetime.combine(day, end)
            # -- On applique la contrainte sur l'intervale de temps
            event_start = max(event_start, constraint[0])
            event_end = min(event_end, constraint[1])
            if event_start < event_end:
                duration = event_end - event_start
                total_minutes = duration.total_seconds() / 60.0
                if required_minutes <= total_minutes:
                    # -- OK, on a trouvé un intervalle assez large.
                    #    On peut plannifier la tâche avec la durée assignée (sans taux rate_percent).
                    return event_start, event_start + datetime.timedelta(hours=assigned_hours)

        # -- not found
        return None

    def find_shifts_in_interval(self, start_date, end_date, tz_delta, assigned_hours, rate_percent, minutes=15):
        """
        Find assignable shifts in the (start_date, end_date) interval.

        .. versionadded:: 2.2.0

        :type start_date: datetime.datetime
        :param start_date: Start date/time (local time) of the interval (inclusive).
        :type end_date: datetime.datetime
        :param end_date: Start date/time (local time) of the interval (exclusive).
        :type tz_delta: datetime.timedelta
        :param tz_delta: time-zone delta from UTC (tz_delta = utc_date - local_date).
        :type assigned_hours: float
        :param assigned_hours: Number of assigned hours to the task.
        :type rate_percent: float
        :param rate_percent: Assignation rate in percent: 0 < rate_percent <= 1 (not nul).
        :type minutes: int
        :param minutes: Minimal number of assignable duration.
        :rtype: list[(datetime.datetime, datetime.datetime)]
        :return: List of hours shifts or empty list if not assignable.
            The couple (event_start, event_end) use date/time (local time).
        """
        # -- On recherche un jour qui permet d'assigner toutes les heures ensembles
        constraint = (start_date, end_date)
        nbr_days = (end_date - start_date).days
        for days in xrange(nbr_days):
            day = (start_date + datetime.timedelta(days=days)).date()
            # -- Il nous faut trouver un intervalle de dates dont la durée soit supérieure (ou égale)
            #    à la durée de la tâche.
            #    L'intervalle trouvé est contraint de se trouver dans l'intervalle de temps (start_date, end_date)
            found = self.find_shift_in_day(day, constraint, tz_delta, assigned_hours, rate_percent, minutes=minutes)
            if found:
                return [found]

        # -- On recherche des jours "libre" et on assigne morceau par morceau en gardant un peu de temps libre
        shifts = []
        for days in xrange(nbr_days):
            day = (start_date + datetime.timedelta(days=days)).date()
            free_intervals = self.get_free_intervals(day)
            busy_intervals = self.get_busy_intervals(day, tz_delta)
            for start, end in free_intervals:
                if any(start <= busy_start <= end or start <= busy_end <= end
                       for busy_start, busy_end in busy_intervals):
                    continue
                event_start = datetime.datetime.combine(day, start)
                event_end = datetime.datetime.combine(day, end)
                # -- On applique la contrainte sur l'intervale de temps
                event_start = max(event_start, constraint[0])
                event_end = min(event_end, constraint[1])
                if event_start < event_end:
                    duration = event_end - event_start
                    total_minutes = duration.total_seconds() / 60.0
                    assignable_minutes = math.floor(total_minutes * rate_percent / minutes) * minutes
                    if assignable_minutes == 0:
                        # peu probable, mais on préfère éviter les intervalles vides.
                        continue
                    consumed_hours = min(assignable_minutes / 60.0, assigned_hours)
                    shifts.append((event_start, event_start + datetime.timedelta(hours=consumed_hours)))
                    assigned_hours -= consumed_hours
                    if assigned_hours == 0:
                        return shifts

        # -- Planification impossible ou incomplète.
        #    On retourne une liste vide même si on a une planification incomplète
        return []
