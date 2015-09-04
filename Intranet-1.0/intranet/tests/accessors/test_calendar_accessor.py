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
from intranet.accessors.worked_hours.week_hours import WeekHoursAccessor
from intranet.accessors.worked_hours.calendar import CalendarAccessor
from intranet.model import DeclarativeBase
from intranet.model.worked_hours.calendar import Calendar

LOG = logging.getLogger(__name__)


class TestCalendarAccessor(unittest.TestCase):
    DEBUG = True

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

        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours("Open hours", "All year calendar")
        accessor.insert_week_hours("Summer calendar", "Open hours in summer")
        week_hours_list = accessor.get_week_hours_list()
        self.week_hours1 = week_hours_list[0]
        self.week_hours2 = week_hours_list[1]

    def test_setup(self):
        accessor = CalendarAccessor(self.session)

        # -- first setup
        week_hours_uid = self.week_hours1.uid
        accessor.setup(week_hours_uid)
        calendar_list = accessor.get_calendar_list()
        self.assertEqual(len(calendar_list), 1)

        accessor.setup(week_hours_uid)  # on second setup, do nothing
        self.assertEqual(len(calendar_list), 1)

    def test_delete_calendar(self):
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours = wh_accessor.get_by_label("Open hours")
        accessor = CalendarAccessor(self.session)
        accessor.insert_calendar(week_hours.uid, "Enterprise's calendar", "The normal calendar")
        calendar = accessor.get_by_label("Enterprise's calendar")
        accessor.delete_calendar(calendar.uid)
        with self.assertRaises(RecordNotFoundError) as context:
            accessor.delete_calendar(123)
        LOG.debug(context.exception)

    def test_get_calendar(self):
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer calendar")
        accessor = CalendarAccessor(self.session)
        accessor.insert_calendar(week_hours1.uid, "Enterprise's calendar", "The normal calendar")
        accessor.insert_calendar(week_hours2.uid, "Summer calendar", "Normal calendar in summer")
        (r1, r2) = accessor.get_calendar_list()
        calendar = accessor.get_calendar(r1.uid)
        self.assertEqual(calendar, r1)
        calendar = accessor.get_calendar(r2.uid)
        self.assertEqual(calendar, r2)
        with self.assertRaises(RecordNotFoundError):
            accessor.get_calendar(123)

    def test_insert_calendar(self):
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer calendar")
        accessor = CalendarAccessor(self.session)
        accessor.insert_calendar(week_hours1.uid, "label1", "Description1")
        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_calendar(week_hours2.uid, "label1", "Description2")
        LOG.debug(context.exception)

    def test_get_calendar_list(self):
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer calendar")

        accessor = CalendarAccessor(self.session)
        self.assertFalse(accessor.get_calendar_list())

        accessor.insert_calendar(week_hours1.uid, "label1", "Description1")
        accessor.insert_calendar(week_hours2.uid, "label2", "Description2")
        curr = accessor.get_calendar_list()
        self.assertEqual(curr[0].label, "label1")
        self.assertEqual(curr[1].label, "label2")

        curr = accessor.get_calendar_list(Calendar.label == "label2")
        self.assertEqual(len(curr), 1)
        self.assertEqual(curr[0].label, "label2")

        accessor.insert_calendar(week_hours2.uid, "label3", "Description3")
        curr = accessor.get_calendar_list(order_by_cond=desc(Calendar.label))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "label3")
        self.assertEqual(curr[1].label, "label2")
        self.assertEqual(curr[2].label, "label1")

        curr = accessor.get_calendar_list(order_by_cond=desc(Calendar.position))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "label3")
        self.assertEqual(curr[1].label, "label2")
        self.assertEqual(curr[2].label, "label1")

    def test_update_calendar(self):
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer calendar")

        accessor = CalendarAccessor(self.session)
        accessor.insert_calendar(week_hours1.uid, "label1", "Description1")
        calendar = accessor.get_by_label("label1")

        accessor.update_calendar(calendar.uid, position=12, label="new label", description="new description")
        curr = accessor.get_calendar(calendar.uid)
        self.assertEqual(curr.position, 12)
        self.assertEqual(curr.label, "new label")
        self.assertEqual(curr.description, "new description")

        accessor.insert_calendar(week_hours2.uid, "label2", "Description2")

        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_calendar(calendar.uid, label="label2")
        LOG.debug(context.exception)
