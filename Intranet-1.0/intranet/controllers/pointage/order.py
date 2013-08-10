"""
:module: intranet.controllers.pointage.order
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from formencode.validators import NotEmpty, DateConverter
from intranet.model import DBSession
from intranet.model.pointage.order import Order
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate
import collections
import datetime
import logging
#from tg.flash import flash

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
        order_cat_list = DBSession.query(Order).all()
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
        """
        order_list = (DBSession.query(Order)
                      .order_by(Order.order_ref)
                      .all())
        return dict(order_list=order_list)

    @expose('json')
    @with_trailing_slash
    @expose('intranet.templates.pointage.order.get_one')
    def get_one(self, uid):
        """
        Display one record.

        GET /pointage/order/1

        :param uid: UID of the order to display.
        """
        order = DBSession.query(Order).get(uid)
        return dict(order=order, order_phase_list=order.order_phase_list)

    @expose('json')
    @with_trailing_slash
    @expose('intranet.templates.pointage.order.get_all')
    def get_all(self):
        """
        Display all records in a resource.

        GET /pointage/order/
        """
        order_list = (DBSession.query(Order)
                      .order_by(Order.order_ref)
                      .all())
        return dict(order_list=order_list)

    @expose('json')
    @with_trailing_slash
    @expose('intranet.templates.pointage.order.get_all')
    def search(self, keyword):
        """
        Search a list of orders.

        GET /pointage/order/?keyword=<keyword>

        :param keyword: order reference's keyword
        """
        predicat = Order.order_ref.like('%' + keyword + '%')
        order_list = (DBSession.query(Order)
                      .filter(predicat)
                      .order_by(Order.order_ref)
                      .all())
        return dict(order_list=order_list)

    @expose('intranet.templates.pointage.order.new')
    def new(self, **kw):
        """
        Display a page to prompt the User for resource creation:

        GET /pointage/order/new
        """
        cat_dict = self._get_cat_dict()
        return dict(values=kw, cat_dict=cat_dict)

    @expose('intranet.templates.pointage.order.edit')
    def edit(self, uid, **kw):
        """
        Display a page to prompt the User for resource modification.

        GET /pointage/order/1/edit

        :param uid: UID of the Order to edit
        """
        order = DBSession.query(Order).get(uid)
        creation_date = order.creation_date.strftime("%Y-%m-%d")
        close_date = (None if order.close_date is None
                      else order.close_date.strftime("%Y-%m-%d"))
        values = dict(order_ref=order.order_ref,
                      project_cat=order.project_cat,
                      creation_date=creation_date,
                      close_date=close_date)
        values.update(kw)
        cat_dict = self._get_cat_dict()
        return dict(values=values, cat_dict=cat_dict)

    @validate({'order_ref': NotEmpty,
               'project_cat': NotEmpty,
               'creation_date': DateConverter(not_empty=True),
               'close_date': DateConverter(not_empty=False)},
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
        creation_date = datetime.datetime.strptime(creation_date, "%Y-%m-%d")
        close_date = (None if close_date is None
                      else datetime.datetime.strptime(close_date, "%Y-%m-%d"))
        order = Order(order_ref, project_cat, creation_date, close_date)
        DBSession.add(order)
        redirect('./')

    @validate({'order_ref': NotEmpty,
               'project_cat': NotEmpty,
               'creation_date': DateConverter(not_empty=True),
               'close_date': DateConverter(not_empty=False)},
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
        order = DBSession.query(Order).get(uid)
        order.order_ref = order_ref
        order.project_cat = project_cat
        order.creation_date = creation_date
        order.close_date = close_date
        DBSession.flush()
        redirect('../')

    @expose()
    def post_delete(self, uid, **kw):
        """
        Delete an existing record.

        POST /pointage/order/1?_method=DELETE
        DELETE /pointage/order/1

        :param uid: UID of the Order to delete.
        """
        DBSession.delete(DBSession.query(Order).get(uid))
        redirect('../')

    @expose('intranet.templates.pointage.order.get_delete')
    def get_delete(self, uid):
        """
        Display a delete Confirmation page.

        GET /pointage/order/1/delete

        :param uid: UID of the Order to delete.
        """
        order = DBSession.query(Order).get(uid)
        return dict(order=order)
