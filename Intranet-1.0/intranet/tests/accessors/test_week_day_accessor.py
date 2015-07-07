# -*- coding: utf-8 -*-
import logging
import unittest
from intranet.accessors import RecordNotFoundError
from intranet.accessors.worked_hours.week_day import WeekDayAccessor

LOG = logging.getLogger(__name__)


class TestWeekDayAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestWeekDayAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def test_get_week_day(self):
        accessor = WeekDayAccessor(session=None)
        for uid in xrange(1, 8):
            week_day = accessor.get_week_day(uid)
            LOG.debug(week_day)
            self.assertEqual(week_day.weekday, uid - 1)
        with self.assertRaises(RecordNotFoundError) as context:
            accessor.get_week_day(25)
        LOG.debug(context.exception)

    def test_get_week_day_list(self):
        accessor = WeekDayAccessor(session=None)
        week_day_list = accessor.get_week_day_list()
        self.assertEqual([w.weekday for w in week_day_list], range(7))
