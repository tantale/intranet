# -*- coding: utf-8 -*-
"""
hours_interval
=============

Date: 2015-07-10

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals
import datetime

from sqlalchemy.schema import Column, CheckConstraint, ForeignKey
from sqlalchemy.types import Integer, Time
from sqlalchemy.orm import relationship, backref

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

    week_day = relationship('WeekDay',
                            backref=backref('hours_interval_list',
                                            cascade='all,delete-orphan'))

    day_period_uid = Column(Integer, ForeignKey('DayPeriod.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            primary_key=True,
                            nullable=False, index=True)

    day_period = relationship('DayPeriod',
                              backref=backref('hours_interval_list',
                                              cascade='all,delete-orphan'))

    def __init__(self, start_hour, end_hour):
        super(HoursInterval, self).__init__()
        self.start_hour = start_hour
        self.end_hour = end_hour

    def __unicode__(self):
        return u"{interval.start_hour:%H:%M} / {interval.end_hour:%H:%M}".format(interval=self)

    def __str__(self):
        return b"{interval.start_hour:%H:%M} / {interval.end_hour:%H:%M}".format(interval=self)

    @property
    def duration(self):
        day_start = datetime.date.today()
        day_end = day_start if self.start_hour <= self.end_hour else day_start + datetime.timedelta(days=1)
        return datetime.datetime.combine(day_start, self.end_hour) - datetime.datetime.combine(day_end, self.start_hour)