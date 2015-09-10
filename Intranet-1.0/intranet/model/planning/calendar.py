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

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    position = Column(SmallInteger, unique=True, index=True, nullable=False)  # no duplicates
    label = Column(String(length=32), unique=True, nullable=False, index=True)  # no duplicates
    description = Column(String(length=200))

    background_color = Column(String(length=7), nullable=True)
    border_color = Column(String(length=7), nullable=True)
    text_color = Column(String(length=7), nullable=True)
    class_name = Column(String(length=50), nullable=True)

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
                 background_color=None, border_color=None, text_color=None, class_name=None):
        """
        Calendar, see: http://fullcalendar.io/docs/event_data/Event_Source_Object/

        :type position: int
        :param position: Relative position.
        :type label: unicode
        :param label: Display name => used in selection.
        :type description: unicode
        :param description: Description => used in tooltip.
        :param background_color: Event's backgroud color (if any)
        :param border_color: Event's border color (if any)
        :param text_color: Event's text color (if any)
        :param class_name: Event's CSS class name (if any), see: project's category ``project_cat``.
        """
        self.position = position
        self.label = label
        self.description = description
        self.background_color = background_color
        self.border_color = border_color
        self.text_color = text_color
        self.class_name = class_name
