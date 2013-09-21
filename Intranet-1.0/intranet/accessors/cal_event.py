"""
:module: intranet.accessors.cal_event
:date: 2013-09-19
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.accessors import BasicAccessor
from intranet.accessors.employee import EmployeeAccessor
from intranet.accessors.order import OrderAccessor
from intranet.accessors.order_phase import OrderPhaseAccessor
from intranet.model.pointage.cal_event import CalEvent
import logging
import transaction


LOG = logging.getLogger(__name__)


class CalEventAccessor(BasicAccessor):
    """
    Calendar event's accessor.
    """

    def __init__(self, session=None):
        super(CalEventAccessor, self).__init__(record_class=CalEvent,
                                               session=session)
        self.employee_accessor = EmployeeAccessor(self.session)
        self.order_accessor = OrderAccessor(self.session)
        self.order_phase_accessor = OrderPhaseAccessor(self.session)

    def get_employee(self, employee_uid):
        return self.employee_accessor.get_employee(employee_uid)

    def get_order(self, order_uid):
        return self.order_accessor.get_order(order_uid)

    def get_order_list(self, filter_cond=None, order_by_cond=None):
        return self.order_accessor.get_order_list(filter_cond, order_by_cond)

    def get_order_phase(self, order_phase_uid):
        return self.order_phase_accessor.get_order_phase(order_phase_uid)

    def get_cal_event(self, employee_uid, order_phase_uid):
        LOG.debug("get_cal_event: {employee_uid!r}, {order_phase_uid!r}"
                  .format(employee_uid=employee_uid,
                          order_phase_uid=order_phase_uid))
        return self._get_record((employee_uid, order_phase_uid))

    def get_cal_event_list(self, filter_cond=None, order_by_cond=None):
        LOG.debug("get_cal_event_list")
        return self._get_record_list(self, filter_cond, order_by_cond)

    def insert_cal_event(self, employee_uid, order_phase_uid,
                         **kwargs):
        cal_event = CalEvent(**kwargs)
        try:
            LOG.debug("insert_cal_event: {cal_event!r}"
                      .format(cal_event=cal_event))
            employee = self.get_employee(employee_uid)
            employee.cal_event_list.append(cal_event)
            order_phase = self.get_order_phase(order_phase_uid)
            order_phase.cal_event_list.append(cal_event)
            transaction.commit()
        except:
            LOG.debug("insert_cal_event: ERROR.")
            transaction.abort()
            raise
        else:
            LOG.debug("insert_cal_event: OK.")
            return order_phase

    def update_cal_event(self, employee_uid, order_phase_uid, **kwargs):
        LOG.debug("update_cal_event: {employee_uid!r}, {order_phase_uid!r}"
                  .format(employee_uid=employee_uid,
                          order_phase_uid=order_phase_uid))
        return self._update_record(self, (employee_uid, order_phase_uid),
                                   **kwargs)

    def delete_cal_event(self, employee_uid, order_phase_uid):
        LOG.debug("delete_cal_event: {employee_uid!r}, {order_phase_uid!r}"
                  .format(employee_uid=employee_uid,
                          order_phase_uid=order_phase_uid))
        return self._delete_record(self, (employee_uid, order_phase_uid))
