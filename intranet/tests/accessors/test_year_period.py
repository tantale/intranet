# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import datetime
import logging
import random
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors import RecordNotFoundError
from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.frequency import FrequencyAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.planning.year_period import YearPeriodAccessor
from intranet.model import DeclarativeBase
from intranet.model.planning.week_hours import WeekHours

LOG = logging.getLogger(__name__)


class TestYearPeriodAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestYearPeriodAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestYearPeriodAccessor, self).setUp()

        # -- Connecting to the database
        engine = create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

        wh_accessor = WeekHoursAccessor(self.session)
        wh_accessor.insert_week_hours("Open hours", "All year open hours")
        wh_accessor.insert_week_hours("Holiday open hours", "Open hours in holiday")
        week_hours1, week_hours2 = wh_accessor.get_week_hours_list(order_by_cond=WeekHours.position)

        calendar_accessor = CalendarAccessor(self.session)
        calendar_accessor.insert_calendar(week_hours1.uid,
                                          "General calendar", "Same as enterprise's open hours")

        fqc_accessor = FrequencyAccessor(self.session)
        fqc_accessor.insert_frequency("aperiodic", "all the year", 0, 1)
        fqc_accessor.insert_frequency("even", "even weeks", 0, 2)
        fqc_accessor.insert_frequency("odd", "odd weeks", 1, 2)

    def test_setup(self):
        accessor = YearPeriodAccessor(self.session)

        # -- first setup
        accessor.setup()

        # -- next setup...
        accessor.setup()  # must not raise

    def test_get_year_period(self):
        accessor = YearPeriodAccessor(self.session)

        calendar_accessor = CalendarAccessor(self.session)
        calendar = calendar_accessor.get_by_label("General calendar")
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours = wh_accessor.get_by_label("Holiday open hours")
        fqc_accessor = FrequencyAccessor(self.session)
        frequency = fqc_accessor.get_by_label("aperiodic")

        start_date = datetime.date(2015, 1, 1)
        end_date = datetime.date(2015, 12, 31)
        accessor.insert_year_period(calendar.uid, week_hours.uid, frequency.uid, start_date, end_date)

        year_period = random.choice(accessor.get_year_period_list())
        current = accessor.get_year_period(year_period.uid)
        self.assertEqual(current, year_period)

        with self.assertRaises(RecordNotFoundError):
            accessor.get_year_period(1234)

    def test_get_year_period_list(self):
        accessor = YearPeriodAccessor(self.session)
        self.assertFalse(accessor.get_year_period_list())

        calendar_accessor = CalendarAccessor(self.session)
        calendar = calendar_accessor.get_by_label("General calendar")
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours = wh_accessor.get_by_label("Holiday open hours")
        fqc_accessor = FrequencyAccessor(self.session)
        frequency = fqc_accessor.get_by_label("aperiodic")

        start_date = datetime.date(2015, 1, 1)
        end_date = datetime.date(2015, 12, 31)
        accessor.insert_year_period(calendar.uid, week_hours.uid, frequency.uid, start_date, end_date)

        self.assertEqual(len(accessor.get_year_period_list()), 1)

    def test_insert_year_period(self):
        accessor = YearPeriodAccessor(self.session)

        calendar_accessor = CalendarAccessor(self.session)
        calendar = calendar_accessor.get_by_label("General calendar")
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours = wh_accessor.get_by_label("Holiday open hours")
        fqc_accessor = FrequencyAccessor(self.session)
        frequency = fqc_accessor.get_by_label("aperiodic")

        start_date = datetime.date(2015, 1, 1)
        end_date = datetime.date(2015, 12, 31)
        accessor.insert_year_period(calendar.uid, week_hours.uid, frequency.uid, start_date, end_date)

        calendar = calendar_accessor.get_calendar(calendar.uid)
        week_hours = wh_accessor.get_week_hours(week_hours.uid)
        frequency = fqc_accessor.get_frequency(frequency.uid)
        self.assertEqual(len(calendar.year_period_list), 1)
        self.assertEqual(len(week_hours.year_period_list), 1)
        self.assertEqual(len(frequency.year_period_list), 1)

        # Can contain duplicates
        accessor.insert_year_period(calendar.uid, week_hours.uid, frequency.uid, start_date, end_date)
        self.assertEqual(len(accessor.get_year_period_list()), 2)

        calendar = calendar_accessor.get_calendar(calendar.uid)
        week_hours = wh_accessor.get_week_hours(week_hours.uid)
        frequency = fqc_accessor.get_frequency(frequency.uid)
        self.assertEqual(len(calendar.year_period_list), 2)
        self.assertEqual(len(week_hours.year_period_list), 2)
        self.assertEqual(len(frequency.year_period_list), 2)

    def test_update_year_period(self):
        accessor = YearPeriodAccessor(self.session)
        self.assertFalse(accessor.get_year_period_list())

        calendar_accessor = CalendarAccessor(self.session)
        calendar = calendar_accessor.get_by_label("General calendar")
        wh_accessor = WeekHoursAccessor(self.session)
        week_hours = wh_accessor.get_by_label("Holiday open hours")
        fqc_accessor = FrequencyAccessor(self.session)
        frequency = fqc_accessor.get_by_label("aperiodic")

        start_date = datetime.date(2015, 1, 1)
        end_date = datetime.date(2015, 12, 31)
        accessor.insert_year_period(calendar.uid, week_hours.uid, frequency.uid, start_date, end_date)

        week_hours = wh_accessor.get_by_label("Holiday open hours")
        year_period = week_hours.year_period_list[0]
        frequency = fqc_accessor.get_by_label("even")
        accessor.update_year_period(year_period.uid, frequency=frequency)

        week_hours = wh_accessor.get_by_label("Holiday open hours")
        year_period = week_hours.year_period_list[0]
        frequency = fqc_accessor.get_by_label("even")
        self.assertEqual(year_period.frequency, frequency)

    def test_select_week_hours(self):
        yp_accessor = YearPeriodAccessor(self.session)
        calendar_accessor = CalendarAccessor(self.session)
        fqc_accessor = FrequencyAccessor(self.session)

        wh_accessor = WeekHoursAccessor(self.session)
        wh_accessor.insert_week_hours("default_week_hours", u"for default")
        wh_accessor.insert_week_hours("aperiodic_week_hours", u"for aperiodic")
        wh_accessor.insert_week_hours("even_week_hours", u"for even")
        wh_accessor.insert_week_hours("odd_week_hours", u"for odd")

        calendar_week_hours = wh_accessor.get_by_label("default_week_hours")
        calendar_accessor.insert_calendar(calendar_week_hours.uid, "select_week_hours", u"calendar description")

        mappings = [(datetime.date(2015, 2, 1), datetime.date(2015, 2, 28), "aperiodic", "aperiodic_week_hours"),
                    (datetime.date(2015, 4, 1), datetime.date(2015, 4, 30), "even", "even_week_hours"),
                    (datetime.date(2015, 4, 1), datetime.date(2015, 4, 30), "odd", "odd_week_hours")]

        calendar = calendar_accessor.get_by_label("select_week_hours")
        for mapping in mappings:
            start_date = mapping[0]
            end_date = mapping[1]
            frequency = fqc_accessor.get_by_label(mapping[2])
            week_hours = wh_accessor.get_by_label(mapping[3])
            yp_accessor.insert_year_period(calendar.uid, week_hours.uid, frequency.uid, start_date, end_date)

        calendar = calendar_accessor.get_by_label("select_week_hours")
        date = datetime.date(2015, 1, 1)
        week_hours = calendar.select_week_hours(date)
        self.assertEqual(week_hours.label, u"default_week_hours")

        date = datetime.date(2015, 2, 5)
        week_hours = calendar.select_week_hours(date)
        self.assertEqual(week_hours.label, u"aperiodic_week_hours")
        date = datetime.date(2015, 2, 12)
        week_hours = calendar.select_week_hours(date)
        self.assertEqual(week_hours.label, u"aperiodic_week_hours")

        date = datetime.date(2015, 4, 3)
        self.assertEqual(date.isocalendar()[1] % 2, 0)  # even
        week_hours = calendar.select_week_hours(date)
        self.assertEqual(week_hours.label, u"even_week_hours")
        date = datetime.date(2015, 4, 10)
        self.assertEqual(date.isocalendar()[1] % 2, 1)  # odd
        week_hours = calendar.select_week_hours(date)
        self.assertEqual(week_hours.label, u"odd_week_hours")
