# -*- coding: utf-8 -*-
"""
layout
======

Date: 2015-05-30

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals
import logging

from tg import session
from tg.controllers.restcontroller import RestController
from tg.decorators import expose

from intranet.controllers.session_obj.casting import as_int, as_dict

LOG = logging.getLogger(__name__)


class LayoutController(RestController):
    """
    Memorize the position of the left frame.

    .. versionadded:: 1.4.0
    """
    CONFIG = dict(
        north__size="auto",
        north__closable=False,
        north__resizable=False,
        north__slidable=False,
        north__spacing_open=0,
        north__spacing_closed=0,
        west__minSize=200,
        west__maxSize=600)

    DEFAULT_PROPERTIES = dict(west__size=260)

    CAST_MAPPING = dict(west__size=as_int)

    def __init__(self, module):
        self.session_var = module + ".layout"

    @property
    def properties(self):
        return session.get(self.session_var, dict(self.DEFAULT_PROPERTIES))

    @properties.setter
    def properties(self, properties):
        # use: http://127.0.0.1:8080/environ.html to display the cookie session
        session[self.session_var] = properties
        session.save()

    @expose('json')
    def get_all(self):
        return dict(self.CONFIG, **self.properties)

    @expose()
    def put(self, **kwargs):
        # with a getter/setter we can't update directly
        casted_kwargs = as_dict(self.CAST_MAPPING, kwargs)
        self.properties = dict(self.properties, **casted_kwargs)
