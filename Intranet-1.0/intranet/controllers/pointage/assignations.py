# -*- coding: utf-8 -*-
import datetime
import logging
import pprint

import pylons
import sqlalchemy.exc
from formencode.validators import Number
from pylons import request
from tg import expose, validate, redirect
from tg.controllers import RestController

from intranet.accessors.pointage.assignation import AssignationAccessor
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.pointage.order_phase import OrderPhaseAccessor
from intranet.validators.iso_date_converter import IsoDateConverter

LOG = logging.getLogger(__name__)


class AssignationsController(RestController):
    """
    Assignation of users (employees) to a task.

    URL: http://127.0.0.1:8080/admin/order/159/tasks/792/assignations
    """

    def __init__(self):
        super(AssignationsController, self).__init__()
        # self.order_accessor = OrderAccessor()
        self.order_phase_accessor = OrderPhaseAccessor()
        self.employee_accessor = EmployeeAccessor()
        self.assignation_accessor = AssignationAccessor()

    # noinspection PyUnusedLocal
    def _before(self, *args, **kw):
        """
        URL: /admin/order/159/tasks/792/assignations
        """
        parts = request.url.split('/')
        order_index = parts.index("order")
        tasks_index = parts.index("tasks")
        assignations_index = parts.index("assignations")
        uid_list = parts[order_index + 1:tasks_index]
        self.order_uid = int(uid_list[0]) if uid_list else None
        uid_list = parts[tasks_index + 1:assignations_index]
        self.order_phase_uid = int(uid_list[0]) if uid_list else None

    @expose('intranet.templates.pointage.order.tasks.assignations.get_all')
    def get_all(self, **hidden):
        """
        Display all Assignations.
        """
        LOG.info(u"get_all:\n{0}".format(pprint.pformat(locals())))
        tz_offset = hidden["tz_offset"]
        tz_delta = datetime.timedelta(minutes=int(tz_offset))
        start_date_utc = datetime.datetime.now() + tz_delta
        active_employees = self.employee_accessor.get_active_employees(start_date_utc)
        task = self.order_phase_accessor.get_order_phase(self.order_phase_uid)
        return dict(task=task,
                    active_employees=active_employees,
                    hidden=hidden)

    @expose('intranet.templates.pointage.order.tasks.assignations.new')
    def new(self, employee_uid, **kwargs):
        """
        Display a page to prompt the User for Assignation creation.

        GET: /admin/order/159/tasks/792/assignations/new?tz_offset=-60&employee_uid=1

        :type employee_uid: unicode
        :param employee_uid: Selected employee UID.
        """
        LOG.info(u"new:\n{0}".format(pprint.pformat(locals())))
        keys = 'rate_percent', 'start_date', 'end_date'
        attrs = {k: v for k, v in kwargs.iteritems() if k in keys}
        hidden = {k: v for k, v in kwargs.iteritems() if k not in keys}
        # -- default values (first display of the form) + extra values
        if "tz_offset" in hidden:
            tz_offset = hidden["tz_offset"]
            tz_delta = datetime.timedelta(minutes=int(tz_offset))
            start_date = (datetime.datetime.utcnow() - tz_delta).date()
        else:
            # should never go here since tz_offset must be defined in the previous form.
            start_date = datetime.date.today()
        values = dict(rate_percent=80.0,
                      start_date=start_date,
                      end_date=None)
        values.update(attrs)
        form_errors = pylons.tmpl_context.form_errors
        employee = self.employee_accessor.get_employee(employee_uid)
        task = self.order_phase_accessor.get_order_phase(self.order_phase_uid)
        fmt = u'Assigner {employee.employee_name}'
        title = fmt.format(employee=employee, task=task)
        fmt = u'Voulez-vous assigner {employee.employee_name} à la tâche "{task.label}"\xa0?'
        question = fmt.format(employee=employee, task=task)
        integrity_error = hidden.pop("IntegrityError", None)
        fmt = u"Erreur d’intégrité : {message}"
        error_message = fmt.format(message=integrity_error) if integrity_error else None
        return dict(title=title,
                    question=question,
                    error_message=error_message,
                    employee=employee,
                    task=task,
                    form_errors=form_errors,
                    values=values,
                    hidden=hidden)

    @validate({'employee_uid': Number(min=1, not_empty=True),
               'rate_percent': Number(min=5.0, max=100.0, not_empty=True),
               'start_date': IsoDateConverter(not_empty=True),
               'end_date': IsoDateConverter(not_empty=False)},
              error_handler=new)
    @expose()
    def post(self, employee_uid, rate_percent, start_date, end_date, **hidden):
        """
        Create a new Assignation record.

        POST: /admin/order/159/tasks/792/assignations/

        :type employee_uid: int
        :param employee_uid: Selected employee UID.
        :type rate_percent: float
        :param rate_percent: Current rate: 0.5 <= rate_percent <= 100.0
        :type start_date: datetime.date
        :param start_date: Start date in local time.
        :type end_date: datetime.date
        :param end_date: End date in local time.
        """
        LOG.info(u"post:\n{0}".format(pprint.pformat(locals())))
        # We must have datetime instance to compute timezone shifting
        start_date = datetime.datetime.combine(start_date, datetime.time())
        end_date = datetime.datetime.combine(end_date, datetime.time()) if end_date else None
        tz_offset = hidden["tz_offset"]
        tz_delta = datetime.timedelta(minutes=int(tz_offset))
        start_date_utc = start_date + tz_delta
        end_date_utc = end_date + tz_delta if end_date else None
        try:
            self.assignation_accessor.insert_assignation(employee_uid,
                                                         self.order_phase_uid,
                                                         rate_percent,
                                                         start_date_utc,
                                                         end_date_utc)
        except sqlalchemy.exc.IntegrityError as exc:
            hidden["IntegrityError"] = exc.message
            redirect('./new',
                     employee_uid=employee_uid,
                     rate_percent=rate_percent,
                     start_date=start_date.date(),
                     end_date=end_date.date() if end_date else None,
                     **hidden)
        else:
            redirect('./new', employee_uid=employee_uid, **hidden)

    @expose('intranet.templates.pointage.order.tasks.assignations.edit')
    def edit(self, assignation_uid, **kwargs):
        """
        Display a page to prompt the User for resource modification.

        GET: /admin/order/159/tasks/792/assignations/new?tz_offset=-60&assignation_uid=1

        :type assignation_uid: unicode
        :param assignation_uid: Selected employee UID.
        """
        LOG.info(u"edit:\n{0}".format(pprint.pformat(locals())))
        keys = 'rate_percent', 'start_date', 'end_date'
        attrs = {k: v for k, v in kwargs.iteritems() if k in keys}
        hidden = {k: v for k, v in kwargs.iteritems() if k not in keys}
        assignation = self.assignation_accessor.get_assignation(assignation_uid)
        tz_offset = hidden["tz_offset"]
        tz_delta = datetime.timedelta(minutes=int(tz_offset))
        start_date_local = (assignation.start_date - tz_delta).date()
        end_date_local = None if assignation.end_date is None else (assignation.end_date - tz_delta).date()
        values = dict(rate_percent=assignation.rate_percent,
                      start_date=start_date_local,
                      end_date=end_date_local)
        values.update(attrs)
        form_errors = pylons.tmpl_context.form_errors
        employee = assignation.employee
        task = assignation.order_phase
        fmt = u'Modifier l’affectation de {employee.employee_name}'
        title = fmt.format(employee=employee, task=task)
        fmt = u'Voulez-vous modifier l’affectation de {employee.employee_name} à la tâche "{task.label}"\xa0?'
        question = fmt.format(employee=employee, task=task)
        integrity_error = hidden.pop("IntegrityError", None)
        fmt = u"Erreur d’intégrité : {message}"
        error_message = fmt.format(message=integrity_error) if integrity_error else None
        return dict(title=title,
                    question=question,
                    error_message=error_message,
                    employee=employee,
                    task=task,
                    assignation=assignation,
                    form_errors=form_errors,
                    values=values,
                    hidden=hidden)

    @validate({'rate_percent': Number(min=5.0, max=100.0, not_empty=True),
               'start_date': IsoDateConverter(not_empty=True),
               'end_date': IsoDateConverter(not_empty=False)},
              error_handler=new)
    @expose()
    def put(self, assignation_uid, rate_percent, start_date, end_date, **hidden):
        """
        Create a new Assignation record.

        POST: /admin/order/159/tasks/792/assignations/

        :type assignation_uid: int
        :param assignation_uid: Selected assignation UID.
        :type rate_percent: float
        :param rate_percent: Current rate: 0.5 <= rate_percent <= 100.0
        :type start_date: datetime.date
        :param start_date: Start date in local time.
        :type end_date: datetime.date
        :param end_date: End date in local time.
        """
        LOG.info(u"put:\n{0}".format(pprint.pformat(locals())))
        # We must have datetime instance to compute timezone shifting
        start_date = datetime.datetime.combine(start_date, datetime.time())
        end_date = datetime.datetime.combine(end_date, datetime.time()) if end_date else None
        tz_offset = hidden["tz_offset"]
        tz_delta = datetime.timedelta(minutes=int(tz_offset))
        start_date_utc = start_date + tz_delta
        end_date_utc = end_date + tz_delta if end_date else None
        try:
            self.assignation_accessor.update_assignation(assignation_uid,
                                                         rate_percent,
                                                         start_date_utc,
                                                         end_date_utc)
        except sqlalchemy.exc.IntegrityError as exc:
            hidden["IntegrityError"] = exc.message
            redirect('./edit',
                     rate_percent=rate_percent,
                     start_date=start_date.date(),
                     end_date=end_date.date() if end_date else None,
                     **hidden)
        else:
            redirect('./edit', **hidden)

    @expose()
    def post_delete(self, assignation_uid):
        """
        Delete an existing record.

        :type assignation_uid: int
        :param assignation_uid: Selected assignation UID.
        """
        LOG.info(u"post_delete:\n{0}".format(pprint.pformat(locals())))
        self.assignation_accessor.delete_assignation(assignation_uid)
        return dict()
