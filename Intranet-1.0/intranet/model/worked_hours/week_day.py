# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime


class WeekDay(object):
    """
    WeekDay management.
    """
    def __init__(self, weekday, label):
        """
        The day of the week, from monday to sunday.

        Examples:

        .. code-block::

            WeekDay(0, u"Monday")
            WeekDay(1, u"Tuesday")
            WeekDay(2, u"Wednesday")
            WeekDay(3, u"Thursday")
            WeekDay(4, u"Friday")
            WeekDay(5, u"Saturday")
            WeekDay(6, u"Sunday")

        :type weekday: int
        :param weekday: Day in the week: 0 <= weekday <= 6
        :type label: unicode
        :param label: Display name of the day => used in selection.
        """
        self.uid = weekday + 1  # > 0
        self.weekday = weekday
        self.label = label

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.weekday!r}, "
                    "{self.label!r})")
        return repr_fmt.format(self=self)

    def __hash__(self):
        return hash(self.weekday)

    def __eq__(self, other):
        return self.weekday == other.weekday

    def __ne__(self, other):
        return self.weekday != other.weekday

    def __lt__(self, other):
        return self.weekday < other.weekday

    def __le__(self, other):
        return self.weekday <= other.weekday

    def __gt__(self, other):
        return self.weekday > other.weekday

    def __ge__(self, other):
        return self.weekday >= other.weekday
