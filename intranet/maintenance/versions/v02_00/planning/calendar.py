# -*- coding: utf-8 -*-
"""
Planning calendar
=================

Module: intranet.model.calendar.calendar

Created on: 2015-08-28
"""
from __future__ import unicode_literals

import re

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey, CheckConstraint
from sqlalchemy.types import Integer, String, Float

from intranet.maintenance.versions.v02_00.model import DeclarativeBase

COLOR_REGEX = ur"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
match_color = re.compile(COLOR_REGEX).match


def checked_color(color):
    if color is None or match_color(color):
        return color
    raise ValueError(color)


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
    position = Column(Float, unique=True, index=True, nullable=False)  # no duplicates
    label = Column(String(length=32), unique=True, nullable=False, index=True)  # no duplicates
    description = Column(String(length=200))

    background_color = Column(String(length=7), nullable=False, default=BACKGROUND_COLOR)
    border_color = Column(String(length=7), nullable=False, default=BORDER_COLOR)
    text_color = Column(String(length=7), nullable=False, default=TEXT_COLOR)
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

    employee = relationship("Employee", back_populates="calendar")

    def __init__(self, position, label, description,
                 background_color=BACKGROUND_COLOR, border_color=BORDER_COLOR, text_color=TEXT_COLOR, class_name=None):
        """
        Calendar, see: http://fullcalendar.io/docs/event_data/Event_Source_Object/

        :type position: int
        :param position: Relative position.
        :type label: unicode
        :param label: Display name => used in selection.
        :type description: unicode
        :param description: Description => used in tooltip.
        :param background_color: Event's background color (if any)
        :param border_color: Event's border color (if any)
        :param text_color: Event's text color (if any)
        :param class_name: Event's CSS class name (if any), see: project's category ``project_cat``.
        """
        self.position = position
        self.label = label
        self.description = description
        self.background_color = checked_color(background_color)
        self.border_color = checked_color(border_color)
        self.text_color = checked_color(text_color)
        self.class_name = class_name

    def event_source_obj(self):
        """
        http://fullcalendar.io/docs1/event_data/Event_Source_Object/

        :return: Event source object as a Python dictionary
        """
        dict_ = dict()
        # -- Standard fields
        dict_['id'] = ('{uid}'.format(uid=self.uid))
        if self.class_name:
            dict_['className'] = self.class_name
        else:
            dict_['backgroundColor'] = self.background_color
            dict_['borderColor'] = self.border_color
            dict_['textColor'] = self.text_color
        return dict_
