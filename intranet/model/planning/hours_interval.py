# -*- coding: utf-8 -*-
"""
hours_interval
=============

Date: 2015-07-10

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, CheckConstraint, ForeignKey
from sqlalchemy.types import Integer, Time

from intranet.model import DeclarativeBase


class HoursInterval(DeclarativeBase):
    """
    `uid` INT NOT NULL AUTO_INCREMENT,
    `start_hour` TIME NOT NULL,
    `end_hour` TIME NOT NULL,
    `week_day_uid` INT NOT NULL COMMENT 'Reference one week_day',
    `day_period_uid` INT NOT NULL COMMENT 'Reference one day_period',
    """
    __tablename__ = 'HoursInterval'
    __table_args__ = (CheckConstraint("(start_hour IS NULL AND end_hour IS NULL) OR "
                                      "(end_hour IS NOT NULL AND start_hour IS NOT NULL)", name="interval_check"),)

    start_hour = Column(Time, unique=False, index=False, nullable=True)
    end_hour = Column(Time, unique=False, index=False, nullable=True)

    week_day_uid = Column(Integer, ForeignKey('WeekDay.uid',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                          primary_key=True,
                          nullable=False, index=True)

    week_day = relationship('WeekDay', back_populates='hours_interval_list')

    day_period_uid = Column(Integer, ForeignKey('DayPeriod.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            primary_key=True,
                            nullable=False, index=True)

    day_period = relationship('DayPeriod', back_populates='hours_interval_list')

    def __init__(self, start_hour, end_hour):
        super(HoursInterval, self).__init__()
        self.start_hour = start_hour
        self.end_hour = end_hour

    def __copy__(self):
        return self.__class__(self.start_hour, self.end_hour)

    # noinspection PyUnusedLocal
    def __deepcopy__(self, memo):
        new = self.__copy__()
        new.week_day_uid = self.week_day_uid
        new.day_period_uid = None
        return new

    def __unicode__(self):
        start = u"{0:%H:%M}".format(self.start_hour) if self.start_hour else u"--"
        end = u"{0:%H:%M}".format(self.end_hour) if self.end_hour else u"--"
        return start + u" / " + end

    def __str__(self):
        start = b"{0:%H:%M}".format(self.start_hour) if self.start_hour else b"--"
        end = b"{0:%H:%M}".format(self.end_hour) if self.end_hour else b"--"
        return start + b" / " + end

    def __repr__(self):
        return self.__str__()

    @property
    def duration(self):
        day_start = datetime.date.today()
        day_end = day_start if self.start_hour <= self.end_hour else day_start + datetime.timedelta(days=1)
        return datetime.datetime.combine(day_start, self.end_hour) - datetime.datetime.combine(day_end, self.start_hour)
