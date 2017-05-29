"""
:module: intranet.model.pointage.employee
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import Date
from sqlalchemy.types import Float
from sqlalchemy.types import Integer
from sqlalchemy.types import String

from intranet.accessors.gap_fill import GapFill
from intranet.accessors.time_slot import BUSY_SLOT
from intranet.accessors.time_slot import EMPTY_SLOT
from intranet.accessors.time_slot import FREE_SLOT
from intranet.accessors.time_slot import create_time_interval
from intranet.accessors.time_slot import create_time_slot
from intranet.model import DeclarativeBase


class Employee(DeclarativeBase):
    """
    Employee management.

    .. versionadded:: 1.2.0
       - The UID is the personal ID.
       - The name 'employee_name' isn't anymore unique: we tolerate duplicated names.
       - The worked hours field can be a decimal value, eg.: 31.2 hours.

    .. versionchanged:: 2.2.0
       Add the *cal_event_list* and *assignation_list* relationships.
       Prepare table properties for MySQL.
    """
    __tablename__ = 'Employee'
    __table_args__ = ({'mysql_engine': 'InnoDB'},)

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    employee_name = Column(String(length=50), unique=False, nullable=False,
                           index=True)
    worked_hours = Column(Float, nullable=False)
    entry_date = Column(Date, nullable=False, index=True)
    exit_date = Column(Date, nullable=True, index=True)
    photo_path = Column(String(length=200), nullable=True)

    # attr calendar: don't delete-orphan
    calendar = relationship("Calendar", uselist=False, back_populates="employee", cascade='all')

    cal_event_list = relationship('CalEvent',
                                  back_populates="employee",
                                  order_by="CalEvent.event_start",
                                  cascade='all,delete-orphan')

    # -- New fields/relationships for order planning (since: 2.2.0)
    assignation_list = relationship('Assignation',
                                    back_populates="employee",
                                    cascade='all,delete-orphan')

    def __init__(self, employee_name, worked_hours, entry_date,
                 exit_date=None, photo_path=None):
        """
        Initialize employee's information.

        :param employee_name: employee's name (unique and not null)

        :param worked_hours: weekly worked hours (required), eg.: 39 h/week
        :type worked_hours: float

        :param entry_date: entry date in the company (required)
        :type entry_date: datetime.date

        :param exit_date: exit date from the company, or None if still active
        :type exit_date: datetime.date

        :param photo_path: photo path of the employee if any, or None
        """
        self.employee_name = employee_name
        self.worked_hours = worked_hours
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.photo_path = photo_path

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.employee_name!r}, "
                    "{self.worked_hours!r}, "
                    "{self.entry_date!r}, "
                    "exit_date={self.exit_date!r}, "
                    "photo_path={self.photo_path!r})")
        return repr_fmt.format(self=self)

    def select_cal_events(self, date_start_utc, date_end_utc):
        """
        Select the calendar events which appears in the date interval.

        ::

            --------------[date_start_utc.........date_end_utc[--------->
                [event_start...event_end[
                              [event_start...event_end[
                                            [event_start...event_end[
                [event_start...............................event_end[

        .. versionadded:: 2.2.0

        .. versionadded:: 2.2.0

        :type date_start_utc: datetime.datetime
        :param date_start_utc: End date/time (UTC) of the interval (exclusive)
        :type date_end_utc: datetime.datetime
        :param date_end_utc: Start date/time (UTC) of the interval (inclusive)
        :rtype: list[intranet.model.pointage.cal_event.CalEvent]
        :return: The list of matching calendar events.
        """
        return [cal_event for cal_event in self.cal_event_list
                if not (cal_event.event_end < date_start_utc or date_end_utc <= cal_event.event_start)]

    def get_free_intervals(self, day):
        """
        Get the free time intervals (for time tracking).

        .. versionadded:: 2.2.0

        :type day: datetime.date
        :param day: day date (local time)
        :rtype: list[(datetime.time, datetime.time)]
        :return: An list of time intervals representing the time intervals for this day.
        """
        if not self.calendar:
            return []  # sorry
        return self.calendar.get_free_intervals(day)

    def get_busy_intervals(self, day, tz_delta):
        """
        Get the busy time intervals (for planing).

        .. versionadded:: 2.2.0

        :type day: datetime.date
        :param day: day date (local time)
        :type tz_delta: datetime.timedelta
        :param tz_delta: time-zone delta from UTC (tz_delta = utc_date - local_date).
        :rtype: list[(datetime.time, datetime.time)]
        :return: An list of time intervals representing the time intervals for this day.
        """
        # fixme: day should be a datetime
        day_start_local = datetime.datetime.combine(day, datetime.time.min)
        day_start_utc = day_start_local + tz_delta
        day_end_utc = day_start_utc + datetime.timedelta(days=1)
        cal_events = self.select_cal_events(day_start_utc, day_end_utc)
        return [cal_event.get_time_interval(day_start_utc, day_end_utc, tz_delta)
                for cal_event in cal_events]

    def get_available_intervals(self, day, tz_delta, minutes=15):
        """
        Get the available time intervals of the given day.
        Available intervals = free from the current week hours - busy from existing planning events.

        .. versionadded:: 2.2.0

        :type day: datetime.date
        :param day: day date (local time)
        :type tz_delta: datetime.timedelta
        :param tz_delta: time-zone delta from UTC (tz_delta = utc_date - local_date).
        :type minutes: int
        :param minutes: number of minutes to round, default is 15 minutes.
        :rtype: list[(datetime.time, datetime.time)]
        :return: An ordered list of time intervals representing the free time intervals for this day.
        """
        # -- Extract the "FREE" intervals
        free_intervals = self.get_free_intervals(day)

        # -- Extract the "BUSY" intervals
        busy_intervals = self.get_busy_intervals(day, tz_delta)

        # -- Merge "FREE" and "BUSY" intervals
        day_interval = datetime.time.min, datetime.time.max
        day_slots = [create_time_slot(day_interval, EMPTY_SLOT, minutes=minutes)]
        free_slots = [create_time_slot(interval, FREE_SLOT, minutes=minutes)
                      for interval in free_intervals]
        busy_slots = [create_time_slot(interval, BUSY_SLOT, minutes=minutes)
                      for interval in busy_intervals]
        gap_fill = GapFill(day_slots, free_slots, busy_slots)
        available_slots = [slot for slot in gap_fill.colored_slots if slot[1] == FREE_SLOT]
        return filter(None, [create_time_interval(slot, minutes=minutes) for slot in available_slots])
