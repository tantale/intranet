# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import datetime
import logging
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.model import DeclarativeBase

LOG = logging.getLogger(__name__)


class TestCalendarAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestCalendarAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestCalendarAccessor, self).setUp()

        # -- Connecting to the database
        engine = create_engine('sqlite:///:memory:', echo=False)
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

        self.accessor = EmployeeAccessor(self.session)

    def test_insert_employee(self):
        employee_name = "Employee"
        worked_hours = 39.0
        entry_date = datetime.date(2010, 11, 15)
        exit_date = None
        photo_path = None
        self.accessor.insert_employee(employee_name=employee_name,
                                      worked_hours=worked_hours,
                                      entry_date=entry_date,
                                      exit_date=exit_date,
                                      photo_path=photo_path)

        employee_list = self.accessor.get_employee_list()
        self.assertEqual(len(employee_list), 1)

        employee = employee_list[0]
        self.assertEqual(employee.employee_name, employee_name)
        self.assertEqual(employee.worked_hours, worked_hours)
        self.assertEqual(employee.entry_date, entry_date)
        self.assertEqual(employee.exit_date, exit_date)
        self.assertEqual(employee.photo_path, photo_path)

        # -- Every employee has a calendar
        self.assertIsNotNone(employee.calendar)

        # -- Check cascade delete
        self.accessor.delete_employee(employee.uid)
        employee_list = self.accessor.get_employee_list()
        self.assertEqual(len(employee_list), 0)
        calendar_accessor = CalendarAccessor(self.session)
        calendar_list = calendar_accessor.get_calendar_list()
        self.assertEqual(len(calendar_list), 1)
