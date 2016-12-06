# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer
from sqlalchemy.types import SmallInteger
from sqlalchemy.types import String

from intranet.model import DeclarativeBase
from intranet.model.planning.hours_interval import HoursInterval


class WeekHours(DeclarativeBase):
    """
    WeekHours management.

    .. versionchanged:: 2.2.0
       Add the *calendar_list*, *day_period_list* and *year_period_list* relationships.
    """
    __tablename__ = 'WeekHours'
    __table_args__ = (CheckConstraint("position > 0", name="position_check"),)  # tuple

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    position = Column(SmallInteger, unique=True, index=True, nullable=False)  # no duplicates
    label = Column(String(length=32), unique=True, nullable=False, index=True)  # no duplicates
    description = Column(String(length=200))

    calendar_list = relationship("Calendar",
                                 back_populates='week_hours',
                                 cascade='all,delete-orphan')

    day_period_list = relationship("DayPeriod",
                                   back_populates='week_hours',
                                   order_by="DayPeriod.position",
                                   cascade='all,delete-orphan')

    year_period_list = relationship('YearPeriod',
                                    back_populates='week_hours',
                                    cascade='all,delete-orphan')

    def __init__(self, position, label, description):
        """
        Hours of the week.

        Examples:

        .. code-block::

            WeekHour(1, u"Open hours", u"Open hours of the company")
            WeekHour(2, u"Open hours (summer)", u"Open hours of the company in summer")

        :type position: int
        :param position: Relative position.
        :type label: unicode
        :param label: Display name of the day => used in selection.
        :type description: unicode
        :param description: Description of the day => used in tooltip.
        """
        self.position = position
        self.label = label
        self.description = description

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.position!r}), "
                    "{self.label!r}, "
                    "{self.description!r}")
        return repr_fmt.format(self=self)

    def __lt__(self, other):
        return self.position < other.position

    def __le__(self, other):
        return self.position <= other.position

    def __gt__(self, other):
        return self.position > other.position

    def __ge__(self, other):
        return self.position >= other.position

    def get_hours_interval_table(self, week_day_list):

        def empty(week_day_uid, day_period_uid):
            hi = HoursInterval(None, None)
            hi.week_day_uid = week_day_uid
            hi.day_period_uid = day_period_uid
            return hi

        day_period_list = self.day_period_list
        indexed_intervals = dict()
        for day_period in day_period_list:
            for hours_interval in day_period.hours_interval_list:
                indexed_intervals[(hours_interval.week_day_uid, hours_interval.day_period_uid)] = hours_interval

        return [[indexed_intervals.get((week_day.uid, day_period.uid)) or empty(week_day.uid, day_period.uid)
                 for day_period in day_period_list]
                for week_day in week_day_list]

    def get_hours_intervals(self, iso_weekday):
        """
        Get the hours intervals of the given day.

        .. versionadded:: 2.2.0

        :type iso_weekday: int
        :param iso_weekday: ISO iso_weekday: Monday is 1 and Sunday is 7.
        :rtype: list[intranet.model.planning.hours_interval.HoursInterval]
        :return: List of matching hours intervals.
        """
        return [hours_interval
                for day_period in self.day_period_list
                for hours_interval in day_period.hours_interval_list
                if hours_interval.week_day.iso_weekday == iso_weekday]

    def get_time_intervals(self, iso_weekday):
        """
        Get the time intervals of the given day.

        .. versionadded:: 2.2.0

        :type iso_weekday: int
        :param iso_weekday: ISO iso_weekday: Monday is 1 and Sunday is 7.
        :rtype: list[(datetime.time, datetime.time)]
        :return: An list of time intervals representing the time intervals for this day.
        """
        intervals = []
        for hours_interval in self.get_hours_intervals(iso_weekday):
            if hours_interval.start_hour <= hours_interval.end_hour:
                intervals.append((hours_interval.start_hour, hours_interval.end_hour))
            else:
                intervals.append((datetime.time.min, hours_interval.end_hour))
                intervals.append((hours_interval.start_hour, datetime.time.max))
        return intervals
