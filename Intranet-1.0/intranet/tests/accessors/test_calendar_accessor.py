# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging
import unittest

import sqlalchemy
import sqlalchemy.exc
import transaction
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import desc
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors import RecordNotFoundError
from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.planning_event import PlanningEventAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.model import DeclarativeBase
from intranet.model.planning.calendar import Calendar

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
        # noinspection SpellCheckingInspection
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

    def test_setup(self):
        week_hours_accessor = WeekHoursAccessor(self.session)
        calendar_accessor = CalendarAccessor(self.session)
        week_hours_list = week_hours_accessor.get_week_hours_list()
        for week_hours in week_hours_list:
            calendar_accessor.setup(week_hours.uid)  # second setup

    def test_delete_calendar(self):
        calendar_accessor = CalendarAccessor(self.session)
        calendar_list = calendar_accessor.get_calendar_list()
        calendar = calendar_list[0]
        calendar_accessor.delete_calendar(calendar.uid)
        with self.assertRaises(RecordNotFoundError) as context:
            calendar_accessor.delete_calendar(123)
        LOG.debug(context.exception)

    def test_get_calendar(self):
        wh_accessor = WeekHoursAccessor(self.session)
        wh_accessor.insert_week_hours("Open hours", "Open hours")
        wh_accessor.insert_week_hours("Summer calendar", "Summer calendar")
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer calendar")
        accessor = CalendarAccessor(self.session)
        accessor.insert_calendar(week_hours1.uid, "Enterprise's calendar", "The normal calendar")
        accessor.insert_calendar(week_hours2.uid, "Summer calendar", "Normal calendar in summer")
        calendar_list = accessor.get_calendar_list()
        (r1, r2) = calendar_list[:2]
        calendar = accessor.get_calendar(r1.uid)
        self.assertEqual(calendar, r1)
        calendar = accessor.get_calendar(r2.uid)
        self.assertEqual(calendar, r2)
        with self.assertRaises(RecordNotFoundError):
            accessor.get_calendar(123)

    def test_insert_calendar(self):
        wh_accessor = WeekHoursAccessor(self.session)
        wh_accessor.insert_week_hours("Open hours", "Open hours")
        wh_accessor.insert_week_hours("Summer calendar", "Summer calendar")
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer calendar")
        accessor = CalendarAccessor(self.session)
        accessor.insert_calendar(week_hours1.uid, "label1", "Description1")
        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_calendar(week_hours2.uid, "label1", "Description2")
        LOG.debug(context.exception)
        transaction.abort()
        # label not NULL
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            # noinspection PyTypeChecker
            accessor.insert_calendar(week_hours2.uid, None, "Description3")
        transaction.abort()
        LOG.debug(context.exception)
        accessor.insert_calendar(week_hours1.uid, "label4", "Description4")

    def test_get_calendar_list(self):
        wh_accessor = WeekHoursAccessor(self.session)
        wh_accessor.insert_week_hours("Open hours", "Open hours")
        wh_accessor.insert_week_hours("Summer calendar", "Summer calendar")
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer calendar")

        accessor = CalendarAccessor(self.session)
        # drop all calendar for testing
        for calendar in accessor.get_calendar_list():
            accessor.delete_calendar(calendar.uid)

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
        wh_accessor.insert_week_hours("Open hours", "Open hours")
        wh_accessor.insert_week_hours("Summer calendar", "Summer calendar")
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
        transaction.abort()
        LOG.debug(context.exception)

    def test_get_free_intervals(self):
        calendar_accessor = CalendarAccessor(self.session)
        calendar_list = calendar_accessor.get_calendar_list()
        calendar = calendar_list[0]

        expected = [[(datetime.time(14, 0), datetime.time(17, 45))],
                    [(datetime.time(8, 30), datetime.time(12, 30)), (datetime.time(14, 0), datetime.time(17, 45))],
                    [(datetime.time(8, 30), datetime.time(12, 30)), (datetime.time(14, 0), datetime.time(17, 45))],
                    [(datetime.time(8, 30), datetime.time(12, 30)), (datetime.time(14, 0), datetime.time(17, 45))],
                    [(datetime.time(8, 30), datetime.time(12, 30)), (datetime.time(14, 0), datetime.time(17, 30))],
                    [(datetime.time(8, 30), datetime.time(12, 30))],
                    []]

        today = datetime.date.today()
        for index in xrange(len(expected)):
            day = today + datetime.timedelta(days=index)
            current = calendar.get_free_intervals(day)
            iso_weekday = day.isoweekday()
            self.assertEqual(expected[iso_weekday - 1], current)

    def test_get_busy_intervals(self):
        calendar_accessor = CalendarAccessor(self.session)
        calendar_list = calendar_accessor.get_calendar_list()
        calendar = calendar_list[0]
        today = datetime.date.today()

        # I have some meeting today
        accessor = PlanningEventAccessor(self.session)

        event_start = datetime.datetime.combine(today, datetime.time(8, 30))
        event_end = event_start + datetime.timedelta(hours=1)
        accessor.insert_planning_event(calendar.uid, "event1", "description1", event_start, event_end)

        event_start = datetime.datetime.combine(today, datetime.time(10, 0))
        event_end = event_start + datetime.timedelta(hours=1.5)
        accessor.insert_planning_event(calendar.uid, "event2", "description2", event_start, event_end)

        event_start = datetime.datetime.combine(today, datetime.time(22, 35))
        event_end = event_start + datetime.timedelta(hours=3)
        accessor.insert_planning_event(calendar.uid, "event3", "description3", event_start, event_end)

        # Am I so busy?
        calendar = calendar_accessor.get_calendar(calendar.uid)
        intervals = calendar.get_busy_intervals(today, tz_delta=datetime.timedelta())
        LOG.debug(intervals)
        expected = [(datetime.time(8, 30), datetime.time(9, 30)),
                    (datetime.time(10, 0), datetime.time(11, 30)),
                    (datetime.time(22, 35), datetime.time(0, 0))]  # truncated
        self.assertEqual(expected, intervals)

    def test_get_available_intervals(self):
        calendar_accessor = CalendarAccessor(self.session)
        calendar_list = calendar_accessor.get_calendar_list()
        calendar = calendar_list[0]
        today = datetime.date(2016, 2, 13)  # Saturday

        # I have some meeting today
        accessor = PlanningEventAccessor(self.session)

        event_start = datetime.datetime.combine(today, datetime.time(8, 30))
        event_end = event_start + datetime.timedelta(hours=1)
        accessor.insert_planning_event(calendar.uid, "event1", "description1", event_start, event_end)

        event_start = datetime.datetime.combine(today, datetime.time(10, 0))
        event_end = event_start + datetime.timedelta(hours=1.5)
        accessor.insert_planning_event(calendar.uid, "event2", "description2", event_start, event_end)

        event_start = datetime.datetime.combine(today, datetime.time(22, 35))
        event_end = event_start + datetime.timedelta(hours=3)
        accessor.insert_planning_event(calendar.uid, "event3", "description3", event_start, event_end)

        # Any time slot available today?
        calendar = calendar_accessor.get_calendar(calendar.uid)
        intervals = calendar.get_available_intervals(today, tz_delta=datetime.timedelta())
        LOG.debug(intervals)
        expected = [(datetime.time(9, 30), datetime.time(10, 0)),
                    (datetime.time(11, 30), datetime.time(12, 30))]
        self.assertEqual(expected, intervals)
