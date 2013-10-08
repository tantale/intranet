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

    def get_employee_list(self, filter_cond=None, order_by_cond=None):
        return self.employee_accessor.get_employee_list(filter_cond,
                                                        order_by_cond)

    def get_order(self, order_uid):
        return self.order_accessor.get_order(order_uid)

    def get_order_list(self, filter_cond=None, order_by_cond=None):
        return self.order_accessor.get_order_list(filter_cond, order_by_cond)

    def get_order_phase(self, order_phase_uid):
        return self.order_phase_accessor.get_order_phase(order_phase_uid)

    def get_cal_event(self, uid):
        LOG.debug("get_cal_event: {uid!r}".format(uid=uid))
        return self._get_record(uid)

    def get_cal_event_list(self, filter_cond=None, order_by_cond=None):
        LOG.debug("get_cal_event_list")
        return self._get_record_list(filter_cond, order_by_cond)

    def insert_cal_event(self, employee_uid, order_phase_uid,
                         event_start, event_end, comment):
        try:
            # NOTE: selection/insertion order is important:
            # first query the foreign objects...
            employee = self.get_employee(employee_uid)
            order_phase = self.get_order_phase(order_phase_uid)
            # ... then create a new calendar event and attach them...
            cal_event = CalEvent(event_start, event_end, comment)
            cal_event.employee = employee
            cal_event.order_phase = order_phase
            # ... and commit.
            transaction.commit()
        except:
            transaction.abort()
            raise
        else:
            return cal_event

    def update_cal_event(self, uid, **kwargs):
        LOG.debug("update_cal_event: {uid!r}"
                  .format(uid=uid))
        return self._update_record(self, uid, **kwargs)

    def delete_cal_event(self, uid):
        LOG.debug("delete_cal_event: {uid!r}"
                  .format(uid=uid))
        return self._delete_record(self, uid)
