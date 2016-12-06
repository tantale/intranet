# -*- coding: utf-8 -*-
"""
Year period
===========

Module: intranet.model.planning.year_period

Created on: 2015-08-28
"""
from __future__ import unicode_literals

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.types import Integer

from intranet.model import DeclarativeBase


class YearPeriod(DeclarativeBase):
    """
    YearPeriod management.
    """
    __tablename__ = 'YearPeriod'

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    start_date = Column(Date, unique=False, index=False, nullable=False)
    end_date = Column(Date, unique=False, index=False, nullable=False)

    calendar_uid = Column(Integer, ForeignKey('Calendar.uid',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                          nullable=False, index=True)

    frequency_uid = Column(Integer, ForeignKey('Frequency.uid',
                                               ondelete='CASCADE',
                                               onupdate='CASCADE'),
                           nullable=False, index=True)

    week_hours_uid = Column(Integer, ForeignKey('WeekHours.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            nullable=False, index=True)

    calendar = relationship('Calendar', back_populates='year_period_list')
    frequency = relationship('Frequency', back_populates='year_period_list')
    week_hours = relationship('WeekHours', back_populates='year_period_list')

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __copy__(self):
        return self.__class__(self.start_date, self.end_date)

    # noinspection PyUnusedLocal
    def __deepcopy__(self, memo):
        new = self.__copy__()
        new.calendar_uid = self.calendar_uid
        new.frequency_uid = self.frequency_uid
        new.week_hours_uid = None
        return new

    def select_week_hours(self, day):
        """
        Select the week hours matching the given day.
        Return ``None`` if the day doesn't match.

        .. versionadded:: 2.2.0

        :type day: datetime.date
        :param day: The day to select in the year period.
        :rtype: WeekHours
        :return: The matching week hours instance, or ``None`` if no match.
        """
        week = day.isocalendar()[1]
        if self.start_date <= day <= self.end_date and self.frequency.match_week(week):
            return self.week_hours
        return None
