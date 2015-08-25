# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import random
import unittest
import logging
import datetime

from sqlalchemy import create_engine

from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors import RecordNotFoundError
from intranet.accessors.worked_hours.day_period import DayPeriodAccessor
from intranet.accessors.worked_hours.hours_interval import HoursIntervalAccessor
from intranet.accessors.worked_hours.week_day import WeekDayAccessor
from intranet.accessors.worked_hours.week_hours import WeekHoursAccessor
from intranet.model import DeclarativeBase
from intranet.model.worked_hours.week_hours import WeekHours

LOG = logging.getLogger(__name__)


class TestHoursIntervalAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestHoursIntervalAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestHoursIntervalAccessor, self).setUp()

        # -- Connecting to the database
        engine = create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

        wd_accessor = WeekDayAccessor(self.session)
        wd_accessor.insert_week_day(1, "Monday")
        wd_accessor.insert_week_day(2, "Tuesday")
        wd_accessor.insert_week_day(3, "Wednesday")
        wd_accessor.insert_week_day(4, "Thursday")
        wd_accessor.insert_week_day(5, "Friday")
        wd_accessor.insert_week_day(6, "Saturday")
        wd_accessor.insert_week_day(7, "Sunday")

        wh_accessor = WeekHoursAccessor(self.session)
        wh_accessor.insert_week_hours(1, "Open hours", "All year open hours")
        wh_accessor.insert_week_hours(2, "Summer open hours", "Open hours in summer")

        week_hours1, week_hours2 = wh_accessor.get_week_hours_list(order_by_cond=WeekHours.position)
        dp_accessor = DayPeriodAccessor(self.session)
        dp_accessor.insert_day_period(week_hours1, "Night", "from 10pm to 6am")
        dp_accessor.insert_day_period(week_hours1, "Morning", "from 6am to 2pm")
        dp_accessor.insert_day_period(week_hours1, "Afternoon" "from 2pm to 10pm")
        dp_accessor.insert_day_period(week_hours2, "Morning", "from 8am to 12am")
        dp_accessor.insert_day_period(week_hours2, "Afternoon" "from 2pm to 6pm")

    def test_setup(self):
        accessor = HoursIntervalAccessor(self.session)

        # -- first setup
        accessor.setup()
        week_hours = accessor.get_week_hours_list()[0]
        table = accessor.get_hours_interval_table(week_hours.uid)
        display = lambda hi: unicode(hi) if hi else "--:-- / --:--"
        for row in table:
            LOG.debug("| " + " | ".join(map(display, row)) + " |")

        # -- next setup...
        accessor.setup()  # must not raise

    def test_get_hours_interval(self):
        accessor = HoursIntervalAccessor(self.session)
        accessor.setup()  # populate the DB
        hours_interval = random.choice(accessor.get_hours_interval_list())
        week_day_uid = hours_interval.week_day_uid
        day_period_uid = hours_interval.day_period_uid

        current = accessor.get_hours_interval(week_day_uid, day_period_uid)
        self.assertEqual(current, hours_interval)

        with self.assertRaises(RecordNotFoundError):
            accessor.get_hours_interval(456, 788)

    def test_get_hours_interval_list(self):
        accessor = HoursIntervalAccessor(self.session)
        self.assertFalse(accessor.get_hours_interval_list())

        week_hours = random.choice(accessor.get_week_hours_list())
        day_period = random.choice(week_hours.day_period_list)
        week_day = random.choice(accessor.get_week_day_list())

        start_hour = datetime.time(8, 0)
        end_hour = datetime.time(12, 30)
        accessor.insert_hours_interval(week_day.uid, day_period.uid, start_hour, end_hour)

        current_list = accessor.get_hours_interval_list()
        self.assertEqual(len(current_list), 1)

    def test_insert_hours_interval(self):
        accessor = HoursIntervalAccessor(self.session)

        week_hours = random.choice(accessor.get_week_hours_list())
        day_period = random.choice(week_hours.day_period_list)
        week_day = random.choice(accessor.get_week_day_list())

        week_day_uid = week_day.uid
        day_period_uid = day_period.uid

        start_hour = datetime.time(8, 0)
        end_hour = datetime.time(12, 30)
        accessor.insert_hours_interval(week_day_uid, day_period_uid, start_hour, end_hour)

        current = accessor.get_hours_interval(week_day_uid, day_period_uid)
        self.assertEqual(current.start_hour, start_hour)
        self.assertEqual(current.end_hour, end_hour)

        with self.assertRaises(IntegrityError):
            accessor.insert_hours_interval(week_day_uid, day_period_uid, start_hour, end_hour)

    def test_update_hours_interval(self):
        accessor = HoursIntervalAccessor(self.session)

        week_hours = random.choice(accessor.get_week_hours_list())
        day_period = random.choice(week_hours.day_period_list)
        week_day = random.choice(accessor.get_week_day_list())

        week_day_uid = week_day.uid
        day_period_uid = day_period.uid

        start_hour = datetime.time(8, 0)
        end_hour = datetime.time(12, 30)
        accessor.insert_hours_interval(week_day_uid, day_period_uid, start_hour, end_hour)

        start_hour = datetime.time(14, 0)
        end_hour = datetime.time(17, 45)
        accessor.update_hours_interval(week_day_uid, day_period_uid,
                                       start_hour=start_hour, end_hour=end_hour)

        current = accessor.get_hours_interval(week_day_uid, day_period_uid)
        self.assertEqual(current.start_hour, start_hour)
        self.assertEqual(current.end_hour, end_hour)

    def test_delete_hours_interval(self):
        accessor = HoursIntervalAccessor(self.session)

        week_hours = random.choice(accessor.get_week_hours_list())
        day_period = random.choice(week_hours.day_period_list)
        week_day = random.choice(accessor.get_week_day_list())

        week_day_uid = week_day.uid
        day_period_uid = day_period.uid

        start_hour = datetime.time(8, 0)
        end_hour = datetime.time(12, 30)
        accessor.insert_hours_interval(week_day_uid, day_period_uid, start_hour, end_hour)

        accessor.delete_hours_interval(week_day_uid, day_period_uid)
