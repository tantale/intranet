# -*- coding: utf-8 -*-
"""
Current user
============

Date: 2015-06-06

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals
import logging

from tg import session
from tg.controllers.restcontroller import RestController
from tg.decorators import expose

from intranet.controllers.session_obj.casting import as_int, as_dict

LOG = logging.getLogger(__name__)


class CurrUserController(RestController):
    """
    Memorize the current user.

    .. versionadded:: 1.4.0
    """
    CONFIG = dict()

    DEFAULT_PROPERTIES = dict(uid=0)

    CAST_MAPPING = dict(uid=as_int)

    def __init__(self, module):
        self.session_var = module + ".curr_user"

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
