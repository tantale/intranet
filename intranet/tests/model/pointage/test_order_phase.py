# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import datetime
import logging
import unittest

import transaction
from sqlalchemy import create_engine

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.planning_event import PlanningEventAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.pointage.assignation import AssignationAccessor
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.pointage.order import OrderAccessor
from intranet.model import *
from intranet.model.pointage.order_phase import STATUS_DONE, STATUS_IN_PROGRESS, STATUS_PENDING

LOG = logging.getLogger(__name__)


class TestFrequencyAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestFrequencyAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestFrequencyAccessor, self).setUp()

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

        order_ref = "My order_ref"
        project_cat = "My project_cat"
        creation_date = datetime.datetime(2016, 2, 14, 12, 30)
        self.order_accessor = OrderAccessor(self.session)
        self.order_accessor.insert_order(order_ref=order_ref,
                                         project_cat=project_cat,
                                         creation_date=creation_date)

        self.planning_event_accessor = PlanningEventAccessor(self.session)
        self.assignation_accessor = AssignationAccessor(self.session)

        self.employee_accessor = EmployeeAccessor(self.session)
        employees = ["Pierre", "Paul", "Jacques"]
        for employee in employees:
            self.employee_accessor.insert_employee(employee_name=employee,
                                                   worked_hours=39.0,
                                                   entry_date=datetime.datetime(2011, 2, 14, 12, 30),
                                                   exit_date=None,
                                                   photo_path=None)

    def _get_order_by_ref(self, order_ref):
        return self.order_accessor.get_order_by_ref(order_ref)

    def _get_employee_by_name(self, employee_name):
        return self.employee_accessor.get_employee_by_name(employee_name)

    def test_plan_status_info(self):
        order = self._get_order_by_ref("My order_ref")
        task = order.order_phase_list[0]
        assert isinstance(task, OrderPhase)

        # -- Terminée
        task.task_status = STATUS_DONE
        info = task.plan_status_info
        self.assertFalse(info["can_plan"])
        self.assertEqual(info["label"], "Terminée")

        # -- Non estimée
        task.task_status = STATUS_IN_PROGRESS
        task.estimated_duration = 0
        info = task.plan_status_info
        self.assertFalse(info["can_plan"])
        self.assertEqual(info["label"], "Non estimée")

        # -- Non affectée
        task.estimated_duration = 10.5
        task.assignation_list = []
        info = task.plan_status_info
        self.assertFalse(info["can_plan"])
        self.assertEqual(info["label"], "Non affectée")

        # -- À planifier 1
        task.assignation_list.append(Assignation(10.5, 1.0, datetime.datetime(2016, 7, 13, 12, 30)))
        info = task.plan_status_info
        self.assertTrue(info["can_plan"])
        self.assertEqual(info["label"], "À planifier")

        # -- Déjà planifiée 1
        assignation = task.assignation_list[0]
        assignation.planning_event_list.append(PlanningEvent("event1",
                                                             "My event1",
                                                             datetime.datetime(2016, 7, 13, 13, 0),
                                                             datetime.datetime(2016, 7, 13, 14, 0)))
        info = task.plan_status_info
        self.assertFalse(info["can_plan"])
        self.assertEqual(info["label"], "Déjà planifiée")

        # -- Partiellement planifiée 2
        task.assignation_list.append(Assignation(15, .8, datetime.datetime(2016, 7, 13, 12, 30)))
        info = task.plan_status_info
        self.assertTrue(info["can_plan"])
        self.assertEqual(info["label"], "Partiellement planifiée")

        # -- Déjà planifiée 2
        assignation = task.assignation_list[1]
        assignation.planning_event_list.append(PlanningEvent("event1",
                                                             "My event1",
                                                             datetime.datetime(2016, 7, 13, 14, 0),
                                                             datetime.datetime(2016, 7, 13, 15, 0)))
        info = task.plan_status_info
        self.assertFalse(info["can_plan"])
        self.assertEqual(info["label"], "Déjà planifiée")

    def test_plan_task(self):
        with transaction.manager:
            order = self._get_order_by_ref("My order_ref")
            task = order.order_phase_list[0]
            task.task_status = STATUS_PENDING
            task.estimated_duration = 30
            task_uid = task.uid
            transaction.commit()

        pierre_uid = self._get_employee_by_name("Pierre").uid
        paul_uid = self._get_employee_by_name("Paul").uid
        jacques_uid = self._get_employee_by_name("Jacques").uid

        # Pierre peut travailler 5 heures à partir du mercredi 17/02/2016 => 8h30
        self.assignation_accessor.insert_assignation(pierre_uid, task_uid,
                                                     5.0, 1, datetime.datetime(2016, 2, 17), None)
        # Paul peut travailler 10 heures à partir du mardi 16/02/2016 => 8h30
        self.assignation_accessor.insert_assignation(paul_uid, task_uid,
                                                     10.0, 1, datetime.datetime(2016, 2, 16), None)
        # Jacques peut travailler 15 heures à partir du lundi 15/02/2016 => 14h00
        self.assignation_accessor.insert_assignation(jacques_uid, task_uid,
                                                     15.0, 1, datetime.datetime(2016, 2, 15), None)

        # -- Plan Paul's assignation
        order = self._get_order_by_ref("My order_ref")
        task = order.order_phase_list[0]
        assignation_uid = task.assignation_list[1].uid  # Paul
        tz_delta = datetime.timedelta()
        self.assignation_accessor.plan_assignation(assignation_uid, tz_delta=tz_delta)

        # => Paul est planifié du mardi 16/02/2016 8h30 au mercredi 17/02/2016 10h45 (soit 10h de travail)
        assignation = self.assignation_accessor.get_assignation(assignation_uid)
        self.assertEqual(assignation.start_planning_date, datetime.datetime(2016, 2, 16, 8, 30))
        self.assertEqual(assignation.end_planning_date, datetime.datetime(2016, 2, 17, 10, 45))
        self.assertEqual(assignation.total_duration, 10.0)

        # -- Plan the task
        with transaction.manager:
            order = self._get_order_by_ref("My order_ref")
            task = order.order_phase_list[0]
            assert isinstance(task, OrderPhase)
            shifts = task.plan_task(tz_delta=tz_delta)
            transaction.commit()

        expected = [(datetime.datetime(2016, 2, 17, 8, 30), datetime.datetime(2016, 2, 17, 15, 0)),  # Pierre
                    (datetime.datetime(2016, 2, 15, 14, 00), datetime.datetime(2016, 2, 17, 12, 0))]  # Jacques
        self.assertEqual(shifts, expected)
