"""
:module: intranet.controllers.pointage.employee
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from tg import expose
from intranet.lib.base import BaseController


class EmployeeController(BaseController):
    """
    Create / Modify / Remove Employees
    """

    @expose('intranet.templates.pointage.employee')
    def index(self):
        return dict(page='index')
