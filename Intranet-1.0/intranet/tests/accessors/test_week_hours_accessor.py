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
from intranet.model import DeclarativeBase
from intranet.model.worked_hours.week_hours import WeekHours

LOG = logging.getLogger(__name__)


class TestWeekHoursAccessor(unittest.TestCase):
    DEBUG = True

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

    def test_setup(self):
        accessor = WeekHoursAccessor(self.session)
        accessor.setup()
        accessor.setup()  # on second setup, do nothing

    def test_delete_week_hours(self):
        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours(1, "label1", "Description1")
        accessor.delete_week_hours(1)
        with self.assertRaises(RecordNotFoundError) as context:
            accessor.delete_week_hours(123)
        LOG.debug(context.exception)

    def test_get_week_hours(self):
        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours(1, "label1", "Description1")
        accessor.insert_week_hours(2, "label2", "Description2")
        (r1, r2) = accessor.get_week_hours_list()
        week_hours = accessor.get_week_hours(r1.uid)
        self.assertEqual(week_hours, r1)
        week_hours = accessor.get_week_hours(r2.uid)
        self.assertEqual(week_hours, r2)
        with self.assertRaises(RecordNotFoundError):
            accessor.get_week_hours(123)

    def test_insert_week_hours(self):
        accessor = WeekHoursAccessor(self.session)
        accessor.insert_week_hours(1, "label1", "Description1")

        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_week_hours(2, "label1", "Description2")
        LOG.debug(context.exception)

        # position is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_week_hours(1, "label2", "Description2")
        LOG.debug(context.exception)

        # position > 0
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_week_hours(0, "label2", "Description2")
        LOG.debug(context.exception)

    def test_get_week_hours_list(self):
        accessor = WeekHoursAccessor(self.session)
        self.assertFalse(accessor.get_week_hours_list())

        accessor.insert_week_hours(1, "label1", "Description1")
        accessor.insert_week_hours(2, "label2", "Description2")
        curr = accessor.get_week_hours_list()
        self.assertEqual(curr[0].label, "label1")
        self.assertEqual(curr[1].label, "label2")

        curr = accessor.get_week_hours_list(WeekHours.label == "label2")
        self.assertEqual(len(curr), 1)
        self.assertEqual(curr[0].label, "label2")

        accessor.insert_week_hours(3, "label3", "Description3")
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
        accessor.insert_week_hours(1, "label1", "Description1")
        uid = 1

        accessor.update_week_hours(uid, position=12, label="new label", description="new description")
        curr = accessor.get_week_hours(uid)
        self.assertEqual(curr.position, 12)
        self.assertEqual(curr.label, "new label")
        self.assertEqual(curr.description, "new description")

        accessor.insert_week_hours(2, "label2", "Description2")

        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_week_hours(uid, label="label2")
        LOG.debug(context.exception)

        # position is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_week_hours(uid, position=2)
        LOG.debug(context.exception)

        # position > 0
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_week_hours(uid, position=0)
        LOG.debug(context.exception)
