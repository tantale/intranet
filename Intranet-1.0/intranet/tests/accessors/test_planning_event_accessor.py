# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import unittest
import logging
import datetime

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import and_
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors import RecordNotFoundError
from intranet.accessors.planning.planning_event import PlanningEventAccessor
from intranet.model import DeclarativeBase
from intranet.model.planning.planning_event import PlanningEvent

LOG = logging.getLogger(__name__)


class TestPlanningEventAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestPlanningEventAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestPlanningEventAccessor, self).setUp()

        # -- Connecting to the database
        engine = create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

        # -- Init the main accessor
        self.accessor = PlanningEventAccessor(self.session)

        # -- Create a calendar
        week_hours_accessor = self.accessor.calendar_accessor.week_hours_accessor
        week_hours_accessor.insert_week_hours("Week Hours", "Description of my week hours")
        week_hours = week_hours_accessor.get_by_label("Week Hours")
        calendar_accessor = self.accessor.calendar_accessor
        calendar_accessor.insert_calendar(week_hours.uid, "Main Calendar", "Description of my calendar")
        calendar = calendar_accessor.get_by_label("Main Calendar")
        self.calendar_uid = calendar.uid

    def test_setup(self):
        self.accessor.setup()

    def test_get_calendar(self):
        calendar = self.accessor.get_calendar(1)
        self.assertEqual(calendar.label, "Main Calendar")

    def test_delete_planning_event(self):
        event_start = datetime.datetime.utcnow()
        event_end = event_start + datetime.timedelta(hours=1)
        self.accessor.insert_planning_event(self.calendar_uid, "Meeting", None,
                                            event_start=event_start,
                                            event_end=event_end)
        filter_cond = and_(PlanningEvent.calendar_uid == self.calendar_uid, PlanningEvent.event_start == event_start,
                           PlanningEvent.event_end == event_end)
        all_events = self.accessor.get_planning_event_list(filter_cond)
        self.assertEqual(len(all_events), 1)
        first = all_events[0]
        self.accessor.delete_planning_event(first.uid)
        all_events = self.accessor.get_planning_event_list(filter_cond)
        self.assertEqual(len(all_events), 0)

        with self.assertRaises(RecordNotFoundError) as context:
            self.accessor.delete_planning_event(123)
        LOG.info(context.exception)

    def test_get_planning_event(self):
        event_start = datetime.datetime.utcnow()
        event_end = event_start + datetime.timedelta(hours=1)
        self.accessor.insert_planning_event(self.calendar_uid, "Meeting", None,
                                            event_start=event_start,
                                            event_end=event_end,
                                            location="At home",
                                            private=True)
        filter_cond = and_(PlanningEvent.calendar_uid == self.calendar_uid, PlanningEvent.event_start == event_start,
                           PlanningEvent.event_end == event_end)
        all_events = self.accessor.get_planning_event_list(filter_cond)
        self.assertEqual(len(all_events), 1)
        first = all_events[0]
        clone = self.accessor.get_planning_event(first.uid)
        self.assertEqual(first, clone)

        with self.assertRaises(RecordNotFoundError) as context:
            self.accessor.get_planning_event(123)
        LOG.info(context.exception)

    def test_insert_planning_event(self):
        event_start = datetime.datetime.utcnow()
        event_end = event_start + datetime.timedelta(hours=1)
        self.accessor.insert_planning_event(self.calendar_uid, "Meeting", None,
                                            event_start=event_start,
                                            event_end=event_end,
                                            location="At home",
                                            private=True)

        with self.assertRaises(IntegrityError) as context:
            self.accessor.insert_planning_event(self.calendar_uid, "Meeting", None,
                                                event_start=event_end,
                                                event_end=event_start)
        LOG.info(context.exception)

    def test_get_planning_event_list(self):
        all_events = self.accessor.get_planning_event_list()
        self.assertFalse(all_events)

        event_start = datetime.datetime.utcnow()
        event_end = event_start + datetime.timedelta(hours=1)
        self.accessor.insert_planning_event(self.calendar_uid, "Meeting", None,
                                            event_start=event_start,
                                            event_end=event_end,
                                            location="At home",
                                            private=True)
        all_events = self.accessor.get_planning_event_list()
        self.assertEqual(len(all_events), 1)

    def test_update_planning_event(self):
        event_start = datetime.datetime.utcnow()
        event_end = event_start + datetime.timedelta(hours=1)
        self.accessor.insert_planning_event(self.calendar_uid, "Meeting", "My meeting today",
                                            event_start=event_start,
                                            event_end=event_end,
                                            location="At home",
                                            private=True)
        first_uid = self.accessor.get_planning_event_list()[0].uid

        # -- calendar_uid required
        with self.assertRaises(IntegrityError) as context:
            self.accessor.update_planning_event(first_uid, calendar_uid=None)
        LOG.info(context.exception)

        # -- label required
        with self.assertRaises(IntegrityError) as context:
            self.accessor.update_planning_event(first_uid, label=None)
        LOG.info(context.exception)

        # -- description optional
        self.accessor.update_planning_event(first_uid, description=None)
        planning_event = self.accessor.get_planning_event(first_uid)
        self.assertIsNone(planning_event.description)

        # -- event_start required
        with self.assertRaises(IntegrityError) as context:
            self.accessor.update_planning_event(first_uid, event_start=None)
        LOG.info(context.exception)

        # -- event_end required
        with self.assertRaises(IntegrityError) as context:
            self.accessor.update_planning_event(first_uid, event_end=None)
        LOG.info(context.exception)

        # -- start_before_end_check
        with self.assertRaises(IntegrityError) as context:
            self.accessor.update_planning_event(first_uid, event_start=event_end, event_end=event_start)
        LOG.info(context.exception)

        # -- editable required
        with self.assertRaises(IntegrityError) as context:
            self.accessor.update_planning_event(first_uid, editable=None)
        LOG.info(context.exception)

        # -- all_day required
        with self.assertRaises(IntegrityError) as context:
            self.accessor.update_planning_event(first_uid, all_day=None)
        LOG.info(context.exception)

        # -- location optional
        self.accessor.update_planning_event(first_uid, location=None)
        planning_event = self.accessor.get_planning_event(first_uid)
        self.assertIsNone(planning_event.location)

        # -- private required
        with self.assertRaises(IntegrityError) as context:
            self.accessor.update_planning_event(first_uid, private=None)
        LOG.info(context.exception)

    def test_increase_duration(self):
        event_start = datetime.datetime.utcnow()
        event_end = event_start + datetime.timedelta(hours=1)
        self.accessor.insert_planning_event(self.calendar_uid, "Meeting", "My meeting today",
                                            event_start=event_start,
                                            event_end=event_end)
        first_uid = self.accessor.get_planning_event_list()[0].uid

        self.accessor.increase_duration(first_uid, datetime.timedelta(minutes=30))
        planning_event = self.accessor.get_planning_event(first_uid)
        self.assertEqual(planning_event.event_start, event_start)
        self.assertEqual(planning_event.event_end, event_start + datetime.timedelta(hours=1, minutes=30))

    def test_move_datetime(self):
        event_start = datetime.datetime.utcnow()
        event_end = event_start + datetime.timedelta(hours=1)
        self.accessor.insert_planning_event(self.calendar_uid, "Meeting", "My meeting today",
                                            event_start=event_start,
                                            event_end=event_end)
        first_uid = self.accessor.get_planning_event_list()[0].uid

        timedelta = datetime.timedelta(days=2)
        self.accessor.move_datetime(first_uid, timedelta)
        planning_event = self.accessor.get_planning_event(first_uid)
        self.assertEqual(planning_event.event_start, event_start + timedelta)
        self.assertEqual(planning_event.event_end, event_end + timedelta)

    def test_calendar_delete(self):
        event_start = datetime.datetime.utcnow()
        event_end = event_start + datetime.timedelta(hours=1)
        self.accessor.insert_planning_event(self.calendar_uid, "Meeting", "My meeting today",
                                            event_start=event_start,
                                            event_end=event_end)
        event_start += + datetime.timedelta(hours=13)
        event_end = event_start + datetime.timedelta(days=1)
        self.accessor.insert_planning_event(self.calendar_uid, "New Meeting", "My new meeting today",
                                            event_start=event_start,
                                            event_end=event_end, all_day=True)
        event_list = self.accessor.get_planning_event_list()
        self.assertEqual(len(event_list), 2)

        self.accessor.calendar_accessor.delete_calendar(self.calendar_uid)
        event_list = self.accessor.get_planning_event_list()
        self.assertEqual(len(event_list), 0)
