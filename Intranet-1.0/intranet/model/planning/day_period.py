# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, CheckConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.types import Integer, SmallInteger, String

from intranet.model import DeclarativeBase


class DayPeriod(DeclarativeBase):
    """
    DayPeriod management.
    """
    __tablename__ = 'DayPeriod'
    __table_args__ = (UniqueConstraint('week_hours_uid', 'position',
                                       name="week_hours_position_unique"),
                      UniqueConstraint('week_hours_uid', 'label',
                                       name="week_hours_label_unique"),
                      CheckConstraint("position > 0", name="position_check"))

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    position = Column(SmallInteger, unique=False, index=True, nullable=False)  # with duplicates
    label = Column(String(length=32), unique=False, nullable=False, index=True)  # with duplicates
    description = Column(String(length=200))

    week_hours_uid = Column(Integer, ForeignKey('WeekHours.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            nullable=False, index=True)

    week_hours = relationship('WeekHours', back_populates='day_period_list')

    hours_interval_list = relationship('HoursInterval',
                                       back_populates='day_period',
                                       cascade='all,delete-orphan')

    def __init__(self, position, label, description):
        """
        Period of the day: morning, afternoon...

        Examples:

        .. code-block::

            WeekHour(1, u"Morning", u"Hours in the morning")
            WeekHour(2, u"Afternoon", u"Hours in the afternoon")

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

    def __copy__(self):
        return self.__class__(self.position, self.label, self.description)

    def __deepcopy__(self, memo):
        new = self.__copy__()
        new.week_hours_uid = None
        new.hours_interval_list = copy.deepcopy(self.hours_interval_list, memo)
        return new

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
