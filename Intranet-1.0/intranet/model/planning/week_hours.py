# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy.schema import Column, CheckConstraint
from sqlalchemy.types import Integer, SmallInteger, String

from intranet.model import DeclarativeBase
from intranet.model.planning.hours_interval import HoursInterval


class WeekHours(DeclarativeBase):
    """
    WeekHours management.
    """
    __tablename__ = 'WeekHours'
    __table_args__ = (CheckConstraint("position > 0", name="position_check"),)  # tuple

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    position = Column(SmallInteger, unique=True, index=True, nullable=False)  # no duplicates
    label = Column(String(length=32), unique=True, nullable=False, index=True)  # no duplicates
    description = Column(String(length=200))

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
