# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.order_phase
:date: 2013-08-29
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import logging

import pylons
from formencode.validators import NotEmpty
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate
from tg.flash import flash

from intranet.accessors.pointage.order_phase import OrderPhaseAccessor

LOG = logging.getLogger(__name__)


class OrderPhaseController(RestController):
    """
    Order phase controller.
    """

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('json')
    def get_one(self, uid):
        """
        Display one record.

        GET /pointage/order_phase/1

        :param uid: UID of the order phase to display.
        """
        accessor = OrderPhaseAccessor()
        order_phase = accessor.get_order_phase(uid)
        return dict(order_phase=order_phase)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.order_phase.get_all')
    def get_all(self, order_uid, editable=True, selectable=False):
        """
        Display all records in a resource.

        GET /pointage/order_phase/?order_uid

        :param order_uid: Current order's UID
        :param editable: ``True`` if the list is editable.
        :param selectable: ``True``is the list is selectable.
        """

        def asbool(obj):
            return str(obj).lower() in ('true', 'yes', 'on', 'y', 't', '1')

        editable = asbool(editable)
        selectable = asbool(selectable)

        LOG.info("get_all")

        accessor = OrderPhaseAccessor()
        order = accessor.get_order(order_uid)
        return dict(order_uid=order_uid,
                    project_cat=order.project_cat,
                    order_phase_list=order.order_phase_list,
                    editable=editable,
                    selectable=selectable)

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
            err_msg = u"Le formulaire comporte des champs invalides"
            flash(err_msg, status="error")
        return dict(order_uid=order_uid, values=kw, errors=form_errors)

    @validate({'label': NotEmpty()}, error_handler=get_all)
    @expose()
    def post(self, order_uid, label):
        """
        Create a new record.

        POST /pointage/order_phase/

        :param order_uid: Current order's UID

        :param label: the order phase's label (not null)
        """
        LOG.info("post")
        accessor = OrderPhaseAccessor()
        accessor.insert_order_phase(order_uid, label=label)
        msg_fmt = u"La phase de commande « {label} » est créée."
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
        accessor = OrderPhaseAccessor()
        order_phase = accessor.get_order_phase(uid)
        values = dict(uid=order_phase.uid,
                      label=order_phase.label)
        values.update(kw)
        return dict(order_uid=order_uid, values=values,
                    form_errors=form_errors)

    @expose('json')
    def edit_in_place(self, **kw):
        """
        Edit an order phase label in place.

        kw = {'pk': u'unused',
              'name': u'order_phase_label_2',
              'value': u'Hello'}
        """
        if LOG.isEnabledFor(logging.INFO):
            LOG.info(u"edit_in_place: {args!r}".format(args=kw))
        label = kw['value']
        uid = int(kw['name'].rsplit('_', 1)[1])
        accessor = OrderPhaseAccessor()
        return accessor.edit_label_in_place(uid, label)

    # noinspection PyUnusedLocal
    @validate({'label': NotEmpty()}, error_handler=edit)
    @expose()
    def put(self, order_uid, uid, label, **kw):
        """
        Update an existing record.

        POST /pointage/order_phase/1?_method=PUT
        PUT /pointage/order_phase/1

        :param order_uid: Current order's UID (not used)

        :param uid: UID of the OrderPhase to update

        :param label: the order phase's label (not null)
        """
        accessor = OrderPhaseAccessor()
        accessor.update_order_phase(uid, label=label)
        msg_fmt = u"La phase de commande « {label} » est modifiée."
        flash(msg_fmt.format(label=label), status="ok")
        redirect('./{uid}/edit'.format(uid=uid))

    @expose('intranet.templates.pointage.order_phase.get_delete')
    def get_delete(self, uid):
        """
        Display a delete Confirmation page.

        GET /pointage/order_phase/1/delete

        :param uid: UID of the OrderPhase to delete.
        """
        accessor = OrderPhaseAccessor()
        order_phase = accessor.get_order_phase(uid)
        return dict(order_phase=order_phase)

    @expose('intranet.templates.pointage.order_phase.get_delete')
    def post_delete(self, uid):
        """
        Delete an existing record.

        POST /pointage/order_phase/1?_method=DELETE
        DELETE /pointage/order_phase/1

        :param uid: UID of the OrderPhase to delete.
        """
        accessor = OrderPhaseAccessor()
        old_order_phase = accessor.delete_order_phase(uid)
        msg_fmt = u"La phase de commande « {label} » est supprimée."
        flash(msg_fmt.format(label=old_order_phase.label), status="ok")
        return dict(order_phase=None)

    @expose('json')
    def reorder(self, uids, delim=u'|'):
        """
        Re-order a list of phases.

        :param uids: String representation of a UID list.
        :param delim: UID delimiter.
        """
        msg_fmt = u"reorder: uids='{uids}', delim='{delim}'"
        LOG.info(msg_fmt.format(uids=uids, delim=delim))
        accessor = OrderPhaseAccessor()
        accessor.reorder_position(uids, delim)
        return dict(status='success')
