# -*- coding: utf-8 -*-
"""
hours_interval
=============

Date: 2015-07-10

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

from sqlalchemy.schema import Column, CheckConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.types import Integer, SmallInteger, String, Time
from sqlalchemy.orm import relationship, backref

from intranet.model import DeclarativeBase


class HoursInterval(object):
    """
    `uid` INT NOT NULL AUTO_INCREMENT,
    `start_hour` TIME NOT NULL,
    `end_hour` TIME NOT NULL,
    `week_hours_uid` INT NOT NULL COMMENT 'Parent week_hours',
    `week_day_uid` INT NOT NULL COMMENT 'Reference one week_day',
    `day_period_uid` INT NOT NULL COMMENT 'Reference one day_period',
    """
    __tablename__ = 'HoursInterval'
    __table_args__ = (CheckConstraint("(start_hour IS NULL AND end_hour IS NULL) OR "
                                      "(end_hour IS NOT NULL AND start_hour IS NOT NULL)", name="interval_check"))

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    start_hour = Column(Time, unique=False, index=False, nullable=True)
    end_hour = Column(Time, unique=False, index=False, nullable=True)

    week_hours_uid = Column(Integer, ForeignKey('WeekHours.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            nullable=False, index=True)

    week_hours = relationship('WeekHours',
                              backref=backref('hour_interval_list',
                                              cascade='all,delete-orphan'))

    week_day_uid = Column(Integer, ForeignKey('WeekDay.uid',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                          nullable=False, index=True)

    week_day = relationship('WeekDay',
                            backref=backref('hour_interval_list',
                                            cascade='all,delete-orphan'))

    day_period_uid = Column(Integer, ForeignKey('DayPeriod.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            nullable=False, index=True)

    day_period = relationship('DayPeriod',
                              backref=backref('hour_interval_list',
                                              cascade='all,delete-orphan'))
