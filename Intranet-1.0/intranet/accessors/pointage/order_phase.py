"""
:module: intranet.accessors.order_phase
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import transaction

from intranet.accessors import BasicAccessor, LOG
from intranet.accessors.pointage.order import OrderAccessor
from intranet.model.pointage.order_phase import OrderPhase


class OrderPhaseAccessor(BasicAccessor):

    def __init__(self, session=None):
        super(OrderPhaseAccessor, self).__init__(record_class=OrderPhase,
                                                 session=session)
        self.order_accessor = OrderAccessor(session)

    def get_order(self, order_uid):
        LOG.debug("get_order: {order_uid!r}".format(order_uid=order_uid))
        return self.order_accessor.get_order(order_uid)

    def get_order_phase(self, uid):
        LOG.debug("get_order_phase: {uid!r}".format(uid=uid))
        return super(OrderPhaseAccessor, self)._get_record(uid)

    def get_order_phase_list(self, filter_cond=None, order_by_cond=None):
        LOG.debug("get_order_phase_list")
        return super(OrderPhaseAccessor, self)._get_record_list(filter_cond,
                                                          order_by_cond)

    def insert_order_phase(self, order_uid, **kwargs):
        LOG.debug("insert_order_phase: {order_uid!r}"
                  .format(order_uid=order_uid))
        order = self.get_order(order_uid)
        # -- calc the new position to place this phase at the end of the list
        position_list = [0]
        position_list.extend([phase.position
                              for phase in order.order_phase_list])
        position = max(position_list) + 1
        order_phase = OrderPhase(position, kwargs['label'])
        try:
            LOG.debug("Append order_phase: {order_phase!r}"
                      .format(order_phase=order_phase))
            order.order_phase_list.append(order_phase)
            transaction.commit()
        except:
            LOG.debug("insert_order_phase: ERROR.")
            transaction.abort()
            raise
        else:
            LOG.debug("insert_order_phase: OK.")
            return order_phase

    def update_order_phase(self, uid, **kwargs):
        LOG.debug("update_order_phase: {uid!r}".format(uid=uid))
        return super(OrderPhaseAccessor, self)._update_record(uid, **kwargs)

    def delete_order_phase(self, uid):
        LOG.debug("delete_order_phase: {uid!r}".format(uid=uid))
        return super(OrderPhaseAccessor, self)._delete_record(uid)

    def reorder(self, uid_list):
        LOG.debug("reorder: {uid_list!r}".format(uid_list=uid_list))
        try:
            filter_cond = OrderPhase.uid.in_(uid_list)
            order_phase_list = self.get_order_phase_list(filter_cond)
            order_phase_dict = {order_phase.uid: order_phase
                                for order_phase in order_phase_list}
            for position, uid in enumerate(uid_list, 1):
                order_phase_dict[uid].position = position
            transaction.commit()
        except:
            LOG.debug("reorder: ERROR.")
            transaction.abort()
            raise
        else:
            LOG.debug("reorder: OK.")
