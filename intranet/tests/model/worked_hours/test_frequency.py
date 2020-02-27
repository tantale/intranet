# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import unittest

from intranet.model.planning.frequency import Frequency


class TestFrequency(unittest.TestCase):
    def test_match_week(self):
        f = Frequency(u"aperiodic", u"all the year", 0, 1)
        self.assertTrue(all(f.match_week(w) for w in range(1, 54)))

        f = Frequency(u"even", u"even weeks", 0, 2)
        self.assertTrue(all(f.match_week(w) for w in range(2, 54, 2)))
        self.assertFalse(any(f.match_week(w) for w in range(1, 54, 2)))

        f = Frequency(u"odd", u"odd weeks", 1, 2)
        self.assertTrue(all(f.match_week(w) for w in range(1, 54, 2)))
        self.assertFalse(any(f.match_week(w) for w in range(2, 54, 2)))

    def test_frequency_repr(self):
        f = Frequency(u"aperiodic", u"all the year", 0, 1)
        self.assertEqual(repr(f), "Frequency(u'aperiodic', u'all the year', 0, 1)")
