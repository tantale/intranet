# -*- coding: utf-8 -*-
"""
Open hours
===========

Module: intranet.model.calendar.calendar

Created on: 2015-08-28
"""
from __future__ import unicode_literals

from sqlalchemy.schema import Column, ForeignKey, CheckConstraint
from sqlalchemy.types import Integer, String, SmallInteger
from sqlalchemy.orm import relationship, backref

from intranet.model import DeclarativeBase


class Calendar(DeclarativeBase):
    """
    Calendar management.
    """
    __tablename__ = 'Calendar'

    __table_args__ = (CheckConstraint("position > 0", name="position_check"),)  # tuple

    #: Default Event colors: intranet/public/css/fullcalendar.css:264
    BACKGROUND_COLOR = "#3a87ad"
    BORDER_COLOR = "#3a87ad"
    TEXT_COLOR = "#ffffff"

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    position = Column(SmallInteger, unique=True, index=True, nullable=False)  # no duplicates
    label = Column(String(length=32), unique=True, nullable=False, index=True)  # no duplicates
    description = Column(String(length=200))
    background_color = Column(String(length=7), nullable=False, default=BACKGROUND_COLOR)
    border_color = Column(String(length=7), nullable=False, default=BORDER_COLOR)
    text_color = Column(String(length=7), nullable=False, default=TEXT_COLOR)

    week_hours_uid = Column(Integer, ForeignKey('WeekHours.uid',
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                            nullable=False, index=True)

    week_hours = relationship('WeekHours',
                              backref=backref('calendar_list',
                                              cascade='all,delete-orphan'))

    employee_uid = Column(Integer, ForeignKey('Employee.uid',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                          nullable=True, index=True)

    employee = relationship('Employee',
                            backref=backref('calendar',
                                            uselist=False,
                                            cascade='save-update'))

    def __init__(self, position, label, description,
                 background_color=BACKGROUND_COLOR, border_color=BORDER_COLOR, text_color=TEXT_COLOR):
        """
        Calendar, see: http://fullcalendar.io/docs/event_data/Event_Source_Object/

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
        self.background_color = background_color
        self.border_color = border_color
        self.text_color = text_color
