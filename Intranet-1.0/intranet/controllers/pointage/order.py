# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.order
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from formencode.validators import NotEmpty
from intranet.accessors import DuplicateFoundError
from intranet.accessors.order import OrderAccessor
from intranet.model.pointage.order import Order
from intranet.validators.iso_date_converter import IsoDateConverter
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate
from tg.flash import flash
import collections
import logging
import pylons

LOG = logging.getLogger(__name__)


class OrderController(RestController):
    """
    The 'order' controller
    """

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

    @with_trailing_slash
    @expose('intranet.templates.pointage.order.index')
    def index(self):
        """
        Display the index page.

        use '/pointage/order_cat.css' to get the order category's styles heet.
        """
        #order_list = (DBSession.query(Order)
        #              .order_by(Order.order_ref)
        #              .all())
        #return dict(order_list=order_list)
        return dict()

    @with_trailing_slash
    @expose('json')
    def get_one(self, uid):
        """
        Display one record.

        GET /pointage/order/1

        :param uid: UID of the order to display.
        """
        accessor = OrderAccessor()
        order = accessor.get_order(uid)
        order_cat_list = accessor.get_order_cat_list()
        cat_label_dict = {order_cat.cat_name: order_cat.label
                          for order_cat in order_cat_list}
        return dict(order=order,
                    order_phase_list=order.order_phase_list,
                    order_cat_label=cat_label_dict[order.project_cat])

    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.order.get_all')
    def get_all(self, keyword=None, uid=None):
        """
        Display all records in a resource.

        GET /pointage/order/

        :param uid: Active order's UID if any
        """
        # -- filter the order list/keyword
        accessor = OrderAccessor()
        order_by_cond = Order.order_ref
        filter_cond = (Order.order_ref.like('%' + keyword + '%')
                       if keyword else None)
        order_list = accessor.get_order_list(filter_cond, order_by_cond)

        # -- active_index of the order by uid
        active_index = False
        if uid:
            uid = int(uid)
            for index, order in enumerate(order_list):
                if order.uid == uid:
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
    @expose()
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
        try:
            accessor = OrderAccessor()
            accessor.insert_order(order_ref=order_ref,
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
            redirect('./new')

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
        creation_date = order.creation_date.strftime("%Y-%m-%d")
        close_date = (None if order.close_date is None
                      else order.close_date.strftime("%Y-%m-%d"))
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
