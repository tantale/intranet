# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.order_phase
:date: 2013-08-29
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from formencode.validators import NotEmpty
from intranet.model import DBSession
from intranet.model.pointage.order import Order
from intranet.model.pointage.order_phase import OrderPhase
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate
from tg.flash import flash
import logging
import pylons

LOG = logging.getLogger(__name__)


class OrderPhaseController(RestController):
    """
    Order phase controller.
    """

    @with_trailing_slash
    @expose('json')
    def get_one(self, uid):
        """
        Display one record.

        GET /pointage/order_phase/1

        :param uid: UID of the order phase to display.
        """
        order_phase = DBSession.query(OrderPhase).get(uid)
        return dict(order_phase=order_phase)

    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.order_phase.get_all')
    def get_all(self, order_uid):
        """
        Display all records in a resource.

        GET /pointage/order_phase/?order_uid

        :param order_uid: Current order's UID
        """
        LOG.info("get_all")
        order = DBSession.query(Order).get(order_uid)
        return dict(order_uid=order_uid,
                    project_cat=order.project_cat,
                    order_phase_list=order.order_phase_list)

    @expose('intranet.templates.pointage.order_phase.new')
    def new(self, order_uid, **kw):
        """
        Display a page to prompt the User for resource creation:

        GET /pointage/order_phase/new?order_uid

        :param order_uid: Current order's UID
        """
        LOG.info("new")
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = (u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(order_uid=order_uid, values=kw, errors=form_errors)

    @validate({'label': NotEmpty}, error_handler=get_all)
    @expose()
    def post(self, order_uid, label):
        """
        Create a new record.

        POST /pointage/order_phase/

        :param order_uid: Current order's UID

        :param label: the order phase's label (not null)
        """
        LOG.info("post")
        order = DBSession.query(Order).get(order_uid)
        OrderPhase(order, label)
        DBSession.flush()
        msg_fmt = (u"La phase de commande « {label} » est créée.")
        flash(msg_fmt.format(label=label), status="ok")
        redirect('./get_all', order_uid=order_uid)

    @expose('intranet.templates.pointage.order_phase.edit')
    def edit(self, order_uid, uid, **kw):
        """
        Display a page to prompt the User for resource modification.

        GET /pointage/order_phase/1/?order_uid

        :param order_uid: Current order's UID

        :param uid: UID of the OrderPhase to edit
        """
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        order_phase = DBSession.query(OrderPhase).get(uid)
        values = dict(uid=order_phase.uid,
                      label=order_phase.label)
        values.update(kw)
        return dict(order_uid=order_uid, values=values,
                    form_errors=form_errors)

    @expose()
    def edit_in_place(self, element_id,
                      original_value, update_value, original_html):
        """
        Edit an order phase label in place.

        :param element_id: HTML element id.

        :param original_value: original value.

        :param update_value: update value.

        :param original_html: original html's content.
        """
        msg_fmt = (u"edit_in_place: "
                   u"element_id={element_id!r}, "
                   u"original_value={original_value!r}, "
                   u"update_value={update_value!r}, "
                   u"original_html={original_html!r}, ")
        LOG.info(msg_fmt.format(element_id=element_id,
                                original_value=original_value,
                                update_value=update_value,
                                original_html=original_html))
        uid = int(element_id.rsplit('_', 1)[1])
        order_phase = DBSession.query(OrderPhase).get(uid)
        order_phase.label = update_value
        DBSession.flush()
        return update_value

    @validate({'label': NotEmpty}, error_handler=edit)
    @expose()
    def put(self, order_uid, uid, label, **kw):
        """
        Update an existing record.

        POST /pointage/order_phase/1?_method=PUT
        PUT /pointage/order_phase/1

        :param order_uid: Current order's UID

        :param uid: UID of the OrderPhase to update

        :param label: the order phase's label (not null)
        """
        order_phase = DBSession.query(OrderPhase).get(uid)
        order_phase.label = label
        DBSession.flush()
        msg_fmt = (u"La phase de commande « {label} » est modifiée.")
        flash(msg_fmt.format(label=label), status="ok")
        redirect('./{uid}/edit'.format(uid=uid))

    @expose('intranet.templates.pointage.order_phase.get_delete')
    def get_delete(self, uid):
        """
        Display a delete Confirmation page.

        GET /pointage/order_phase/1/delete

        :param uid: UID of the OrderPhase to delete.
        """
        order_phase = DBSession.query(OrderPhase).get(uid)
        return dict(order_phase=order_phase)

    @expose('intranet.templates.pointage.order_phase.get_delete')
    def post_delete(self, uid):
        """
        Delete an existing record.

        POST /pointage/order_phase/1?_method=DELETE
        DELETE /pointage/order_phase/1

        :param uid: UID of the OrderPhase to delete.
        """
        order_phase = DBSession.query(OrderPhase).get(uid)
        DBSession.delete(order_phase)
        msg_fmt = (u"La phase de commande « {label} » est supprimée.")
        flash(msg_fmt.format(label=order_phase.label), status="ok")
        return dict(order_phase=None)
