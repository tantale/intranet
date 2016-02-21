# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.order
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections
import datetime
import logging

import pylons
import sqlalchemy.exc
from formencode.validators import Int, NotEmpty, StringBool, Number, UnicodeString, OneOf
from sqlalchemy.sql.expression import desc
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate, without_trailing_slash, request
from tg.flash import flash
from tg.i18n import ugettext as _

from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.pointage.order import OrderAccessor
from intranet.accessors.pointage.order_phase import OrderPhaseAccessor
from intranet.controllers.session_obj.layout import LayoutController
from intranet.model.pointage.order import Order
from intranet.model.pointage.order_phase import ALL_TASK_STATUS
from intranet.validators.date_interval import check_date_interval
from intranet.validators.iso_date_converter import IsoDateConverter

LOG = logging.getLogger(__name__)


class TasksController(RestController):
    """
    Manage the task list of a given order.

    .. versionadded:: 1.4.0

    .. note::
        This controller is experimental.
    """

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


class OrderController(RestController):
    """
    The 'order' controller

    .. versionchanged:: 1.4.0
        Add layout controller to memorize the position of the left frame.

        Use a (new) :class:`TasksController` to manage the task list of a given order.
    """
    layout = LayoutController("order")
    tasks = TasksController()

    MISSING_ORDER_CAT_LABEL = _(u"(sans catégorie)")

    def __init__(self, main_menu):
        self.main_menu = main_menu
        self.order_accessor = OrderAccessor()

    # noinspection PyMethodMayBeStatic
    def _get_cat_dict(self):
        """
        :return: order categories grouped by category's group.
        """
        cat_dict = collections.OrderedDict()
        accessor = OrderAccessor()
        order_cat_list = accessor.get_order_cat_list()
        for order_cat in order_cat_list:
            if order_cat.cat_group not in cat_dict:
                cat_dict[order_cat.cat_group] = []
            cat_dict[order_cat.cat_group].append(order_cat)
        return cat_dict

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('intranet.templates.pointage.order.index')
    def index(self, uid=None, keyword=None):
        """
        Display the index page.

        :param uid: Order UID
        :param keyword: Search keyword.
        """
        return dict(main_menu=self.main_menu, uid=uid, keyword=keyword)

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('json')
    def get_one(self, uid):
        """
        Display one record.

        GET /pointage/order/1
        GET /pointage/order/1.json
        GET /pointage/order/get_one?uid=1
        GET /pointage/order/get_one.json?uid=1

        :param uid: UID of the order to display.
        """
        order = self.order_accessor.get_order(uid)
        order_cat_list = self.order_accessor.get_order_cat_list()
        cat_label_dict = {order_cat.cat_name: order_cat.label
                          for order_cat in order_cat_list}
        # populate the lazy loaded order_phase_list for json result:
        # noinspection PyUnusedLocal
        __ = order.order_phase_list

        return dict(order=order,
                    order_cat_label=cat_label_dict.get(order.project_cat, self.MISSING_ORDER_CAT_LABEL))

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.order.get_all')
    def get_all(self, keyword=None, uid=None, order_ref=None):
        """
        Get all order matching the given query.

        GET /pointage/order/
        GET /pointage/order.json
        GET /pointage/order/get_all
        GET /pointage/order/get_all.json

        :param keyword: Search keyword (for ``order_ref`` field), or empty.
        :param uid: The currently selected ``uid``, or empty if none is selected.
        :param order_ref: The currently selected ``order_ref``, or empty if none is selected.
        """
        uid = int(uid) if uid else None  # not: uid can't be 0

        # -- filter the order list/keyword
        order_by_cond = desc(Order.creation_date)
        filter_cond = (Order.order_ref.like('%' + keyword + '%')
                       if keyword else None)
        order_list = self.order_accessor.get_order_list(filter_cond, order_by_cond)

        # -- Limit the list to 25 orders
        order_list[:] = order_list[:25]

        # -- but add missing matches
        if uid:
            extras = self.order_accessor.get_order_list(Order.uid == uid)
            order_list.extend(extras)
        if order_ref:
            extras = self.order_accessor.get_order_list(Order.order_ref == order_ref)
            order_list.extend(extras)
        order_list.sort(key=lambda o: o.creation_date, reverse=True)

        # -- active_index of the order by uid
        active_index = False
        if uid:
            for index, order in enumerate(order_list):
                if order.uid == uid:
                    active_index = index
                    break
        elif order_ref:
            for index, order in enumerate(order_list):
                if order.order_ref == order_ref:
                    active_index = index
                    break
        return dict(order_list=order_list, keyword=keyword,
                    active_index=active_index)

    @expose('intranet.templates.pointage.order.new')
    def new(self, **kw):
        """
        Display a page to prompt the User for resource creation:

        GET /pointage/order/new
        """
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = u"Le formulaire comporte des champs invalides"
            flash(err_msg, status="error")
        cat_dict = self._get_cat_dict()
        values = dict(creation_date=datetime.date.today())
        values.update(kw)
        return dict(values=values,
                    cat_dict=cat_dict,
                    missing_order_cat_label=self.MISSING_ORDER_CAT_LABEL,
                    form_errors=form_errors)

    @validate({'order_ref': NotEmpty(),
               'project_cat': NotEmpty(),
               'creation_date': IsoDateConverter(not_empty=True),
               'close_date': IsoDateConverter(not_empty=False)},
              error_handler=new)
    @expose('json')
    def post(self, order_ref, project_cat, creation_date, close_date=None):
        """
        Create a new record.

        POST /pointage/order/

        :param order_ref: the order's reference (unique and not null)

        :param project_cat: the project's category which determines
        its color (required)

        :param creation_date: creation date (required)
        :type creation_date: datetime.date

        :param close_date: close date, or None if it's status is in progress.
        :type close_date: datetime.date
        """
        ctrl_dict = check_date_interval(creation_date, close_date)
        if ctrl_dict['status'] != "ok":
            flash(ctrl_dict['message'], status=ctrl_dict['status'])
            redirect('./new',
                     order_ref=order_ref,
                     project_cat=project_cat,
                     creation_date=creation_date,
                     close_date=close_date)

        try:

            values = self.order_accessor.insert_order(order_ref=order_ref,
                                                      project_cat=project_cat,
                                                      creation_date=creation_date,
                                                      close_date=close_date)
        except sqlalchemy.exc.IntegrityError:
            msg_fmt = u"La commande « {order_ref} » existe déjà."
            err_msg = msg_fmt.format(order_ref=order_ref)
            flash(err_msg, status="error")
            redirect('./new',
                     order_ref=order_ref,
                     project_cat=project_cat,
                     creation_date=creation_date,
                     close_date=close_date)
        else:
            msg_fmt = u"La commande « {order_ref} » est créée."
            flash(msg_fmt.format(order_ref=order_ref), status="ok")
            return dict(action='post',
                        result='ok',
                        values=values)

    @expose('intranet.templates.pointage.order.edit')
    def edit(self, uid, **kw):
        """
        Display a page to prompt the User for resource modification.

        GET /pointage/order/1/edit

        :param uid: UID of the Order to edit
        """
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        order = self.order_accessor.get_order(uid)
        creation_date = order.creation_date.isoformat()
        close_date = (None if order.close_date is None
                      else order.close_date.isoformat())
        values = dict(uid=order.uid,
                      order_ref=order.order_ref,
                      project_cat=order.project_cat,
                      creation_date=creation_date,
                      close_date=close_date)
        values.update(kw)
        cat_dict = self._get_cat_dict()
        return dict(values=values, cat_dict=cat_dict,
                    missing_order_cat_label=self.MISSING_ORDER_CAT_LABEL,
                    form_errors=form_errors)

    # noinspection PyUnusedLocal
    @validate({'order_ref': NotEmpty(),
               'project_cat': NotEmpty(),
               'creation_date': IsoDateConverter(not_empty=True),
               'close_date': IsoDateConverter(not_empty=False)},
              error_handler=edit)
    @expose()
    def put(self, uid, order_ref, project_cat, creation_date, close_date, **kw):
        """
        Update an existing record.

        POST /pointage/order/1?_method=PUT
        PUT /pointage/order/1

        :param uid: UID of the Order to update

        :param order_ref: the order's reference (unique and not null)

        :param project_cat: the project's category which determines
        its color (required)

        :param creation_date: creation date (required)
        :type creation_date: datetime.date

        :param close_date: close date, or None if it's status is in progress.
        :type close_date: datetime.date
        """
        ctrl_dict = check_date_interval(creation_date, close_date)
        if ctrl_dict['status'] != "ok":
            flash(ctrl_dict['message'], status=ctrl_dict['status'])
            redirect('./{uid}/edit'.format(uid=uid),
                     order_ref=order_ref,
                     project_cat=project_cat,
                     creation_date=creation_date,
                     close_date=close_date)

        try:

            self.order_accessor.update_order(uid,
                                             order_ref=order_ref,
                                             project_cat=project_cat,
                                             creation_date=creation_date,
                                             close_date=close_date)
        except sqlalchemy.exc.IntegrityError:
            msg_fmt = u"La commande « {order_ref} » existe déjà."
            err_msg = msg_fmt.format(order_ref=order_ref)
            flash(err_msg, status="error")
            redirect('./{uid}/edit'.format(uid=uid),
                     order_ref=order_ref,
                     project_cat=project_cat,
                     creation_date=creation_date,
                     close_date=close_date)
        else:
            msg_fmt = u"La commande « {order_ref} » est modifiée."
            flash(msg_fmt.format(order_ref=order_ref), status="ok")
            redirect('./{uid}/edit'.format(uid=uid))

    @expose('json')
    def duplicate(self, uid):
        """
        Duplicate an existing record.

        GET /pointage/order/duplicate?uid=1

        :param uid: UID of the Order to delete.
        """
        values = self.order_accessor.duplicate(uid)
        return dict(action='duplicate',
                    result='ok',
                    values=values)

    @expose('intranet.templates.pointage.order.get_delete')
    def get_delete(self, uid):
        """
        Display a delete Confirmation page.

        GET /pointage/order/1/delete

        :param uid: UID of the Order to delete.
        """
        order = self.order_accessor.get_order(uid)
        return dict(order=order)

    @expose('intranet.templates.pointage.order.get_delete')
    def post_delete(self, uid):
        """
        Delete an existing record.

        POST /pointage/order/1?_method=DELETE
        DELETE /pointage/order/1

        :param uid: UID of the Order to delete.
        """
        old_order = self.order_accessor.delete_order(uid)
        msg_fmt = u"La commande « {order_ref} » est supprimée."
        flash(msg_fmt.format(order_ref=old_order.order_ref), status="ok")
        return dict(order=None)
