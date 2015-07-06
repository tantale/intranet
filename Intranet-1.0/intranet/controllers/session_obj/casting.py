# -*- coding: utf-8 -*-
from __future__ import unicode_literals

as_bool = lambda x: unicode(x).lower() in ("true", "yes", "on", "1")
as_int = lambda x: int(x)
as_unicode = lambda x: x
as_dict = lambda cast_mapping, kwargs: {k: cast_mapping[k](v) for k, v in kwargs.iteritems()}
