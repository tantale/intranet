# -*- coding: utf-8 -*-
"""
Mathematical statistics functions
=================================

Minimal implementation of statistics, see: `<https://docs.python.org/3/library/statistics.html>`_.
"""
from __future__ import division

import math


class StatisticsError(ValueError):
    pass


def mean(data):
    """
    Return the sample arithmetic mean of data.

    >>> mean([1, 2, 3, 4, 4])
    2.8

    >>> mean(xrange(10))
    4.5

    :param data:
    :return:
    """
    try:
        return sum(data) / len(data)
    except ZeroDivisionError:
        raise StatisticsError('mean requires at least one data point')


def pvariance(data, xbar=None):
    """
    Return the population variance of ``data``.

    >>> data = [0.0, 0.25, 0.25, 1.25, 1.5, 1.75, 2.75, 3.25]
    >>> pvariance(data)
    1.25

    :param data:
    :param xbar:
    :return:
    """
    xbar = mean(data) if xbar is None else xbar
    return sum((x - xbar) ** 2 for x in data) / len(data)


def phi(x):
    """
    Approximation de la fonction de répartition

    >>> 2 * phi(2) - 1
    0.9544997361036414

    >>> [phi(x) for x in xrange(5)]
    [0.5, 0.841344746068543, 0.9772498680518207, 0.9986501019683696, 0.999968328758167]

    :param x:
    :return:
    """
    s = x
    t = 0
    b = x
    q = x ** 2
    i = 1
    while s != t:
        t = s
        i += 2
        b = b * q / i
        s = t + b
    # math.log(math.sqrt(2 * math.pi)) = 0.91893853320467274178
    return 0.5 + s * math.exp(-0.5 * q - 0.91893853320467274178)


def gauss_filter(items, r=1.6449, key=None):
    """
    Filter items according to the gauss quantile function.

    * p(r) = 2 * phi(r) - 1 = erf(r / sqrt(2))
    * phi(r) = (p(r) + 1) / 2
    * r = phi^-1((p(r) + 1) / 2)
    * r = phi_inv((p(r) + 1) / 2)

    +---+------+--------+--------+--------+--------+--------+--------+--------+--------+
    | r | 0,0  | 0,5    | 1,0    | 1,5    | 1.6449 | 2,0    | 2,5    | 3,0    | 3,5    |
    +===+======+========+========+========+========+========+========+========+========+
    | p | 0,00 | 0,3829 | 0,6827 | 0,8664 | 0.9000 | 0,9545 | 0,9876 | 0,9973 | 0,9995 |
    +---+------+--------+--------+--------+--------+--------+--------+--------+--------+

    >>> math.erf(2 / math.sqrt(2))
    0.9544997361036415

    >>> gauss_filter([3, 4, 5, 4, 3, 12])
    [3, 4, 5, 4, 3]

    >>> import collections
    >>> Item = collections.namedtuple("Item", ["uid", "duration"])
    >>> items = [Item(1, 4.5), Item(3, 4), Item(4, 10), Item(5, 7.25), Item(6, 8.5),
    ...          Item(8, 6.5), Item(9, 12), Item(10, 10.75), Item(12, 9.25),
    ...          Item(13, 9), Item(14, 5.5), Item(15, 6), Item(17, 5.5),
    ...          Item(18, 8.75), Item(19, 9.75)]
    >>> filtered = gauss_filter(items, key=lambda i: i[1], r=1.5)
    >>> missing = [x for x in items if x not in filtered]
    >>> missing
    [Item(uid=3, duration=4), Item(uid=9, duration=12)]

    :param items:
    :param key:
    :param r:
    :return:
    """
    if key is None:
        key = lambda x1: x1
    data = [key(x) for x in items]
    mu = mean(data)
    sigma = math.sqrt(pvariance(data, mu))
    inf = mu - r * sigma
    sup = mu + r * sigma
    return filter(lambda x2: inf <= key(x2) <= sup, items)
