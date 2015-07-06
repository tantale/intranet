# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.order_cat
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections
import logging
from pprint import pformat

import transaction
from tg.i18n import ugettext as _
from formencode.validators import NotEmpty, Regex
import pylons
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import expose, with_trailing_slash, validate, without_trailing_slash
from tg.flash import flash
import sqlalchemy.exc
from intranet.accessors import RecordNotFoundError

from intranet.accessors.order import OrderAccessor
from intranet.accessors.order_cat import OrderCatAccessor
from intranet.model.pointage.order import Order

LOG = logging.getLogger(__name__)


class OrderCatController(RestController):
    """
    Order category controller
    """
    DISPLAY_NORMAL, DISPLAY_DETAIL = 'normal', 'detail'

    def _prepare(self, **kw):
        accessor = OrderCatAccessor()
        order_cat_list = accessor.get_order_cat_list()
        self.cat_group_index = collections.defaultdict(list)
        for order_cat in order_cat_list:
            self.cat_group_index[order_cat.cat_group].append(order_cat)
        self.cat_group = kw.get('cat_group')
        self.order_cat_list = self.cat_group_index.get(self.cat_group, order_cat_list)
        self.display = kw.get('display', self.DISPLAY_NORMAL)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.pointage.order_cat.index")
    def index(self, **kw):
        LOG.info("OrderCatController.index, kw = " + pformat(kw))
        return dict(values=kw)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.order_cat.get_all')
    @expose('intranet.templates.pointage.order_cat.get_all_css',
            content_type='text/css')
    def get_all(self, **kw):
        """
        Display all OrderCat in a resource.

        GET /pointage/order_cat/
        """
        LOG.info("OrderCatController.get_all, kw = " + pformat(kw))
        self._prepare(**kw)
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(display=self.display, cat_group=self.cat_group, order_cat_list=self.order_cat_list,
                    cat_group_index=self.cat_group_index, form_errors=form_errors, values=kw)

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('intranet.templates.pointage.order_cat.new')
    def new(self, **kw):
        """
        Display a page to prompt the User for resource creation:

        GET /pointage/order_cat/new
        """
        LOG.info("OrderCatController.new, kw={0}".format(pformat(kw)))
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(values=kw, form_errors=form_errors)

    @validate({'cat_group': NotEmpty(),
               'code': Regex(r'^\w+$', not_empty=True),
               'label': NotEmpty(),
               'color': NotEmpty(),
               'background-color': NotEmpty()},
              error_handler=new)
    @expose()
    def post(self, cat_group, code, label, **kw):
        LOG.info("OrderCatController.post, kw={0}".format(pformat(kw)))
        try:
            self.insert_order_cat(cat_group, code, label, kw)
        except Exception:
            redirect('./new',
                     cat_group=cat_group,
                     code=code,
                     label=label,
                     css=kw)
        else:
            redirect('./new', cat_group=cat_group)

    # noinspection PyMethodMayBeStatic
    def insert_order_cat(self, cat_group, code, label, kw):
        try:
            accessor = OrderCatAccessor()
            accessor.insert_order_cat(cat_name=None,  # use 'code' instead
                                      cat_group=cat_group,
                                      code=code,
                                      label=label,
                                      css_def=None,  # use 'css' instead
                                      css=kw)
        except sqlalchemy.exc.IntegrityError:
            msg_fmt = _(u"Nom de la catégorie de commande en doublon ! "
                        u"Le nom « {code} » existe déjà.")
            err_msg = msg_fmt.format(code=code)
            flash(err_msg, status="error")
            raise
        else:
            msg_fmt = _(u"La catégorie de commande « {code} » a été créé "
                        u"dans la base de données avec succès.")
            flash(msg_fmt.format(code=code), status="ok")

    @validate({'cat_group': NotEmpty(),
               'code': Regex(r'^\w+$', not_empty=True),
               'label': NotEmpty(),
               'color': NotEmpty(),
               'background-color': NotEmpty()},
              error_handler=get_all)
    @expose('json')
    def create_in_place(self, cat_group, code, label, **kw):
        LOG.info("OrderCatController.create_in_place")
        # noinspection PyBroadException
        try:
            self.insert_order_cat(cat_group, code, label, kw)
        except Exception:
            redirect('./', cat_group=cat_group, code=code, label=label, **kw)
        else:
            redirect('./', cat_group=cat_group)

    # noinspection PyUnusedLocal
    @expose('json')
    def invalid_value(self, name, value, pk):
        field, uid = name.split("__")[1:]
        field_mapping = dict(cat_group=_(u"Nom du groupe"),
                             code=_(u"Code couleur"),
                             label=_(u"Libellé"),
                             css_def=_(u"Définition CSS"))
        err_fmt = u"{field} invalide\u00a0: '{{value}}'. {{error}}" if value else u"{field} vide. {{error}}"
        msg_fmt = err_fmt.format(field=field_mapping[field])
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        error = form_errors['value']
        return dict(status='error', msg=msg_fmt.format(value=value, error=error))

    # noinspection PyMethodMayBeStatic
    def edit_in_place(self, name, value):
        field, uid = name.split("__")[1:]
        accessor = OrderCatAccessor()
        uid = int(uid)
        kwargs = {field: value}
        if LOG.isEnabledFor(logging.INFO):
            msg_fmt = u"Update OrderCat #{uid}: field='{field}', value='{value}'..."
            LOG.info(msg_fmt.format(uid=uid, field=field, value=value))
        try:
            accessor.update_order_cat(uid, **kwargs)
        except sqlalchemy.exc.IntegrityError:
            assert field == "code"
            msg_fmt = _(u"Nom de catégorie en doublon ! "
                        u"Le nom « {code} » existe déjà.")
            err_msg = msg_fmt.format(code=value)
            return dict(status='error', msg=err_msg)
        return dict(status='updated', label=value)

    @validate({'name': Regex(r"cat_group__\d+", not_empty=True),
               'value': NotEmpty(),
               'pk': NotEmpty()},
              error_handler=invalid_value)
    @expose('json')
    def edit_cat_group(self, name, value, pk):
        """
        Edit the `cat_group` in place.

        Posted data are:

        - name:order_cat__cat_group__21  # uid of the first order_cat
        - value:Groupe name
        - pk:unused

        :return: dictionary with a `status` and a `label`.
        """
        LOG.info("OrderCatController.edit_cat_group: "
                 "name = {name!r}, value = {value!r}, pk = {pk!r}".format(name=name, value=value, pk=pk))
        accessor = OrderCatAccessor()
        if not pk or pk == "unused":
            # -- CASE: edit in place (editable plugin)
            uid = int(name.rsplit("__", 1)[-1])
            # -- find the order_cat list that match the given uid
            match_order_cat_uid = lambda x: x[0].uid == uid
            filtered_list = filter(match_order_cat_uid, self.cat_group_index.values())
            assert len(filtered_list) == 1, b"uid: {0}, filtered_list: {1!r}".format(uid, filtered_list)
            order_cat_list = filtered_list[0]
            # -- for each order_cat: update the cat_group
            for order_cat in order_cat_list:
                accessor.update_order_cat(order_cat.uid, cat_group=value)
        else:
            # -- CASE: dropped in cat_group (droppable plugin)
            try:
                uid = int(pk)
                accessor.update_order_cat(uid, cat_group=value)
            except RecordNotFoundError as exc:
                msg_fmt = _(u"Impossible d'attribuer le groupe {value} : {exc}")
                return dict(status='error', msg=msg_fmt.format(value=value, exc=exc))
        return dict(status='updated', label=value)

    # noinspection PyUnusedLocal
    @validate({'name': Regex(r"order_cat__code__\d+", not_empty=True),
               'value': Regex(r'^\w+$', not_empty=True),
               'pk': NotEmpty()},
              error_handler=invalid_value)
    @expose('json')
    def edit_code(self, name, value, pk):
        """
        Edit the `code` in place.

        Posted data are:

        - name:order_cat__code__3
        - value:colorXYZ
        - pk:unused

        :return: dictionary with a `status` and a `label`.
        """
        uid = int(name.rsplit("__", 1)[-1])
        old_cat_name = OrderCatAccessor().get_order_cat(uid).cat_name
        result = self.edit_in_place(name, value)
        if result["status"] == "updated":
            new_cat_name = OrderCatAccessor().get_order_cat(uid).cat_name
            accessor = OrderAccessor()
            order_list = accessor.get_order_list(filter_cond=Order.project_cat == old_cat_name)
            for order in order_list:
                order.project_cat = new_cat_name
            transaction.commit()
        return result

    # noinspection PyUnusedLocal
    @validate({'name': Regex(r"order_cat__label__\d+", not_empty=True),
               'value': NotEmpty(),
               'pk': NotEmpty()},
              error_handler=invalid_value)
    @expose('json')
    def edit_label(self, name, value, pk):
        """
        Edit the `label` in place.

        Posted data are:

        - name:order_cat__label__3
        - value:Dressings
        - pk:unused

        :return: dictionary with a `status` and a `label`.
        """
        return self.edit_in_place(name, value)

    @validate({'name': Regex(r"order_cat__[bf]gcolor__\d+", not_empty=True),
               'value': NotEmpty(),
               'pk': NotEmpty()},
              error_handler=invalid_value)
    @expose('json')
    def edit_color(self, name, value, pk):
        """
        Edit the `color` in place.

        Posted data are:

        - name:order_cat__bgcolor__3
        - value:background-color: #f6a9bc; color: black;
        - pk:color

        :return: dictionary with a `status` and a `label`.
        """
        accessor = OrderCatAccessor()
        kind, field, uid = name.split("__")
        order_cat = accessor.get_order_cat(uid)
        css = order_cat.css
        css[pk] = value
        order_cat.css = css
        return self.edit_in_place("__".join([kind, "css_def", uid]), order_cat.css_def)

    @expose('intranet.templates.pointage.order_cat.get_delete')
    def get_delete(self, uid):
        """
        Display a delete Confirmation page.

        GET /admin/order_cat/1/delete

        :param uid: UID of the order category to delete.
        """
        order_cat = OrderCatAccessor().get_order_cat(uid)
        accessor = OrderAccessor()
        order_list = accessor.get_order_list(filter_cond=Order.project_cat == order_cat.cat_name)
        return dict(order_cat=order_cat, order_list=order_list)

    @expose()
    def post_delete(self, uid):
        """
        Delete an existing order category.

        :param uid: UID of the Employee to delete.
        """
        accessor = OrderCatAccessor()
        old_order_cat = accessor.delete_order_cat(uid)
        msg_fmt = _(u"La catégorie « {code} » a été supprimé "
                    u"de la base de données avec succès.")
        flash(msg_fmt.format(code=old_order_cat.code),
              status="ok")
        return dict()

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.order_cat.get_orphans')
    def get_orphans(self, **kw):
        """
        Display the list of orphans order_cat.

        GET /admin/order_cat/get_orphans.json

        .. code-block:: json

            {
              "values": {},
              "orphans_groups": {
                "Meubles": [
                  {
                    "close_date": null,
                    "creation_date": "2014-01-15",
                    "uid": 5,
                    "order_ref": "Table pour Tomas",
                    "project_cat": "colorMEUBLES"
                  },
                  ...
                ],
                "Dressing": [...]
              },
              "cat_group_index": {
                "Absences": [
                  {
                    "cat_group": "Absences",
                    "css_def": "color: #000000; background-color: #ffffff",
                    "uid": 1,
                    "cat_name": "colorConges",
                    "label": "Conges"
                  }
                ],
                "Projets": [...],
                "Hors projet": [...]
              },
              "form_errors": {},
              "display": "normal"
            }
        """
        LOG.info("OrderCatController.get_orphans, kw = " + pformat(kw))
        self._prepare(**kw)

        # -- Find all orphans
        accessor = OrderAccessor()
        if self.order_cat_list:
            existing_names = [x.cat_name for x in self.order_cat_list]
            predicate = ~Order.project_cat.in_(existing_names)
            order_list = accessor.get_order_list(filter_cond=predicate)
        else:
            order_list = accessor.get_order_list()

        # -- Group orders by code (not cat_name)
        orphans_groups = collections.defaultdict(list)
        for order in order_list:
            code = order.project_cat[5:]  # drop "color" prefix
            orphans_groups[code].append(order)

        # -- Get errors a the previous query
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")

        return dict(display=self.display, orphans_groups=orphans_groups,
                    cat_group_index=self.cat_group_index, form_errors=form_errors, values=kw)

    @validate({'cat_group': NotEmpty(),
               'code': Regex(r'^\w+$', not_empty=True),
               'label': NotEmpty(),
               'color': NotEmpty(),
               'background-color': NotEmpty()},
              error_handler=get_orphans)
    @expose()
    def post_orphan(self, cat_group, code, label, **kw):
        LOG.info("OrderCatController.post_orphan, kw={0}".format(pformat(kw)))
        try:
            self.insert_order_cat(cat_group, code, label, kw)
        except Exception:
            redirect('./get_orphans',
                     cat_group=cat_group, code=code, label=label, kw=kw)
        else:
            redirect('./get_orphans')
