# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy.schema import Column, CheckConstraint
from sqlalchemy.types import Integer, SmallInteger, String
from intranet.model import DeclarativeBase


class WeekDay(DeclarativeBase):
    """
    WeekDay management.
    """
    __tablename__ = 'WeekDay'
    # ISO weekday: Monday is 1 and Sunday is 7
    __table_args__ = (CheckConstraint("1 <= weekday AND weekday <= 7", name="weekday_check"),)

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    weekday = Column(SmallInteger, unique=True, index=True, nullable=False)  # without duplicates
    label = Column(String(length=32), unique=True, nullable=False, index=True)  # without duplicates
    description = Column(String(length=200))

    def __init__(self, weekday, label, description=None):
        """
        The day of the week, from monday to sunday.

        Examples:

        .. code-block::

            WeekDay(1, u"Monday")
            WeekDay(2, u"Tuesday")
            WeekDay(3, u"Wednesday")
            WeekDay(4, u"Thursday")
            WeekDay(5, u"Friday")
            WeekDay(6, u"Saturday")
            WeekDay(7, u"Sunday")

        :type weekday: int
        :param weekday: Day in the week: 0 <= weekday <= 6
        :type label: unicode
        :param label: Display name of the day => used in selection.
        :type description: unicode
        :param description: Description of the day => used in tooltip.
        """
        self.weekday = weekday
        self.label = label
        self.description = description

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.weekday!r}, "
                    "{self.label!r}, "
                    "{self.description!r})")
        return repr_fmt.format(self=self)
