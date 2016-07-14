# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import datetime
import logging
import pprint
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.planning_event import PlanningEventAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.pointage.assignation import AssignationAccessor
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.pointage.order import OrderAccessor
from intranet.model import DeclarativeBase
from intranet.model.pointage.order import Order

LOG = logging.getLogger(__name__)


class TestAssignationAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestAssignationAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)
        logging.getLogger("txn").setLevel(logging.INFO)

    def setUp(self):
        super(TestAssignationAccessor, self).setUp()

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

        employee_name = "Employee"
        worked_hours = 39.0
        entry_date = datetime.date(2010, 11, 15)
        exit_date = None
        photo_path = None
        self.employee_accessor = EmployeeAccessor(self.session)
        self.employee_accessor.insert_employee(employee_name=employee_name,
                                               worked_hours=worked_hours,
                                               entry_date=entry_date,
                                               exit_date=exit_date,
                                               photo_path=photo_path)

        order_ref = "My order_ref"
        project_cat = "My project_cat"
        creation_date = datetime.datetime(2016, 2, 14, 12, 30)
        self.order_accessor = OrderAccessor(self.session)
        self.order_accessor.insert_order(order_ref=order_ref,
                                         project_cat=project_cat,
                                         creation_date=creation_date)

        self.planning_event_accessor = PlanningEventAccessor(self.session)
        self.assignation_accessor = AssignationAccessor(self.session)

    def _get_order_by_ref(self, order_ref):
        return self.order_accessor.get_order_list(Order.order_ref == order_ref)[0]

    def test_short_plan(self):
        # -- start date is Tuesdays
        tz_delta = datetime.timedelta(hours=2)  # UTC+2
        today = datetime.date(2016, 5, 24)
        assert today.isoweekday() == 2  # Monday is 1 and Sunday is 7.

        # -- Add a event from 9:00 to 10:30
        label = "My Work"
        description = "I do some DIY"
        # note: tz_delta = utc_date - local_date
        event_start_utc = datetime.datetime.combine(today, datetime.time(9, 0)) + tz_delta
        event_end_utc = datetime.datetime.combine(today, datetime.time(10, 30)) + tz_delta
        employee = self.employee_accessor.get_last_employee()
        self.planning_event_accessor.insert_planning_event(employee.calendar.uid,
                                                           label, description, event_start_utc, event_end_utc)

        # -- Check available intervals (local time)
        employee = self.employee_accessor.get_last_employee()
        intervals = employee.calendar.get_available_intervals(today, tz_delta)
        expected = [(datetime.time(8, 30), datetime.time(9, 0)),
                    (datetime.time(10, 30), datetime.time(12, 30)),
                    (datetime.time(14, 0), datetime.time(17, 45))]
        self.assertEqual(intervals, expected)

        # -- Prepare an Order, an OrderPhase and insert a new assignation
        order = self._get_order_by_ref("My order_ref")
        order_phase = order.order_phase_list[0]
        assigned_hours = 1.5  # 1:30
        rate_percent = .8  # 80%
        start_date_utc = datetime.datetime.combine(today, datetime.time.min) + tz_delta
        end_date_utc = None  # No limit
        self.assignation_accessor.insert_assignation(employee.uid,
                                                     order_phase.uid, assigned_hours, rate_percent,
                                                     start_date_utc, end_date_utc)

        # -- We can list the assigned tasks
        employee = self.employee_accessor.get_last_employee()
        assignation_list = employee.assignation_list
        self.assertEqual(len(assignation_list), 1)
        assignation = assignation_list[0]
        self.assertEqual(assignation.employee, employee)
        self.assertEqual(assignation.assigned_hours, assigned_hours)
        self.assertEqual(assignation.rate_percent, rate_percent)
        self.assertEqual(assignation.start_date, start_date_utc)
        self.assertEqual(assignation.end_date, end_date_utc)

        # -- We want to plan it today
        event_list = self.assignation_accessor.plan_assignation(assignation.uid, tz_delta=tz_delta)
        event_start, event_end = event_list[0]
        self.assertEqual(event_start, datetime.datetime.combine(today, datetime.time(10, 30)))
        self.assertEqual(event_end, datetime.datetime.combine(today, datetime.time(12, 0)))

        # -- Check available intervals
        employee = self.employee_accessor.get_last_employee()
        intervals = employee.calendar.get_available_intervals(today, tz_delta)
        expected = [(datetime.time(8, 30), datetime.time(9, 0)),
                    (datetime.time(12, 00), datetime.time(12, 30)),
                    (datetime.time(14, 0), datetime.time(17, 45))]
        self.assertEqual(intervals, expected)

    def test_medium_plan(self):
        # -- start date is Tuesdays
        tz_delta = datetime.timedelta(hours=2)  # UTC+2
        today = datetime.date(2016, 5, 24)

        # -- Add a event from 9:00 to 10:30
        label = "My Work"
        description = "I do some DIY"
        event_start_utc = datetime.datetime.combine(today, datetime.time(9, 0)) + tz_delta
        event_end_utc = datetime.datetime.combine(today, datetime.time(10, 30)) + tz_delta
        employee = self.employee_accessor.get_last_employee()
        self.planning_event_accessor.insert_planning_event(employee.calendar.uid,
                                                           label, description, event_start_utc, event_end_utc)

        # -- Prepare an Order, an OrderPhase and insert a new assignation
        order = self._get_order_by_ref("My order_ref")
        order_phase = order.order_phase_list[0]
        assigned_hours = 3.25  # 3h15
        rate_percent = 1  # 100 %
        start_date_utc = datetime.datetime.combine(today, datetime.time.min) + tz_delta
        end_date_utc = None  # No limit
        self.assignation_accessor.insert_assignation(employee.uid,
                                                     order_phase.uid, assigned_hours, rate_percent,
                                                     start_date_utc, end_date_utc)

        # -- We can list the assigned tasks
        employee = self.employee_accessor.get_last_employee()
        assignation_list = employee.assignation_list
        self.assertEqual(len(assignation_list), 1)
        assignation = assignation_list[0]

        # -- We want to plan it today
        event_list = self.assignation_accessor.plan_assignation(assignation.uid, tz_delta=tz_delta)
        event_start, event_end = event_list[0]
        self.assertEqual(event_start, datetime.datetime.combine(today, datetime.time(14, 0)))
        self.assertEqual(event_end, datetime.datetime.combine(today, datetime.time(17, 15)))

        # -- Check available intervals
        employee = self.employee_accessor.get_last_employee()
        intervals = employee.calendar.get_available_intervals(today, tz_delta)
        expected = [(datetime.time(8, 30), datetime.time(9, 0)),
                    (datetime.time(10, 30), datetime.time(12, 30)),
                    (datetime.time(17, 15), datetime.time(17, 45))]
        self.assertEqual(intervals, expected)

    def test_medium_plan_tomorrow(self):
        # -- start date is Tuesdays
        tz_delta = datetime.timedelta(hours=2)  # UTC+2
        today = datetime.date(2016, 5, 24)

        employee = self.employee_accessor.get_last_employee()
        calendar_uid = employee.calendar.uid

        # -- Add a event from 9:00 to 10:30
        label = "My Work"
        description = "I do some DIY"
        event_start_utc = datetime.datetime.combine(today, datetime.time(9, 0)) + tz_delta
        event_end_utc = datetime.datetime.combine(today, datetime.time(10, 30)) + tz_delta
        self.planning_event_accessor.insert_planning_event(calendar_uid,
                                                           label, description, event_start_utc, event_end_utc)

        # -- Add a event from 15:00 to 17:00
        label = "Meeting"
        description = "I have a meeting"
        event_start_utc = datetime.datetime.combine(today, datetime.time(15, 0)) + tz_delta
        event_end_utc = datetime.datetime.combine(today, datetime.time(17, 0)) + tz_delta
        self.planning_event_accessor.insert_planning_event(calendar_uid,
                                                           label, description, event_start_utc, event_end_utc)

        # -- Prepare an Order, an OrderPhase and insert a new assignation
        order = self._get_order_by_ref("My order_ref")
        order_phase = order.order_phase_list[0]
        assigned_hours = 3.25  # 3h15
        rate_percent = 1  # 100 %
        start_date_utc = datetime.datetime.combine(today, datetime.time.min) + tz_delta
        end_date_utc = None  # No limit
        self.assignation_accessor.insert_assignation(employee.uid,
                                                     order_phase.uid, assigned_hours, rate_percent,
                                                     start_date_utc, end_date_utc)

        # -- We can list the assigned tasks
        employee = self.employee_accessor.get_last_employee()
        assignation_list = employee.assignation_list
        self.assertEqual(len(assignation_list), 1)
        assignation = assignation_list[0]

        # -- We want to plan it today, we got it tomorrow
        event_list = self.assignation_accessor.plan_assignation(assignation.uid, tz_delta=tz_delta)
        event_start, event_end = event_list[0]
        tomorrow = today + datetime.timedelta(days=1)
        self.assertEqual(event_start, datetime.datetime.combine(tomorrow, datetime.time(8, 30)))
        self.assertEqual(event_end, datetime.datetime.combine(tomorrow, datetime.time(11, 45)))

        # -- Check available intervals for today
        employee = self.employee_accessor.get_last_employee()
        intervals = employee.calendar.get_available_intervals(today, tz_delta)
        expected = [(datetime.time(8, 30), datetime.time(9, 0)),
                    (datetime.time(10, 30), datetime.time(12, 30)),
                    (datetime.time(14, 0), datetime.time(15, 0)),
                    (datetime.time(17, 0), datetime.time(17, 45))]
        self.assertEqual(intervals, expected)

        # -- Check available intervals for tomorrow
        employee = self.employee_accessor.get_last_employee()
        intervals = employee.calendar.get_available_intervals(tomorrow, tz_delta)
        expected = [(datetime.time(11, 45), datetime.time(12, 30)),
                    (datetime.time(14, 0), datetime.time(17, 45))]
        self.assertEqual(intervals, expected)

    def _check_total_hours(self, intervals, assigned_hours):
        total_sec = 0
        for start_time, end_time in intervals:
            delay = end_time - start_time
            total_sec += delay.total_seconds()
        self.assertEqual(total_sec / 3600, assigned_hours)

    def test_big_plan(self):
        # -- start date is Tuesdays
        tz_delta = datetime.timedelta(hours=2)  # UTC+2
        today = datetime.date(2016, 5, 24)

        # -- Add a event from 9:00 to 10:30
        label = "My Work"
        description = "I do some DIY"
        event_start_utc = datetime.datetime.combine(today, datetime.time(9, 0)) + tz_delta
        event_end_utc = datetime.datetime.combine(today, datetime.time(10, 30)) + tz_delta
        employee = self.employee_accessor.get_last_employee()
        self.planning_event_accessor.insert_planning_event(employee.calendar.uid,
                                                           label, description, event_start_utc, event_end_utc)

        # -- Prepare an Order, an OrderPhase and insert a new assignation
        order = self._get_order_by_ref("My order_ref")
        order_phase = order.order_phase_list[0]
        assigned_hours = 12  # 12:00
        rate_percent = .5  # 50 %
        start_date_utc = datetime.datetime.combine(today, datetime.time.min) + tz_delta
        end_date_utc = None  # No limit
        self.assignation_accessor.insert_assignation(employee.uid,
                                                     order_phase.uid, assigned_hours, rate_percent,
                                                     start_date_utc, end_date_utc)

        # -- We can list the assigned tasks
        employee = self.employee_accessor.get_last_employee()
        assignation_list = employee.assignation_list
        self.assertEqual(len(assignation_list), 1)
        assignation = assignation_list[0]

        # -- We want to plan it today, but it is shifted to this afternoon
        expected = [(datetime.datetime(2016, 5, 24, 14, 0), datetime.datetime(2016, 5, 24, 15, 45)),
                    (datetime.datetime(2016, 5, 25, 8, 30), datetime.datetime(2016, 5, 25, 10, 30)),
                    (datetime.datetime(2016, 5, 25, 14, 0), datetime.datetime(2016, 5, 25, 15, 45)),
                    (datetime.datetime(2016, 5, 26, 8, 30), datetime.datetime(2016, 5, 26, 10, 30)),
                    (datetime.datetime(2016, 5, 26, 14, 0), datetime.datetime(2016, 5, 26, 15, 45)),
                    (datetime.datetime(2016, 5, 27, 8, 30), datetime.datetime(2016, 5, 27, 10, 30)),
                    (datetime.datetime(2016, 5, 27, 14, 0), datetime.datetime(2016, 5, 27, 14, 45))]
        self._check_total_hours(expected, assigned_hours)
        intervals = self.assignation_accessor.plan_assignation(assignation.uid, tz_delta=tz_delta)
        self._check_total_hours(intervals, assigned_hours)
        LOG.debug("intervals:\n" + pprint.pformat(intervals, width=120))
        self.assertEqual(intervals, expected)
