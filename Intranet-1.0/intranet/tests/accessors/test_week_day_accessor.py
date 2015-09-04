# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import logging
import datetime

from sqlalchemy import create_engine
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import desc
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors import RecordNotFoundError
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.model import DeclarativeBase
from intranet.model.planning.week_day import WeekDay

LOG = logging.getLogger(__name__)


class TestWeekDayAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestWeekDayAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestWeekDayAccessor, self).setUp()

        # -- Connecting to the database
        engine = create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

    def test_setup(self):
        accessor = WeekDayAccessor(self.session)
        accessor.setup()
        week_days = {wd.iso_weekday: wd for wd in accessor.get_week_day_list()}
        for days in xrange(7):
            date = datetime.date.today() + datetime.timedelta(days=days)
            iso_weekday = date.isoweekday()
            LOG.debug("{iso_weekday}: {label}".format(iso_weekday=iso_weekday, label=week_days[iso_weekday].label))

        accessor.setup()  # on second setup, do nothing

    def test_delete_week_day(self):
        accessor = WeekDayAccessor(self.session)
        accessor.insert_week_day(1, "Monday", "On Monday")
        accessor.delete_week_day(1)
        with self.assertRaises(RecordNotFoundError) as context:
            accessor.delete_week_day(123)
        LOG.debug(context.exception)

    def test_get_week_day(self):
        accessor = WeekDayAccessor(self.session)
        accessor.insert_week_day(1, "Monday", "On Monday")
        accessor.insert_week_day(2, "Tuesday", "On Tuesday")
        (r1, r2) = accessor.get_week_day_list()
        week_day = accessor.get_week_day(r1.uid)
        self.assertEqual(week_day, r1)
        week_day = accessor.get_week_day(r2.uid)
        self.assertEqual(week_day, r2)
        with self.assertRaises(RecordNotFoundError):
            accessor.get_week_day(123)

    def test_insert_week_day(self):
        accessor = WeekDayAccessor(self.session)
        accessor.insert_week_day(1, "Monday", "On Monday")

        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_week_day(2, "Monday", "On Tuesday")
        LOG.debug(context.exception)

        # iso_weekday is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_week_day(1, "Tuesday", "On Tuesday")
        LOG.debug(context.exception)

        # 0 <= iso_weekday
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_week_day(-1, "Tuesday", "On Tuesday")
        LOG.debug(context.exception)

        # iso_weekday <= 6
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_week_day(8, "Tuesday", "On Tuesday")
        LOG.debug(context.exception)

    def test_get_week_day_list(self):
        accessor = WeekDayAccessor(self.session)
        self.assertFalse(accessor.get_week_day_list())

        accessor.insert_week_day(1, "Monday", "On Monday")
        accessor.insert_week_day(2, "Tuesday", "On Tuesday")
        curr = accessor.get_week_day_list()
        self.assertEqual(curr[0].label, "Monday")
        self.assertEqual(curr[1].label, "Tuesday")

        curr = accessor.get_week_day_list(WeekDay.label == "Tuesday")
        self.assertEqual(len(curr), 1)
        self.assertEqual(curr[0].label, "Tuesday")

        accessor.insert_week_day(3, "label3", "Description3")
        curr = accessor.get_week_day_list(order_by_cond=desc(WeekDay.label))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "label3")
        self.assertEqual(curr[1].label, "Tuesday")
        self.assertEqual(curr[2].label, "Monday")

        curr = accessor.get_week_day_list(order_by_cond=desc(WeekDay.iso_weekday))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "label3")
        self.assertEqual(curr[1].label, "Tuesday")
        self.assertEqual(curr[2].label, "Monday")

    def test_update_week_day(self):
        accessor = WeekDayAccessor(self.session)
        accessor.insert_week_day(1, "Monday", "On Monday")
        uid = 1

        accessor.update_week_day(uid, iso_weekday=5, label="new label", description="new description")
        curr = accessor.get_week_day(uid)
        self.assertEqual(curr.iso_weekday, 5)
        self.assertEqual(curr.label, "new label")
        self.assertEqual(curr.description, "new description")

        accessor.insert_week_day(2, "Tuesday", "On Tuesday")

        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_week_day(uid, label="Tuesday")
        LOG.debug(context.exception)

        # iso_weekday is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_week_day(uid, iso_weekday=2)
        LOG.debug(context.exception)

        # 0 <= iso_weekday
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_week_day(uid, iso_weekday=-1)
        LOG.debug(context.exception)

        # iso_weekday <= 6
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_week_day(uid, iso_weekday=8)
        LOG.debug(context.exception)
