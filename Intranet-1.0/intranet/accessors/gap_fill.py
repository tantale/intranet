# -*- coding: utf-8 -*-
"""
Gap fill
========

:Date: 2016-02-10
:Author: Laurent LAPORTE

.. versionadded:: 2.2.0
   Utility classe used to find gaps in date/time intervals.
"""

import itertools


# noinspection PyMethodOverriding
class GapFill(dict):
    u"""
    A GapFill is a collection of colored slots.
    A slots in a ordered list of items; a color is a label.

    >>> colored_slots = [([1, 2, 3], 'RED'), ([4, 5, 6, 7], 'BLUE'), ([8, 9], 'RED')]
    >>> gp = GapFill(colored_slots)
    >>> gp[6]
    'BLUE'
    >>> gp[4:6] = 'RED'
    >>> gp.colored_slots
    [([1, 2, 3, 4, 5], 'RED'), ([6, 7], 'BLUE'), ([8, 9], 'RED')]
    >>> gp[8:] = 'BLUE'
    >>> gp.colored_slots
    [([1, 2, 3, 4, 5], 'RED'), ([6, 7, 8, 9], 'BLUE')]
    >>> gp[:8:2]
    ['RED', 'RED', 'RED', 'BLUE']
    >>> gp[:] = 'GREEN'
    >>> gp.colored_slots
    [([1, 2, 3, 4, 5, 6, 7, 8, 9], 'GREEN')]
    >>> gp[10] = 'RED'
    >>> gp[11] = 'RED'
    >>> gp.colored_slots
    [([1, 2, 3, 4, 5, 6, 7, 8, 9], 'GREEN'), ([10, 11], 'RED')]
    """

    def __init__(self, *colored_slots):
        """
        Construct a Gap fill.

        :type colored_slots: list[tuple(list, str|unicode)]
        :param colored_slots: collection of colored slots: [item1, item2, item3, ...] -> color.
        """
        super(GapFill, self).__init__()
        self.colored_slots = colored_slots

    def keys(self):
        return sorted(super(GapFill, self).keys())

    def items(self):
        return sorted(super(GapFill, self).items())

    def values(self):
        return [self[k] for k in self.keys()]

    def iterkeys(self):
        return (k for k in self.keys())

    def iteritems(self):
        return (i for i in self.items())

    def itervalues(self):
        return (v for v in self.values())

    def __iter__(self):
        keys = sorted(super(GapFill, self).keys())
        return (k for k in keys)

    def __reversed__(self):
        reversed_keys = sorted(super(GapFill, self).keys(), reverse=True)
        return (k for k in reversed_keys)

    @property
    def colored_slots(self):
        colored_slots = []
        for color, slot in itertools.groupby(self.items(), key=lambda i: i[1]):
            colored_slots.append(([item[0] for item in slot], color))
        return colored_slots

    @colored_slots.setter
    def colored_slots(self, colored_slots):
        for colored_slot in colored_slots:
            for slot, color in colored_slot:
                for item in slot:
                    super(GapFill, self).__setitem__(item, color)

    @colored_slots.deleter
    def colored_slots(self):
        self.clear()

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.start is None:
                if key.stop is None:
                    items = self.keys()
                else:
                    items = [item for item in self.iterkeys() if item < key.stop]
            else:
                if key.stop is None:
                    items = [item for item in self.iterkeys() if key.start <= item]
                else:
                    items = [item for item in self.iterkeys() if key.start <= item < key.stop]
            if key.step:
                items = items[::key.step]
            return [super(GapFill, self).__getitem__(item) for item in items]
        else:
            return super(GapFill, self).__getitem__(key)

    def __setitem__(self, key, color, **kwargs):
        if isinstance(key, slice):
            if key.start is None:
                if key.stop is None:
                    items = self.keys()
                else:
                    items = [item for item in self.iterkeys() if item < key.stop]
            else:
                if key.stop is None:
                    items = [item for item in self.iterkeys() if key.start <= item]
                else:
                    items = [item for item in self.iterkeys() if key.start <= item < key.stop]
            if key.step:
                items = items[::key.step]
            for item in items:
                super(GapFill, self).__setitem__(item, color)
        else:
            super(GapFill, self).__setitem__(key, color)
