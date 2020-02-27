# -*- coding: utf-8 -*-
"""
Year period
===========

Module: intranet.model.planning.year_period

Created on: 2015-08-28
"""
from __future__ import unicode_literals

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Date

from intranet.maintenance.versions.v02_00.model import DeclarativeBase


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

    calendar = relationship('Calendar',
                            backref=backref('year_period_list',
                                            cascade='all,delete-orphan'))

    frequency_uid = Column(Integer, ForeignKey('Frequency.uid',
                                               ondelete='CASCADE',
                                               onupdate='CASCADE'),
                           nullable=False, index=True)

    frequency = relationship('Frequency',
                             backref=backref('year_period_list',
                                             cascade='all,delete-orphan'))

    week_hours_uid = Column(Integer, ForeignKey('WeekHours.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            nullable=False, index=True)

    week_hours = relationship('WeekHours',
                              backref=backref('year_period_list',
                                              cascade='all,delete-orphan'))

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
