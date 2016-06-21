# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import unittest

from intranet.model.planning.week_day import WeekDay


class TestWeekDay(unittest.TestCase):
    @unittest.skip("Don't work with tox")
    def test_position(self):
        monday = WeekDay(1, u"Monday", u"First day of the week")
        tuesday = WeekDay(2, u"Tuesday", u"Second day of the week")
        wednesday = WeekDay(3, u"Wednesday", u"Third day of the week")
        thursday = WeekDay(4, u"Thursday", u"Fourth day of the week")
        friday = WeekDay(5, u"Friday", u"Fifth day of the week")
        saturday = WeekDay(6, u"Saturday", u"Sixth day of the week")
        sunday = WeekDay(7, u"Sunday", u"Last day of the week")
        assert monday < tuesday < wednesday < thursday < friday < saturday < sunday
        assert monday <= tuesday <= wednesday <= thursday <= friday <= saturday <= sunday <= sunday
        assert sunday > saturday > friday > thursday > wednesday > tuesday > monday
        assert sunday >= saturday >= friday >= thursday >= wednesday >= tuesday >= monday >= monday

    @unittest.skip("Don't work with tox")
    def test_invalid(self):
        with self.assertRaisesRegexp(ValueError, r"required position > 0"):
            WeekDay(0, u"Monday", u"First day of the week")

    @unittest.skip("Don't work with tox")
    def test_week_day_repr(self):
        wd = WeekDay(1, u"Monday", u"First day")
        self.assertEqual(repr(wd), "WeekDay(1, u'Monday', u'First day')")
