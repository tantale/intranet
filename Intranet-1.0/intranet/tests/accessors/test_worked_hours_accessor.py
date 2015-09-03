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
from intranet.accessors.worked_hours.worked_hours import WorkedHoursAccessor
from intranet.model import DeclarativeBase
from intranet.model.worked_hours.worked_hours import WorkedHours

LOG = logging.getLogger(__name__)


class TestWorkedHoursAccessor(unittest.TestCase):
    DEBUG = True

    @classmethod
    def setUpClass(cls):
        super(TestWorkedHoursAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestWorkedHoursAccessor, self).setUp()

        # -- Connecting to the database
        engine = create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours("Open hours", "All year open hours")
        accessor.insert_week_hours("Summer open hours", "Open hours in summer")
        week_hours_list = accessor.get_week_hours_list()
        self.week_hours1 = week_hours_list[0]
        self.week_hours2 = week_hours_list[1]

    def test_setup(self):
        accessor = WorkedHoursAccessor(self.session)

        # -- first setup
        week_hours_uid = self.week_hours1.uid
        accessor.setup(week_hours_uid)
        worked_hours_list = accessor.get_worked_hours_list()
        self.assertEqual(len(worked_hours_list), 1)

        accessor.setup(week_hours_uid)  # on second setup, do nothing
        self.assertEqual(len(worked_hours_list), 1)

    def test_delete_worked_hours(self):
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours = wh_accessor.get_by_label("Open hours")
        accessor = WorkedHoursAccessor(self.session)
        accessor.insert_worked_hours(week_hours.uid, "Enterprise's open hours", "The normal open hours")
        worked_hours = accessor.get_by_label("Enterprise's open hours")
        accessor.delete_worked_hours(worked_hours.uid)
        with self.assertRaises(RecordNotFoundError) as context:
            accessor.delete_worked_hours(123)
        LOG.debug(context.exception)

    def test_get_worked_hours(self):
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer open hours")
        accessor = WorkedHoursAccessor(self.session)
        accessor.insert_worked_hours(week_hours1.uid, "Enterprise's open hours", "The normal open hours")
        accessor.insert_worked_hours(week_hours2.uid, "Summer open hours", "Normal open hours in summer")
        (r1, r2) = accessor.get_worked_hours_list()
        worked_hours = accessor.get_worked_hours(r1.uid)
        self.assertEqual(worked_hours, r1)
        worked_hours = accessor.get_worked_hours(r2.uid)
        self.assertEqual(worked_hours, r2)
        with self.assertRaises(RecordNotFoundError):
            accessor.get_worked_hours(123)

    def test_insert_worked_hours(self):
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer open hours")
        accessor = WorkedHoursAccessor(self.session)
        accessor.insert_worked_hours(week_hours1.uid, "label1", "Description1")
        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_worked_hours(week_hours2.uid, "label1", "Description2")
        LOG.debug(context.exception)

    def test_get_worked_hours_list(self):
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer open hours")

        accessor = WorkedHoursAccessor(self.session)
        self.assertFalse(accessor.get_worked_hours_list())

        accessor.insert_worked_hours(week_hours1.uid, "label1", "Description1")
        accessor.insert_worked_hours(week_hours2.uid, "label2", "Description2")
        curr = accessor.get_worked_hours_list()
        self.assertEqual(curr[0].label, "label1")
        self.assertEqual(curr[1].label, "label2")

        curr = accessor.get_worked_hours_list(WorkedHours.label == "label2")
        self.assertEqual(len(curr), 1)
        self.assertEqual(curr[0].label, "label2")

        accessor.insert_worked_hours(week_hours2.uid, "label3", "Description3")
        curr = accessor.get_worked_hours_list(order_by_cond=desc(WorkedHours.label))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "label3")
        self.assertEqual(curr[1].label, "label2")
        self.assertEqual(curr[2].label, "label1")

        curr = accessor.get_worked_hours_list(order_by_cond=desc(WorkedHours.position))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "label3")
        self.assertEqual(curr[1].label, "label2")
        self.assertEqual(curr[2].label, "label1")

    def test_update_worked_hours(self):
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours1 = wh_accessor.get_by_label("Open hours")
        week_hours2 = wh_accessor.get_by_label("Summer open hours")

        accessor = WorkedHoursAccessor(self.session)
        accessor.insert_worked_hours(week_hours1.uid, "label1", "Description1")
        worked_hours = accessor.get_by_label("label1")

        accessor.update_worked_hours(worked_hours.uid, position=12, label="new label", description="new description")
        curr = accessor.get_worked_hours(worked_hours.uid)
        self.assertEqual(curr.position, 12)
        self.assertEqual(curr.label, "new label")
        self.assertEqual(curr.description, "new description")

        accessor.insert_worked_hours(week_hours2.uid, "label2", "Description2")

        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_worked_hours(worked_hours.uid, label="label2")
        LOG.debug(context.exception)
