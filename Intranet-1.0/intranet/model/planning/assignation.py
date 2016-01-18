# -*- coding: utf-8 -*-
"""
Assignation
=============

Date: 2016-01-18

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.types import Integer, DateTime, Float

from intranet.model import DeclarativeBase


class Assignation(DeclarativeBase):
    """
    Assign an Employee to an OrderPhase with the given rate (percent)
    """
    __tablename__ = 'Assignation'
    __table_args__ = (UniqueConstraint('employee_uid', 'order_phase_uid',
                                       name="order_phase_employee_unique"),
                      CheckConstraint("0.0 <= rate_percent AND rate_percent <= 100.0",
                                      name="rate_interval_check"),
                      {'mysql_engine': 'InnoDB'})

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    employee_uid = Column(Integer, ForeignKey('Employee.uid',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                          nullable=True, index=True)
    order_phase_uid = Column(Integer, ForeignKey('OrderPhase.uid',
                                                 ondelete='CASCADE',
                                                 onupdate='CASCADE'),
                             nullable=True, index=True)
    rate_percent = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    employee = relationship('Employee', back_populates='assignation_list')
    order_phase = relationship('OrderPhase', back_populates='assignation_list')
    planning_event_list = relationship('PlanningEvent',
                                       back_populates="assignation",
                                       cascade='all,delete-orphan')

    def __init__(self, rate_percent, start_date=None, end_date=None):
        self.rate_percent = rate_percent
        self.start_date = start_date
        self.end_date = end_date

    @property
    def total_duration(self):
        return sum(pe.event_duration for pe in self.planning_event_list)
