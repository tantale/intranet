# coding: utf8
from __future__ import unicode_literals

import datetime
import logging
import unittest

import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.planning_event import PlanningEventAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.model import DeclarativeBase

LOG = logging.getLogger(__name__)


class TestCalendarAccessor(unittest.TestCase):
    DEBUG = True

    @classmethod
    def setUpClass(cls):
        super(TestCalendarAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestCalendarAccessor, self).setUp()

        # # -- Connecting to the database
        # here = "/Users/laurentlaporte/git/repo-intranet-master/Intranet-1.0"
        # engine = sqlalchemy.create_engine('sqlite:///{here}/devdata.db'.format(here=here), echo=False)

        # -- Connecting to the database
        engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

        week_day_accessor = WeekDayAccessor(self.session)
        week_hours_accessor = WeekHoursAccessor(self.session)
        day_period_accessor = DayPeriodAccessor(self.session)
        hours_interval_accessor = HoursIntervalAccessor(self.session)
        calendar_accessor = CalendarAccessor(self.session)

        week_day_accessor.setup()
        week_hours_accessor.setup()
        week_hours_list = week_hours_accessor.get_week_hours_list()
        for week_hours in week_hours_list:
            day_period_accessor.setup(week_hours.uid)
            hours_interval_accessor.setup(week_hours.uid)
            calendar_accessor.setup(week_hours.uid)

        employee_accessor = EmployeeAccessor(self.session)
        employee_accessor.insert_employee(employee_name=u"MOUSSAY Damien",
                                          worked_hours=39.0,
                                          entry_date=datetime.datetime(2010, 1, 1),
                                          exit_date=None,
                                          photo_path=None)

        employee = employee_accessor.get_employee_by_name(u"MOUSSAY Damien")
        planning_event_accessor = PlanningEventAccessor(self.session)
        planning_event_accessor.insert_planning_event(employee.calendar.uid,
                                                      u"Sports d'hiver",
                                                      None,
                                                      datetime.datetime(2017, 2, 13, 7, 0),
                                                      datetime.datetime(2017, 2, 18, 8, 0),
                                                      editable=True,
                                                      all_day=False,
                                                      location=u"",
                                                      private=False)

    def test_get_free_intervals(self):
        employee_accessor = EmployeeAccessor(self.session)
        employee = employee_accessor.get_employee_by_name(u"MOUSSAY Damien")

        # -- Get the employee's calendar
        calendar = employee.calendar
        LOG.info("planning_event_list for {employee_name}:".format(employee_name=employee.employee_name))
        planning_event_list = sorted(calendar.planning_event_list, key=lambda e: (e.event_start, e.event_end))
        for event in planning_event_list:
            LOG.info("  " + unicode(event))
        self.assertEqual(len(planning_event_list), 1)

        day = datetime.datetime.strptime("14/02/2017", "%d/%m/%Y")
        free_intervals = calendar.get_free_intervals(day)
        LOG.info("free_intervals for {day:%d/%m/%Y}:".format(day=day))
        for interval in free_intervals:
            LOG.info("  {interval[0]:%H:%M} - {interval[1]:%H:%M}".format(interval=interval))
        self.assertEqual(free_intervals, [(datetime.time(8, 30), datetime.time(12, 30)),
                                          (datetime.time(14, 0), datetime.time(17, 45))])

        tz_delta = datetime.timedelta(-1, 82800, 0)
        busy_intervals = calendar.get_busy_intervals(day, tz_delta=tz_delta)
        LOG.info("busy_intervals for {day:%d/%m/%Y}:".format(day=day))
        for interval in busy_intervals:
            LOG.info("  {interval[0]:%H:%M} - {interval[1]:%H:%M}".format(interval=interval))
        self.assertEqual(busy_intervals, [(datetime.time.min, datetime.time.max)])

        available_intervals = calendar.get_available_intervals(day, tz_delta=tz_delta)
        LOG.info("available_intervals for {day:%d/%m/%Y}:".format(day=day))
        for interval in available_intervals:
            LOG.info("  {interval[0]:%H:%M} - {interval[1]:%H:%M}".format(interval=interval))
        self.assertEqual(len(available_intervals), 0)
