# -*- coding: utf-8 -*-
"""
Users selection
===============

Date: 2015-06-06

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals
import logging

from tg import session
from tg.controllers.restcontroller import RestController
from tg.decorators import expose

from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.controllers.session_obj.casting import as_int, as_bool

LOG = logging.getLogger(__name__)


class UsersSelectionController(RestController):
    """
    Memorize the selected calendar.
    .. versionadded:: 1.4.0
        Prepare next release for "planning".
    """
    def __init__(self, module):
        self.session_var = module + ".users_selection"

    @property
    def selections(self):
        return session.get(self.session_var)

    @selections.setter
    def selections(self, selections):
        session[self.session_var] = selections
        session.save()

    @expose('json')
    def get_all(self):
        selections = self.selections
        if selections is None:
            accessor = EmployeeAccessor()
            employee_list = accessor.get_employee_list()
            # Select all employees except employees outside staff
            selections = {employee.uid for employee in employee_list if not employee.exit_date}
            self.selections = selections
        # It is more secure to return a dict than a list
        return dict(selections=selections)

    @expose()
    def put(self, uid, checked):
        uid = as_int(uid)
        checked = as_bool(checked)
        if checked:
            self.selections = self.selections | {uid}
        else:
            self.selections = self.selections - {uid}
