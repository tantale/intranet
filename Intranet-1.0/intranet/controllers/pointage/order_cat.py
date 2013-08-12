"""
:module: intranet.controllers.pointage.order_cat
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.model import DBSession
from intranet.model.pointage.order_cat import OrderCat
from tg.controllers.restcontroller import RestController
from tg.decorators import expose, with_trailing_slash


class OrderCatController(RestController):
    """
    Order category controller
    """

    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.order_cat.get_all_css',
            content_type='text/css')
    def get_all(self):
        """
        Display all OrderCat in a resource.

        GET /pointage/order/
        """
        order_cat_list = DBSession.query(OrderCat).all()
        return dict(order_cat_list=order_cat_list)
