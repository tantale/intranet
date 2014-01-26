# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.order
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections
from intranet.accessors import DuplicateFoundError
from intranet.accessors.order import OrderAccessor
from intranet.model.pointage.order import Order
from intranet.validators.date_interval import check_date_interval
from intranet.validators.iso_date_converter import IsoDateConverter
import logging

from formencode.validators import NotEmpty
import pylons
from sqlalchemy.sql.expression import desc
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate, \
    without_trailing_slash
from tg.flash import flash


LOG = logging.getLogger(__name__)


class OrderController(RestController):
    """
    The 'order' controller
    """

    def __init__(self, main_menu):
        self.main_menu = main_menu

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

    @without_trailing_slash
    @expose('intranet.templates.pointage.order.index')
    def index(self):
        """
        Display the index page.
        """
        return dict(main_menu=self.main_menu)

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
        accessor = OrderAccessor()
        order = accessor.get_order(uid)
        order_cat_list = accessor.get_order_cat_list()
        cat_label_dict = {order_cat.cat_name: order_cat.label
                          for order_cat in order_cat_list}
        # populate the lazy loaded order_phase_list for json result:
        __ = order.order_phase_list
        return dict(order=order,
                    order_cat_label=cat_label_dict[order.project_cat])

    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.order.get_all')
    def get_all(self, keyword=None, uid=None, order_ref=None,
                _heavy_loading=False):
        """
        Display all records in a resource.

        GET /pointage/order/
        GET /pointage/order.json
        GET /pointage/order/get_all
        GET /pointage/order/get_all.json

        :param uid: Active order's UID if any
        """
        # -- filter the order list/keyword
        accessor = OrderAccessor()
        order_by_cond = desc(Order.creation_date)
        filter_cond = (Order.order_ref.like('%' + keyword + '%')
                       if keyword else None)
        order_list = accessor.get_order_list(filter_cond, order_by_cond)

        # -- heavy loading for debug
        if _heavy_loading:
            for order in order_list:
                order.order_phase_list

        # -- active_index of the order by uid
        active_index = False
        if uid:
            uid = int(uid)
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
            err_msg = (u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        cat_dict = self._get_cat_dict()
        return dict(values=kw, cat_dict=cat_dict,
                    form_errors=form_errors)

    @validate({'order_ref': NotEmpty,
               'project_cat': NotEmpty,
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
            accessor = OrderAccessor()
            values = accessor.insert_order(order_ref=order_ref,
                                           project_cat=project_cat,
                                           creation_date=creation_date,
                                           close_date=close_date)
        except DuplicateFoundError:
            msg_fmt = (u"La commande « {order_ref} » existe déjà.")
            err_msg = msg_fmt.format(order_ref=order_ref)
            flash(err_msg, status="error")
            redirect('./new',
                     order_ref=order_ref,
                     project_cat=project_cat,
                     creation_date=creation_date,
                     close_date=close_date)
        else:
            msg_fmt = (u"La commande « {order_ref} » est créée.")
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
        accessor = OrderAccessor()
        order = accessor.get_order(uid)
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
                    form_errors=form_errors)

    @validate({'order_ref': NotEmpty,
               'project_cat': NotEmpty,
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
            accessor = OrderAccessor()
            accessor.update_order(uid,
                                  order_ref=order_ref,
                                  project_cat=project_cat,
                                  creation_date=creation_date,
                                  close_date=close_date)
        except DuplicateFoundError:
            msg_fmt = (u"La commande « {order_ref} » existe déjà.")
            err_msg = msg_fmt.format(order_ref=order_ref)
            flash(err_msg, status="error")
            redirect('./{uid}/edit'.format(uid=uid),
                     order_ref=order_ref,
                     project_cat=project_cat,
                     creation_date=creation_date,
                     close_date=close_date)
        else:
            msg_fmt = (u"La commande « {order_ref} » est modifiée.")
            flash(msg_fmt.format(order_ref=order_ref), status="ok")
            redirect('./{uid}/edit'.format(uid=uid))

    @expose('json')
    def duplicate(self, uid):
        """
        Duplicate an existing record.

        GET /pointage/order/duplicate?uid=1

        :param uid: UID of the Order to delete.
        """
        accessor = OrderAccessor()
        values = accessor.duplicate(uid)
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
        accessor = OrderAccessor()
        order = accessor.get_order(uid)
        return dict(order=order)

    @expose('intranet.templates.pointage.order.get_delete')
    def post_delete(self, uid):
        """
        Delete an existing record.

        POST /pointage/order/1?_method=DELETE
        DELETE /pointage/order/1

        :param uid: UID of the Order to delete.
        """
        accessor = OrderAccessor()
        old_order = accessor.delete_order(uid)
        msg_fmt = (u"La commande « {order_ref} » est supprimée.")
        flash(msg_fmt.format(order_ref=old_order.order_ref), status="ok")
        return dict(order=None)
