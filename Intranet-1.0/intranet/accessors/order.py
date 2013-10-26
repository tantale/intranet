# -*- coding: utf-8 -*-
"""
:module: intranet.accessors.order
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.accessors import BasicAccessor, DuplicateFoundError
from intranet.accessors.order_cat import OrderCatAccessor
from intranet.model.pointage.order import Order
from intranet.model.pointage.order_phase import OrderPhase
from sqlalchemy.exc import IntegrityError
import transaction


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
        order = self.record_class(**kwargs)
        phases = [u"Commercialisation / Étude",
                  u"Fabrication",
                  u"Finition",
                  u"Livraison / Pose",
                  u"Divers"]
        order_phase_list = [OrderPhase(position=position,
                                       label=label)
                            for position, label in enumerate(phases, 1)]
        order.order_phase_list.extend(order_phase_list)
        try:
            self.session.add(order)
            transaction.commit()
        except IntegrityError:
            transaction.abort()
            raise DuplicateFoundError(self.class_name, **kwargs)
        except:
            transaction.abort()
            raise
        else:
            return order

    def update_order(self, uid, **kwargs):
        return super(OrderAccessor, self)._update_record(uid, **kwargs)

    def delete_order(self, uid):
        return super(OrderAccessor, self)._delete_record(uid)
