# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def as_bool(x):
    return unicode(x).lower() in ("true", "yes", "on", "1")


def as_int(x):
    return int(x)


def as_unicode(x):
    return x


def as_dict(cast_mapping, kwargs):
    return {k: cast_mapping[k](v) for k, v in kwargs.iteritems()}
