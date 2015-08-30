# -*- coding: utf-8 -*-
"""
Open hours
===========

Module: intranet.model.worked_hours.worked_hours

Created on: 2015-08-28
"""
from __future__ import unicode_literals

from sqlalchemy.schema import Column, ForeignKey, CheckConstraint
from sqlalchemy.types import Integer, String, SmallInteger
from sqlalchemy.orm import relationship, backref

from intranet.model import DeclarativeBase


class WorkedHours(DeclarativeBase):
    """
    WorkedHours management.
    """
    __tablename__ = 'WorkedHours'

    __table_args__ = (CheckConstraint("position > 0", name="position_check"),)  # tuple

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    position = Column(SmallInteger, unique=True, index=True, nullable=False)  # no duplicates
    label = Column(String(length=32), unique=True, nullable=False, index=True)  # no duplicates
    description = Column(String(length=200))

    week_hours_uid = Column(Integer, ForeignKey('WeekHours.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            nullable=False, index=True)

    week_hours = relationship('WeekHours',
                              backref=backref('worked_hours_list',
                                              cascade='all,delete-orphan'))

    def __init__(self, position, label, description):
        """
        Open hours

        :type position: int
        :param position: Relative position.
        :type label: unicode
        :param label: Display name => used in selection.
        :type description: unicode
        :param description: Description => used in tooltip.
        """
        self.position = position
        self.label = label
        self.description = description
