# -*- coding: utf-8 -*-
import datetime
import logging

import pylons
import sqlalchemy.exc
from formencode.validators import StringBool, Int, UnicodeString, Number, OneOf
from pylons import request
from tg import expose, validate, redirect
from tg.controllers import RestController

from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.pointage.order import OrderAccessor
from intranet.accessors.pointage.order_phase import OrderPhaseAccessor
from intranet.controllers.pointage.assignations import AssignationsController
from intranet.model.pointage.order_phase import ALL_TASK_STATUS

LOG = logging.getLogger(__name__)


class TasksController(RestController):
    """
    Manage the task list of a given order.

    .. versionadded:: 1.4.0

    .. versionchanged:: 2.2.0
       Full implementation.
    """
    assignations = AssignationsController()

    def __init__(self):
        super(TasksController, self).__init__()
        self.order_accessor = OrderAccessor()
        self.order_phase_accessor = OrderPhaseAccessor()
        self.employee_accessor = EmployeeAccessor()

    # noinspection PyUnusedLocal
    def _before(self, *args, **kw):
        """
        order/uid/tasks
        """
        parts = request.url.split('/')
        order_index = parts.index("order")
        tasks_index = parts.index("tasks")
        uid_list = parts[order_index + 1:tasks_index]
        self.order_uid = int(uid_list[0]) if uid_list else None

    @expose('intranet.templates.pointage.order.tasks.estimate_all_form')
    def estimate_all_form(self, closed=False, max_count=64, tz_offset=0):
        # In case of error, values are form values => need to convert
        closed = {"": None, "true": True, "false": False}.get(closed)
        max_count = int(max_count) if max_count else 64  # default value
        tz_offset = int(tz_offset) if tz_offset else 0
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        order = self.order_accessor.get_order(self.order_uid)
        title_fmt = u'Estimation de la durée des tâches pour "{order.order_ref}"'
        return dict(title=title_fmt.format(order=order),
                    order=order,
                    closed=closed,
                    max_count=max_count,
                    hidden=dict(tz_offset=tz_offset),
                    form_errors=form_errors)

    @validate({'closed': StringBool(),
               'max_count': Int(min=32, max=128, not_empty=True),
               'tz_offset': Int(not_empty=True)},
              error_handler=estimate_all_form)
    @expose()
    def estimate_all(self, closed=True, max_count=64, tz_offset=0):
        LOG.debug("estimate_all: "
                  "closed={closed!r},"
                  "max_count={max_count!r},"
                  "tz_offset={tz_offset!r}".format(**locals()))
        self.order_accessor.estimate_duration(self.order_uid, closed=closed, max_count=max_count)
        redirect('./',
                 closed=closed,
                 max_count=max_count,
                 tz_offset=tz_offset, )

    @expose('intranet.templates.pointage.order.tasks.estimate_one_form')
    def estimate_one_form(self, uid, closed=False, max_count=64, tz_offset=0):
        # In case of error, values are form values => need to convert
        closed = {"": None, "true": True, "false": False}.get(closed)
        max_count = int(max_count) if max_count else 64  # default value
        tz_offset = int(tz_offset) if tz_offset else 0
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        task = self.order_phase_accessor.get_order_phase(uid)
        title_fmt = u'Estimation de la durée de la tâche "{task.label}"'
        return dict(title=title_fmt.format(task=task),
                    task=task,
                    closed=closed,
                    max_count=max_count,
                    hidden=dict(tz_offset=tz_offset),
                    form_errors=form_errors)

    @validate({'uid': Int(min=1, not_empty=True),
               'closed': StringBool(),
               'max_count': Int(min=32, max=128, not_empty=True),
               'tz_offset': Int(not_empty=True)},
              error_handler=estimate_one_form)
    @expose()
    def estimate_one(self, uid, closed=True, max_count=64, tz_offset=0):
        LOG.debug("estimate_one: "
                  "closed={closed!r},"
                  "max_count={max_count!r},"
                  "tz_offset={tz_offset!r}".format(**locals()))
        self.order_accessor.estimate_duration(self.order_uid, order_phase_uid=uid, closed=closed, max_count=max_count)
        redirect('./edit',
                 uid=uid,
                 closed=closed,
                 max_count=max_count,
                 tz_offset=tz_offset, )

    @expose('json')
    def get_one(self, uid, **kwargs):
        task = self.order_phase_accessor.get_order_phase(uid)
        return dict(task=task, **kwargs)

    # noinspection PyUnusedLocal
    @expose('intranet.templates.pointage.order.tasks.get_all')
    def get_all(self, **hidden):
        tz_offset = hidden["tz_offset"]
        tz_delta = datetime.timedelta(minutes=int(tz_offset))
        start_date_utc = datetime.datetime.now() + tz_delta
        active_employees = self.employee_accessor.get_active_employees(start_date_utc)
        order = self.order_accessor.get_order(self.order_uid)
        title_fmt = u"Liste des tâches de la commande {order_ref}"
        return dict(title=title_fmt.format(order_ref=order.order_ref),
                    order=order,
                    active_employees=active_employees,
                    hidden=hidden)

    @expose('intranet.templates.pointage.order.tasks.edit')
    def edit(self, uid, **kwargs):
        keys = 'label', 'description', 'estimated_duration', 'remain_duration', 'task_status'
        attrs = {k: v for k, v in kwargs.iteritems() if k in keys}
        hidden = {k: v for k, v in kwargs.iteritems() if k not in keys}
        tz_offset = hidden["tz_offset"]
        tz_delta = datetime.timedelta(minutes=int(tz_offset))
        start_date_utc = datetime.datetime.now() + tz_delta
        active_employees = self.employee_accessor.get_active_employees(start_date_utc)
        task = self.order_phase_accessor.get_order_phase(uid)
        values = dict(label=task.label,
                      description=task.description,
                      estimated_duration=task.estimated_duration,
                      remain_duration=task.remain_duration,
                      task_status=task.task_status)
        values.update(attrs)
        form_errors = pylons.tmpl_context.form_errors
        return dict(task=task,
                    active_employees=active_employees,
                    form_errors=form_errors,
                    values=values,
                    hidden=hidden)

    # noinspection PyUnusedLocal
    @validate({'uid': Int(not_empty=True),
               'label': UnicodeString(not_empty=True),
               'description': UnicodeString(if_empty=u""),
               'estimated_duration': Number(if_empty=0),
               'tracked_duration': Number(if_empty=0),
               'remain_duration': Number(if_empty=0),
               'task_status': OneOf(ALL_TASK_STATUS, not_empty=True)},
              error_handler=edit)
    @expose()
    def put(self, uid,
            label,
            description,
            estimated_duration,
            tracked_duration,
            remain_duration,
            task_status,
            **hidden):
        u"""
        PUT /admin/order/index.html

        Arguments are:

        - label = "Commercialisation / Étude"
        - description = "Commercialisation / Étude"
        - estimated_duration = 2.25
        - remain_duration = 2.25
        - task_status = "PENDING"

        :param uid: OrderPhase UID
        :param label: the order phase label (required)
        :param description: the order phase description (more a task description)
        :param estimated_duration: Estimated duration (calculated).
        :param remain_duration: Remain duration
        :param tracked_duration: Tacked duration (not used)
        :param task_status: Task status: "PENDING", "IN_PROGRESS", "DONE".
        :param hidden: extra parameters (not used).
        """
        attrs = dict(label=label,
                     description=description,
                     estimated_duration=estimated_duration,
                     remain_duration=remain_duration,
                     task_status=task_status)
        LOG.debug("put: attrs={attrs!r}".format(**locals()))
        try:
            self.order_phase_accessor.update_order_phase(uid, **attrs)
        except sqlalchemy.exc.IntegrityError as exc:
            LOG.warning(u"Trouble", exc_info=True)
            form_errors = pylons.tmpl_context.form_errors
            form_errors["exc"] = exc.message
            attrs.update(hidden)
            redirect('./{uid}/edit'.format(uid=uid), **attrs)
        else:
            redirect('./{uid}/edit'.format(uid=uid), **hidden)
