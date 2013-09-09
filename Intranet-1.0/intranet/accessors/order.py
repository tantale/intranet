"""
:module: intranet.accessors.order
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.accessors import BasicAccessor
from intranet.model.pointage.order import Order
from intranet.accessors.order_cat import OrderCatAccessor


class OrderAccessor(BasicAccessor):

    def __init__(self, session=None):
        super(OrderAccessor, self).__init__(record_class=Order,
                                            session=session)
        self.order_cat_accessor = OrderCatAccessor(session)

    def get_order_cat_list(self, filter_cond=None, order_by_cond=None):
        return self.order_cat_accessor.get_order_cat_list(filter_cond,
                                                          order_by_cond)

    def get_order(self, uid):
        return super(OrderAccessor, self)._get_record(uid)

    def get_order_list(self, filter_cond=None, order_by_cond=None):
        return super(OrderAccessor, self)._get_record_list(filter_cond,
                                                          order_by_cond)

    def insert_order(self, **kwargs):
        return super(OrderAccessor, self)._insert_record(**kwargs)

    def update_order(self, uid, **kwargs):
        return super(OrderAccessor, self)._update_record(uid, **kwargs)

    def delete_order(self, uid):
        return super(OrderAccessor, self)._delete_record(uid)
