# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import datetime
import logging
import pprint
import random
import sys
import unittest

import sqlalchemy
import sqlalchemy.exc
import transaction
from sqlalchemy.orm import sessionmaker

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.pointage.cal_event import CalEventAccessor
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.pointage.order import OrderAccessor
from intranet.model import *

LOG = logging.getLogger(__name__)


class TestOrderAccessor(unittest.TestCase):
    DEBUG = True

    @classmethod
    def setUpClass(cls):
        super(TestOrderAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestOrderAccessor, self).setUp()

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

        # -- Create a Employee
        self.employee_accessor = EmployeeAccessor(self.session)
        for employee_name in ["Pierre", "Paul", "Jacques", "Marie", "Alice", "Margaux"]:
            worked_hours = 39.0
            entry_date = datetime.date(2010, 11, 15)
            self.employee_accessor.insert_employee(employee_name=employee_name,
                                                   worked_hours=worked_hours,
                                                   entry_date=entry_date,
                                                   exit_date=None,
                                                   photo_path=None)

        self.order_accessor = OrderAccessor(self.session)

    def test_get_order_by_ref_NoResultFound(self):
        with self.assertRaises(sqlalchemy.orm.exc.NoResultFound):
            self.order_accessor.get_order_by_ref("Missing")

    def test_get_order_by_ref_MultipleResultsFound(self):
        self.order_accessor.insert_order(order_ref="Duplicate",
                                         project_cat="project_cat1",
                                         creation_date=datetime.date(2015, 10, 1),
                                         close_date=None)
        self.order_accessor.insert_order(order_ref="Duplicate",
                                         project_cat="project_cat2",
                                         creation_date=datetime.date(2015, 10, 3),
                                         close_date=None)
        with self.assertRaises(sqlalchemy.orm.exc.MultipleResultsFound):
            self.order_accessor.get_order_by_ref("Duplicate")

    def test_get_order_by_ref(self):
        self.order_accessor.insert_order(order_ref="my first order_ref",
                                         project_cat="project_cat",
                                         creation_date=datetime.date(2015, 10, 1),
                                         close_date=None)
        self.order_accessor.insert_order(order_ref="my second order_ref",
                                         project_cat="project_cat1",
                                         creation_date=datetime.date(2015, 10, 2),
                                         close_date=None)
        first = self.order_accessor.get_order_by_ref("my first order_ref")
        self.assertEqual(first.order_ref, "my first order_ref")
        second = self.order_accessor.get_order_by_ref("my second order_ref")
        self.assertEqual(second.order_ref, "my second order_ref")

    def test_prepare_planning(self):

        # -- Create a "old" Order with tracked time
        orders = [dict(order_ref="Order#{0}".format(n),
                       project_cat="project_cat",
                       creation_date=datetime.date(2015, 10, 1) + datetime.timedelta(days=n),
                       close_date=datetime.date(2015, 11, 16) + datetime.timedelta(days=n))
                  for n in range(100)]
        for order in orders:
            self.order_accessor.insert_order(**order)

        self.cal_event_accessor = CalEventAccessor(self.session)
        try:
            employees = self.employee_accessor.get_employee_list()
            for order in self.order_accessor.get_order_list():
                for order_phase in order.order_phase_list:
                    for times in xrange(random.randrange(10)):
                        # choose a day between creation_date and close_date
                        period = order.close_date - order.creation_date
                        days = random.randrange(period.days)
                        # choose start and end hours
                        hour_start = random.randrange(8, 19)
                        hour_end = random.randrange(hour_start, 19)
                        tracked_date = datetime.datetime.combine(order.creation_date, datetime.time(0))
                        event_start = tracked_date + datetime.timedelta(days=days, hours=hour_start)
                        event_end = tracked_date + datetime.timedelta(days=days, hours=hour_end)
                        cal_event = CalEvent(event_start, event_end, comment=u"")
                        cal_event.employee = random.choice(employees)
                        cal_event.order_phase = order_phase
                        self.session.add(cal_event)
            transaction.commit()
        except:
            transaction.abort()
            raise

        # -- Create a "new" Order without tracked time
        self.order_accessor.insert_order(order_ref="NewOrder",
                                         project_cat="project_cat",
                                         creation_date=datetime.date(2016, 1, 21),
                                         close_date=None)

        LOG.info("Estimate OrderPhase duration...")
        new_order = self.order_accessor.get_order_list(Order.order_ref == "NewOrder")[0]

        order_uid = new_order.uid
        self.order_accessor.estimate_duration(order_uid, closed=True)

        new_order = self.order_accessor.get_order(order_uid)
        for order_phase in new_order.order_phase_list:
            LOG.info("{label}: {duration}".format(label=order_phase.label, duration=order_phase.estimated_duration))

    def test_plan_all_closed(self):
        order_ref = "my_order_ref"
        self.order_accessor.insert_order(order_ref=order_ref,
                                         project_cat="my_project_cat",
                                         creation_date=datetime.date(2016, 7, 6),
                                         close_date=datetime.date(2016, 7, 14))
        order_uid = self.order_accessor.get_order_by_ref(order_ref).uid
        shifts = self.order_accessor.plan_order(order_uid, tz_delta=datetime.timedelta())
        # -- close Order can't be planned => no shift
        self.assertEqual(len(shifts), 0)

    def test_plan_all(self):
        # -- First create an Order with OrderPhase
        order_ref = "my_order_ref"
        try:
            order = Order(order_ref=order_ref,
                          project_cat="my_project_cat",
                          creation_date=datetime.date(2016, 7, 6))

            task1 = OrderPhase(1, "task1", "estimated_duration = 0.0")
            task1.estimated_duration = 0.0
            order.order_phase_list.append(task1)

            task2 = OrderPhase(2, "task2", "estimated_duration = 2.0")
            task2.estimated_duration = 2.0
            order.order_phase_list.append(task2)

            task3 = OrderPhase(3, "task3", "single assignation")
            task3.estimated_duration = 5.0
            order.order_phase_list.append(task3)

            task4 = OrderPhase(4, "task4", "multiple assignation")
            task4.estimated_duration = 5.0
            order.order_phase_list.append(task4)

            task5 = OrderPhase(5, "task5", "single assignation")
            task5.estimated_duration = 5.0
            order.order_phase_list.append(task5)

            task6 = OrderPhase(6, "task6", "single assignation")
            task6.estimated_duration = 10.0
            order.order_phase_list.append(task6)

            self.session.add(order)
            self.session.flush()

            task3_assign1_dt = datetime.datetime(2016, 7, 11, 12, 0)
            task3_assign1 = Assignation(5.0, 1.0, task3_assign1_dt)
            task3_assign1.employee = self.employee_accessor.get_employee_by_name("Pierre")
            task3.assignation_list.append(task3_assign1)

            task4_assign1_dt = datetime.datetime(2016, 7, 11, 12, 0)
            task4_assign1 = Assignation(3.0, 1.0, task4_assign1_dt)
            task4_assign1.employee = self.employee_accessor.get_employee_by_name("Pierre")
            task4.assignation_list.append(task4_assign1)
            task4_assign2_dt = datetime.datetime(2016, 7, 12, 8, 0)
            task4_assign2 = Assignation(2.0, 1.0, task4_assign2_dt)
            task4_assign2.employee = self.employee_accessor.get_employee_by_name("Marie")
            task4.assignation_list.append(task4_assign2)

            task5_assign1_dt = datetime.datetime(2016, 7, 15)
            task5_assign1 = Assignation(5.0, 1.0, task5_assign1_dt)
            task5_assign1.employee = self.employee_accessor.get_employee_by_name("Alice")
            task5.assignation_list.append(task5_assign1)

            task6_assign1_dt = datetime.datetime(2016, 6, 15)
            task6_assign1 = Assignation(10.0, 1.0, task6_assign1_dt)
            task6_assign1.employee = self.employee_accessor.get_employee_by_name("Margaux")
            task6.assignation_list.append(task6_assign1)

            transaction.commit()
        except:
            transaction.abort()
            raise

        order_uid = self.order_accessor.get_order_by_ref(order_ref).uid

        # -- check the shifts
        shifts = self.order_accessor.plan_order(order_uid, tz_delta=datetime.timedelta())

        try:
            # task1 and task2 can't be planned => only 4 shifts
            self.assertEqual(len(shifts), 4)

            # shift must start after assignation date
            shift3, shift4, shift5, shift6 = shifts
            self.assertGreaterEqual(shift3[0], task3_assign1_dt)
            self.assertGreaterEqual(shift4[0], task4_assign1_dt)
            self.assertGreaterEqual(shift4[0], task4_assign2_dt)
            self.assertGreaterEqual(shift5[0], task5_assign1_dt)
            self.assertGreaterEqual(shift6[0], task6_assign1_dt)

            # shifts must be chronologically ordered
            for prev_shift, next_shift in zip(shifts[:-1], shifts[1:]):
                prev_date_end = prev_shift[1]
                next_date_start = next_shift[0]
                self.assertLessEqual(prev_date_end, next_date_start)

            expected = [(datetime.datetime(2016, 7, 11, 14, 0), datetime.datetime(2016, 7, 12, 9, 45)),
                        (datetime.datetime(2016, 7, 12, 9, 45), datetime.datetime(2016, 7, 12, 17, 0)),
                        (datetime.datetime(2016, 7, 15, 8, 30), datetime.datetime(2016, 7, 15, 15, 0)),
                        (datetime.datetime(2016, 7, 15, 15, 0), datetime.datetime(2016, 7, 18, 17, 30))]
            self.assertEqual(shifts, expected)

        except AssertionError:
            pprint.pprint(shifts, width=120, stream=sys.stderr)
            raise
