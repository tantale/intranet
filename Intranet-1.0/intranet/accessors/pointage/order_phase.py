"""
:module: intranet.accessors.order_phase
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import transaction

from intranet.accessors import BasicAccessor
from intranet.accessors.pointage.order import OrderAccessor
from intranet.model.pointage.order_phase import OrderPhase


class OrderPhaseAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(OrderPhaseAccessor, self).__init__(record_class=OrderPhase, session=session)
        self.order_accessor = OrderAccessor(session)

    def get_order(self, order_uid):
        return self.order_accessor.get_order(order_uid)

    def get_order_phase(self, uid):
        return super(OrderPhaseAccessor, self)._get_record(uid)

    def get_order_phase_list(self, filter_cond=None, order_by_cond=None):
        return super(OrderPhaseAccessor, self)._get_record_list(filter_cond, order_by_cond)

    def insert_order_phase(self, order_uid, **kwargs):
        with transaction.manager:
            order = self.get_order(order_uid)
            # -- calc the new position to place this phase at the end of the list
            order_phase_list = order.order_phase_list
            last_position = max(record.position for record in order_phase_list) if order_phase_list else 0
            order_phase = OrderPhase(last_position + 1, kwargs['label'])
            order.order_phase_list.append(order_phase)
        return order_phase

    def update_order_phase(self, uid, **kwargs):
        return super(OrderPhaseAccessor, self)._update_record(uid, **kwargs)

    def delete_order_phase(self, uid):
        return super(OrderPhaseAccessor, self)._delete_record(uid)
