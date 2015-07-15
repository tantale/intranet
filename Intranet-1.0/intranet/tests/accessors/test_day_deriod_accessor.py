# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import unittest
import logging

from sqlalchemy import create_engine
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import desc
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors import RecordNotFoundError
from intranet.accessors.worked_hours.day_period import DayPeriodAccessor
from intranet.accessors.worked_hours.week_hours import WeekHoursAccessor
from intranet.model import DeclarativeBase
from intranet.model.worked_hours.day_period import DayPeriod

LOG = logging.getLogger(__name__)


class TestDayPeriodAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestDayPeriodAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestDayPeriodAccessor, self).setUp()

        # -- Connecting to the database
        engine = create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours(1, "Open hours", "All year open hours")
        accessor.insert_week_hours(2, "Summer open hours", "Open hours in summer")
        week_hours_list = accessor.get_week_hours_list()
        self.week_hours1 = week_hours_list[0]
        self.week_hours2 = week_hours_list[1]

    def test_setup(self):
        accessor = DayPeriodAccessor(self.session)

        # -- first setup
        accessor.setup()
        week_hours_accessor = WeekHoursAccessor(self.session)
        open_hours = week_hours_accessor.get_week_hours(1)
        self.assertEqual(len(open_hours.day_period_list), 2)

        # -- next setup...
        accessor.setup()  # must not raise
        open_hours = week_hours_accessor.get_week_hours(1)
        self.assertEqual(len(open_hours.day_period_list), 2)

    def test_get_day_period(self):
        accessor = DayPeriodAccessor(self.session)
        accessor.insert_day_period(self.week_hours1.uid, "Morning")

        curr = accessor.get_day_period(1)
        self.assertEqual(curr.label, "Morning")

        with self.assertRaises(RecordNotFoundError) as context:
            accessor.get_day_period(2)
        LOG.debug(context.exception)

    def test_get_day_period_list(self):
        accessor = DayPeriodAccessor(self.session)
        self.assertFalse(accessor.get_day_period_list())

        accessor.insert_day_period(self.week_hours1.uid, "Morning")
        accessor.insert_day_period(self.week_hours1.uid, "Afternoon")
        curr = accessor.get_day_period_list()
        self.assertEqual(curr[0].label, "Morning")
        self.assertEqual(curr[1].label, "Afternoon")

        curr = accessor.get_day_period_list(DayPeriod.label == "Morning")
        self.assertEqual(len(curr), 1)
        self.assertEqual(curr[0].label, "Morning")

        accessor.insert_day_period(self.week_hours1.uid, "Night")
        curr = accessor.get_day_period_list(order_by_cond=desc(DayPeriod.label))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "Night")
        self.assertEqual(curr[1].label, "Morning")
        self.assertEqual(curr[2].label, "Afternoon")

        curr = accessor.get_day_period_list(order_by_cond=desc(DayPeriod.position))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "Night")
        self.assertEqual(curr[1].label, "Afternoon")
        self.assertEqual(curr[2].label, "Morning")

    def test_insert_day_period(self):
        accessor = DayPeriodAccessor(self.session)
        accessor.insert_day_period(self.week_hours1.uid, "Morning")
        accessor.insert_day_period(self.week_hours1.uid, "Afternoon")
        accessor.insert_day_period(self.week_hours2.uid, "Morning")
        accessor.insert_day_period(self.week_hours2.uid, "Afternoon")
        accessor.insert_day_period(self.week_hours2.uid, "Night")

        # label is unique for this week_hours
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_day_period(self.week_hours1.uid, "Morning")
        LOG.debug(context.exception)

    def test_update_day_period(self):
        accessor = DayPeriodAccessor(self.session)

        accessor.insert_day_period(self.week_hours1.uid, "Morning")
        accessor.update_day_period(1, label="Afternoon")
        curr = accessor.get_day_period(1)
        self.assertEqual(curr.label, "Afternoon")

        accessor.insert_day_period(self.week_hours1.uid, "Morning")
        # label is unique for this week_hours
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_day_period(1, label="Morning")
        LOG.debug(context.exception)

    def test_delete_day_period(self):
        accessor = DayPeriodAccessor(self.session)
        accessor.insert_day_period(self.week_hours1.uid, "Morning")

        accessor.delete_day_period(1)
        self.assertFalse(accessor.get_day_period_list())

        with self.assertRaises(RecordNotFoundError) as context:
            accessor.get_day_period(2)
        LOG.debug(context.exception)

    def test_reorder_position(self):
        accessor = DayPeriodAccessor(self.session)
        accessor.insert_day_period(self.week_hours2.uid, "Night")
        accessor.insert_day_period(self.week_hours2.uid, "Morning")
        accessor.insert_day_period(self.week_hours2.uid, "Afternoon")
        expected = [2, 3, 1]
        accessor.reorder_position(expected)
        curr = [record.uid for record in accessor.get_day_period_list(order_by_cond=DayPeriod.position)]
        self.assertEqual(curr, expected)

    def test_cascade_delete(self):
        accessor = DayPeriodAccessor(self.session)
        accessor.insert_day_period(self.week_hours1.uid, "Morning")
        accessor.insert_day_period(self.week_hours1.uid, "Afternoon")
        accessor.insert_day_period(self.week_hours2.uid, "Morning")
        accessor.insert_day_period(self.week_hours2.uid, "Afternoon")
        accessor.insert_day_period(self.week_hours2.uid, "Night")

        week_hours_accessor = WeekHoursAccessor(self.session)
        week_hours_accessor.delete_week_hours(self.week_hours1.uid)

        day_period_list = accessor.get_day_period_list()
        self.assertEqual(day_period_list, week_hours_accessor.get_week_hours(2).day_period_list)
