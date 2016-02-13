# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.types import Integer, String, DateTime, Boolean

from intranet.model import DeclarativeBase


class PlanningEvent(DeclarativeBase):
    """
    An event in the planning calendar.
    """
    __tablename__ = 'PlanningEvent'
    __table_args__ = (CheckConstraint("event_start <= event_end",
                                      name="start_before_end_check"),
                      UniqueConstraint('calendar_uid', 'event_start', 'event_end',
                                       name="dates_unique"),
                      {'mysql_engine': 'InnoDB'})

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    label = Column(String(length=32), unique=False, nullable=False)
    description = Column(String(length=200))
    #: start -- The date/time an event begins.
    event_start = Column(DateTime, nullable=False, index=True)
    #: end -- The date/time an event ends (exclusive).
    event_end = Column(DateTime, nullable=False, index=True)
    #: editable -- Determine if the events can be dragged and resized.
    editable = Column(Boolean(), nullable=False, default=True)
    #: all_day -- Whether an event occurs at a specific time-of-day.
    all_day = Column(Boolean(), nullable=False, default=False)
    #: location/address of the event.
    location = Column(String(length=200))
    #: is the event private?
    private = Column(Boolean(), nullable=False, default=False)

    calendar_uid = Column(Integer, ForeignKey('Calendar.uid',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                          nullable=False, index=True)

    calendar = relationship('Calendar', back_populates='planning_event_list')

    assignation_uid = Column(Integer, ForeignKey('Assignation.uid',
                                                 ondelete='CASCADE',
                                                 onupdate='CASCADE'),
                             nullable=True, index=True)

    assignation = relationship('Assignation', back_populates='planning_event_list')

    def __init__(self, label, description, event_start, event_end, editable=True, all_day=False,
                 location=None, private=False):
        """
        Initialize an calendar's event.

        :type label: unicode
        :param label: Display name of the event in the calendar grid.
        :type description: unicode or None
        :param description: Description of the event.
        :type event_start: datetime.datetime
        :param event_start: The date/time an event begins.
        :type event_end: datetime.datetime
        :param event_end: The date/time an event ends (exclusive).
        :type editable: bool
        :param editable: Determine if the events can be dragged and resized.
        :type all_day: bool
        :param all_day: Whether an event occurs at a specific time-of-day.
        :type location: unicode
        :param location: location/address of the event (if any).
        :type private: bool
        :param private: is the event private? Default is public (``False``).
        """
        self.label = label
        self.description = description
        self.event_start = event_start
        self.event_end = event_end
        self.editable = editable
        self.all_day = all_day
        self.location = location
        self.private = private

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.label!r}, "
                    "{self.description!r}, "
                    "{self.event_start!r}, "
                    "{self.event_end!r}, "
                    "{self.editable!r}, "
                    "{self.all_day!r}, "
                    "{self.location!r}, "
                    "{self.private!r}")
        return repr_fmt.format(self=self)

    def event_obj(self):
        """
        http://arshaw.com/fullcalendar/docs/event_data/Event_Object/
        @return: Event object as a Python dictionary
        """
        dict_ = dict()
        # -- Standard fields
        dict_['id'] = ('planning_event_{uid}'.format(uid=self.uid))
        dict_['title'] = self.label
        dict_['start'] = self.event_start.strftime('%Y-%m-%dT%H:%M:%SZ')
        dict_['end'] = self.event_end.strftime('%Y-%m-%dT%H:%M:%SZ')
        dict_['allDay'] = self.all_day
        dict_['editable'] = self.editable
        # todo: dict_['className'] = ""
        # -- Non-standard Fields
        dict_['calendar_uid'] = self.calendar_uid
        dict_['description'] = self.description
        dict_['location'] = self.location
        dict_['private'] = self.private
        return dict_

    @property
    def event_duration(self):
        """
        Compute the event duration in hours for statistics.

        :rtype: float
        :return: Event duration in hours.
        """
        delta = self.event_end - self.event_start
        return delta.seconds / 3600.0

    def get_time_interval(self, date_start_utc, date_end_utc, tz_delta):
        """
        Get the time interval of the event, restricted in the current day.

        ::

            --------------[date_start_utc.........date_end_utc[--------->
                [event_start...event_end[
                              [event_start...event_end[
                                            [event_start...event_end[

        :type date_start_utc: datetime.datetime
        :param date_start_utc: End date/time (UTC) of the interval (exclusive)
        :type date_end_utc: datetime.datetime
        :param date_end_utc: Start date/time (UTC) of the interval (inclusive)
        :type tz_delta: datetime.timedelta
        :param tz_delta: time-zone delta from UTC (tz_delta = local_date - utc_date).
        :rtype: (datetime.time, datetime.time)
        :return: An single time interval representing the time interval in local time.
        """
        if self.all_day:
            event_start = date_start_utc
            event_end = date_end_utc
        else:
            event_start = max(date_start_utc, self.event_start)
            event_end = min(date_end_utc, self.event_end)
        event_start_local = event_start + tz_delta
        event_end_local = event_end + tz_delta
        return event_start_local.time(), event_end_local.time()
