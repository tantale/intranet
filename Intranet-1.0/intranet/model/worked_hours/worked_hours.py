# -*- coding: utf-8 -*-
"""
Open hours
===========

Module: intranet.model.worked_hours.worked_hours

Created on: 2015-08-28
"""
from __future__ import unicode_literals

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship, backref

from intranet.model import DeclarativeBase


class WorkedHours(DeclarativeBase):
    """
    OpenHours management.
    """
    __tablename__ = 'OpenHours'

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    label = Column(String(length=32), unique=True, nullable=False, index=True)
    description = Column(String(length=200))

    week_hours_uid = Column(Integer, ForeignKey('WeekHours.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            nullable=False, index=True)

    week_hours = relationship('WeekHours',
                              backref=backref('worked_hours_list',
                                              cascade='all,delete-orphan'))

    def __init__(self, label, description):
        """
        Open hours

        :type label: unicode
        :param label: Display name => used in selection.
        :type description: unicode
        :param description: Description => used in tooltip.
        """
        self.label = label
        self.description = description
