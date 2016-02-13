# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import logging
import unittest

import sqlalchemy.exc
import sqlalchemy.orm.exc
import transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import desc
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors import RecordNotFoundError
from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.model import DeclarativeBase
from intranet.model.planning.week_hours import WeekHours

LOG = logging.getLogger(__name__)


class TestWeekHoursAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestWeekHoursAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestWeekHoursAccessor, self).setUp()

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

    def test_setup(self):
        accessor = WeekHoursAccessor(self.session)
        accessor.setup()  # on second setup, do nothing

    def test_delete_week_hours(self):
        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours("label1", "Description1")
        accessor.delete_week_hours(1)
        with self.assertRaises(RecordNotFoundError) as context:
            accessor.delete_week_hours(123)
        LOG.debug(context.exception)

    def test_get_week_hours(self):
        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours("label1", "Description1")
        accessor.insert_week_hours("label2", "Description2")
        week_hours_list = accessor.get_week_hours_list()
        (r1, r2) = week_hours_list[:2]
        week_hours = accessor.get_week_hours(r1.uid)
        self.assertEqual(week_hours, r1)
        week_hours = accessor.get_week_hours(r2.uid)
        self.assertEqual(week_hours, r2)
        with self.assertRaises(RecordNotFoundError):
            accessor.get_week_hours(123)

    def test_insert_week_hours(self):
        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours("label1", "Description1")

        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_week_hours("label1", "Description2")
        transaction.abort()
        LOG.debug(context.exception)

    def test_get_week_hours_list(self):
        accessor = WeekHoursAccessor(self.session)

        # cleanup before testing
        week_hours_list = accessor.get_week_hours_list()
        for week_hours in week_hours_list:
            accessor.delete_week_hours(week_hours.uid)

        accessor.insert_week_hours("label1", "Description1")
        accessor.insert_week_hours("label2", "Description2")
        curr = accessor.get_week_hours_list()
        self.assertEqual(curr[0].label, "label1")
        self.assertEqual(curr[1].label, "label2")

        curr = accessor.get_week_hours_list(WeekHours.label == "label2")
        self.assertEqual(len(curr), 1)
        self.assertEqual(curr[0].label, "label2")

        accessor.insert_week_hours("label3", "Description3")
        curr = accessor.get_week_hours_list(order_by_cond=desc(WeekHours.label))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "label3")
        self.assertEqual(curr[1].label, "label2")
        self.assertEqual(curr[2].label, "label1")

        curr = accessor.get_week_hours_list(order_by_cond=desc(WeekHours.position))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "label3")
        self.assertEqual(curr[1].label, "label2")
        self.assertEqual(curr[2].label, "label1")

    def test_update_week_hours(self):
        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours("label1", "Description1")
        uid = 1

        accessor.update_week_hours(uid, position=12, label="new label", description="new description")
        curr = accessor.get_week_hours(uid)
        self.assertEqual(curr.position, 12)
        self.assertEqual(curr.label, "new label")
        self.assertEqual(curr.description, "new description")

        accessor.insert_week_hours("label2", "Description2")

        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_week_hours(uid, label="label2")
        transaction.abort()
        LOG.debug(context.exception)

    def test_get_by_label(self):
        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours("label1", "Description1")
        week_hours = accessor.get_by_label("label1")
        self.assertEqual(week_hours.label, "label1")
        with self.assertRaises(sqlalchemy.orm.exc.NoResultFound) as context:
            accessor.get_by_label("unknown")

    def test_get_hours_intervals(self):
        week_hours_accessor = WeekHoursAccessor(self.session)
        week_hours_accessor.insert_week_hours("label1", "Description1")
        week_hours = week_hours_accessor.get_by_label("label1")

        for iso_weekday in [1, 2, 3, 4, 5, 6, 7]:
            hours_intervals = week_hours.get_hours_intervals(iso_weekday)
            print(hours_intervals)
