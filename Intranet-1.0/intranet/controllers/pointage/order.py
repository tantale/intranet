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
from formencode.validators import Int, NotEmpty, StringBool
from sqlalchemy.sql.expression import desc, and_
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate, without_trailing_slash, request
from tg.flash import flash
from tg.i18n import ugettext as _

from intranet.accessors.pointage.order import OrderAccessor
from intranet.controllers.session_obj.layout import LayoutController
from intranet.model.pointage.order import Order
from intranet.model.pointage.order_phase import OrderPhase
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

    # noinspection PyUnusedLocal
    def _before(self, *args, **kw):
        """
        order/uid/tasks
        """
        # http://127.0.0.1:8080/admin/order/160/tasks/estimate_form
        parts = request.url.split('/')
        index = parts.index("tasks")
        self.order_uid = int(parts[index - 1])

    @expose('intranet.templates.pointage.order.tasks.estimate_form')
    def estimate_form(self, closed=False, max_count=64):
        # In case of error, values are form values => need to convert
        if closed in ("", "true", "false"):
            closed = closed == "true" if closed else None
        max_count = int(max_count) if max_count else 64  # default value
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        return dict(order_uid=self.order_uid,
                    closed=closed,
                    max_count=max_count,
                    form_errors=form_errors)

    @validate({'closed': StringBool(),
               'max_count': Int(min=32, max=128, not_empty=True)},
              error_handler=estimate_form)
    @expose('intranet.templates.pointage.order.tasks')
    def estimate_tasks(self, closed=True, max_count=64):
        LOG.debug("estimate_tasks: closed={closed!r}, max_count={max_count!r}".format(**locals()))
        order_accessor = OrderAccessor()
        order_accessor.estimate_duration(self.order_uid, closed=closed, max_count=max_count)
        order = order_accessor.get_order(self.order_uid)
        task_list = order.order_phase_list
        return dict(order=order, task_list=task_list, sample_count=max_count)

    @expose('intranet.templates.pointage.order.tasks')
    def get_all(self, **kwargs):
        """
        Get the tasks of the given order.
        """
        accessor = OrderAccessor()
        order = accessor.get_order(self.order_uid)

        # -- Search order of the same project category
        same_cat = Order.project_cat == order.project_cat

        # Not too old: 1/2 year, one year, two years, all records
        for days in (182, 365, 730, None):
            if days:
                start_date = order.creation_date - datetime.timedelta(days=days)
                not_too_old = Order.creation_date > start_date
                order_filter = and_(same_cat, not_too_old)
            else:
                order_filter = same_cat
            sample_list = accessor.get_order_list(order_filter)
            if len(sample_list) > 30:
                break

        # -- Prepare a list of tasks
        task_list = []

        # noinspection PyPep8Naming
        Task = collections.namedtuple("Task", "display_name description position "
                                              "done_duration remain_duration total_duration min_duration max_duration")

        for order_phase in order.order_phase_list:
            assert isinstance(order_phase, OrderPhase)

            # find the orders which phase duration is not null
            key = (order_phase.position, order_phase.label)
            duration_list = [x.statistics[key] for x in sample_list
                             if x.statistics[key] != 0]

            done_duration = order.statistics[key]
            if len(duration_list):
                total_duration = max(done_duration, float(sum(duration_list)) / len(duration_list))
                remain_duration = total_duration - done_duration
                min_duration = min(duration_list)
                max_duration = max(duration_list)
            else:
                total_duration = done_duration or None
                remain_duration = total_duration - done_duration if total_duration else None
                min_duration = None
                max_duration = None

            round4 = lambda x: None if x is None else int(x * 4) / 4.0
            task = Task(display_name=order_phase.label,
                        description=u"",
                        position=order_phase.position,
                        done_duration=round4(done_duration),
                        remain_duration=round4(remain_duration),
                        total_duration=round4(total_duration),
                        min_duration=round4(min_duration),
                        max_duration=round4(max_duration))
            task_list.append(task)
        task_list.sort(key=lambda x: x.position)
        return dict(order=order, task_list=task_list, sample_count=len(sample_list))


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

    @validate({'order_ref': NotEmpty(),
               'project_cat': NotEmpty(),
               'creation_date': IsoDateConverter(not_empty=True),
               'close_date': IsoDateConverter(not_empty=False)},
              error_handler=edit)
    @expose()
    def put(self, uid, order_ref, project_cat, creation_date, close_date,
            **kw):
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
