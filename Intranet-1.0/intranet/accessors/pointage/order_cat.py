"""
:module: intranet.accessors.order_cat
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections

from intranet.accessors import BasicAccessor
from intranet.model.pointage.order_cat import OrderCat


class OrderCatAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(OrderCatAccessor, self).__init__(record_class=OrderCat,
                                               session=session)

    def get_order_cat(self, uid):
        return super(OrderCatAccessor, self)._get_record(uid)

    def get_order_cat_groups(self):
        """
        Get the order categories groups.

        :rtype: dict[unicode, list[OrderCat]]
        :return: order categories grouped by category's group.
        """
        cat_dict = collections.OrderedDict()
        order_cat_list = self.get_order_cat_list()
        for order_cat in order_cat_list:
            if order_cat.cat_group not in cat_dict:
                cat_dict[order_cat.cat_group] = []
            cat_dict[order_cat.cat_group].append(order_cat)
        return cat_dict

    def get_order_cat_list(self, filter_cond=None, order_by_cond=None):
        return super(OrderCatAccessor, self)._get_record_list(filter_cond,
                                                              order_by_cond)

    def insert_order_cat(self, **kwargs):
        return super(OrderCatAccessor, self)._insert_record(**kwargs)

    def update_order_cat(self, uid, **kwargs):
        return super(OrderCatAccessor, self)._update_record(uid, **kwargs)

    def delete_order_cat(self, uid):
        return super(OrderCatAccessor, self)._delete_record(uid)
