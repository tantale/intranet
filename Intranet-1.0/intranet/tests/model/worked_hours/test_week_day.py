# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import unittest

from intranet.model.worked_hours.week_day import WeekDay


class TestWeekDay(unittest.TestCase):
    def test_position(self):
        monday = WeekDay(u"Monday", u"First day of the week", 1)
        tuesday = WeekDay(u"Tuesday", u"Second day of the week", 2)
        wednesday = WeekDay(u"Wednesday", u"Third day of the week", 3)
        thursday = WeekDay(u"Thursday", u"Fourth day of the week", 4)
        friday = WeekDay(u"Friday", u"Fifth day of the week", 5)
        saturday = WeekDay(u"Saturday", u"Sixth day of the week", 6)
        sunday = WeekDay(u"Sunday", u"Last day of the week", 7)
        assert monday < tuesday < wednesday < thursday < friday < saturday < sunday
        assert monday <= tuesday <= wednesday <= thursday <= friday <= saturday <= sunday <= sunday
        assert sunday > saturday > friday > thursday > wednesday > tuesday > monday
        assert sunday >= saturday >= friday >= thursday >= wednesday >= tuesday >= monday >= monday

    def test_invalid(self):
        with self.assertRaisesRegexp(ValueError, r"required position > 0"):
            WeekDay(u"Monday", u"First day of the week", 0)

    def test_week_day_repr(self):
        wd = WeekDay(u"Monday", u"First day", 1)
        self.assertEqual(repr(wd), "WeekDay(u'Monday', u'First day', 1)")
