# -*- coding: utf-8 -*-
"""
Calendar selection
==================

Date: 2015-09-21

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals
import logging

from tg import session
from tg.controllers.restcontroller import RestController
from tg.decorators import expose

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.controllers.session_obj.casting import as_int, as_bool

LOG = logging.getLogger(__name__)


# noinspection PyAbstractClass
class CalendarSelectionController(RestController):
    """
    Memorize the selected calendar.
    """
    def __init__(self, module):
        self.session_var = module + ".calendar_selection"

    @property
    def selections(self):
        if self.session_var not in session:
            # Select all calendars
            accessor = CalendarAccessor()
            calendar_list = accessor.get_calendar_list()
            session[self.session_var] = {calendar.uid for calendar in calendar_list}
            session.save()
            LOG.debug("init session[{key}] = {val!r}".format(key=self.session_var, val=session[self.session_var]))
        LOG.debug("get session[{key}] = {val!r}".format(key=self.session_var, val=session[self.session_var]))
        return session.get(self.session_var)

    @selections.setter
    def selections(self, selections):
        session[self.session_var] = selections
        session.save()
        LOG.debug("set session[{key}] = {val!r}".format(key=self.session_var, val=session[self.session_var]))

    @expose('json')
    def get_all(self):
        # It is more secure to return a dict than a list
        return dict(selections=self.selections)

    @expose()
    def put(self, uid, checked):
        uid = as_int(uid)
        checked = as_bool(checked)
        if checked:
            self.selections = self.selections | {uid}
        else:
            self.selections = self.selections - {uid}
