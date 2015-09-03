# -*- coding: utf-8 -*-

import logging
from pprint import pformat

from tg.i18n import ugettext as _
import pylons
from tg.controllers.restcontroller import RestController

from tg.flash import flash

from tg.decorators import expose, with_trailing_slash, without_trailing_slash

from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.worked_hours.worked_hours import WorkedHoursAccessor
from intranet.model.pointage.employee import Employee

LOG = logging.getLogger(__name__)


class OpenHoursController(RestController):
    def _before(self, *args, **kw):
        self.accessor = WorkedHoursAccessor()

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.hours.open_hours.index")
    def index(self, **kwargs):
        LOG.info("OpenHoursController.index, kw = " + pformat(kwargs))
        return dict(values=kwargs)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.hours.open_hours.get_all")
    def get_all(self, **kwargs):
        LOG.info("OpenHoursController.get_all, kw = " + pformat(kwargs))
        return dict(values=kwargs, worked_hours_list=self.accessor.get_worked_hours_list())

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.hours.open_hours.new")
    def new(self, **kwargs):
        LOG.info("OpenHoursController.new, kw = " + pformat(kwargs))
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(values=kwargs, form_errors=form_errors,
                    week_hours_list=self.accessor.get_week_hours_list())


class UsersController(RestController):
    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.hours.users.index")
    def index(self, **kwargs):
        LOG.info("UsersController.index, kw = " + pformat(kwargs))
        return dict(values=kwargs)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('json')
    @expose("intranet.templates.hours.users.get_all")
    def get_all(self, **kwargs):
        LOG.info("UsersController.get_all, kw = " + pformat(kwargs))
        accessor = EmployeeAccessor()
        return dict(title=_(u"Liste des employés"),
                    employee_list=accessor.get_employee_list(order_by_cond=Employee.employee_name))

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('json')
    @expose("intranet.templates.hours.users.new")
    def new(self, **kwargs):
        LOG.info("UsersController.new, kw = " + pformat(kwargs))
        accessor = EmployeeAccessor()
        return dict(title=_(u"Liste des employés"),
                    employee_list=accessor.get_employee_list(order_by_cond=Employee.employee_name))

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('json')
    def get_one(self, uid, **kwargs):
        LOG.info("UsersController.get_one, kw = " + pformat(kwargs))
        uid = int(uid)
        accessor = EmployeeAccessor()
        employee = accessor.get_employee(uid)
        return dict(title=employee.employee_name,
                    employee=employee)


class HoursController(RestController):
    open_hours = OpenHoursController()
    users = UsersController()
