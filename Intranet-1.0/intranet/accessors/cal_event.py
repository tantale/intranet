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
import datetime
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

    def increase_duration(self, uid, end_timedelta):
        """
        Event has changed in duration.

        :param uid:
        :param end_timedelta:
        """
        LOG.debug("move_datetime: {uid!r}".format(uid=uid))
        record = self._get_record(uid)
        try:
            LOG.debug("before: [{record.event_start}, {record.event_end}]"
                      .format(record=record))
            record.event_end += end_timedelta
            LOG.debug("after:  [{record.event_start}, {record.event_end}]"
                      .format(record=record))
            transaction.commit()
        except:
            transaction.abort()
            raise

    def divide_event(self, uid, days):
        """
        Divide the event and insert a new event for each extra day.

        :param uid: clendar event's UID.
        :type uid: int

        :param days: number of days
        :type days: int
        """
        event = self._get_record(uid)

        def divide(day):
            timedelta = datetime.timedelta(days=day + 1)
            new_event_start = event.event_start + timedelta
            new_event_end = event.event_end + timedelta
            new_event = CalEvent(new_event_start, new_event_end, event.comment)
            new_event.employee_uid = event.employee_uid
            new_event.order_phase = event.order_phase
            return new_event

        try:
            event_list = map(divide, xrange(days))
            self.session.add_all(event_list)
            transaction.commit()
        except:
            transaction.abort()
            raise

    def move_datetime(self, uid, timedelta):
        """
        Event has moved to a different day/time.

        :param uid:
        :param timedelta:
        """
        LOG.debug("move_datetime: {uid!r}".format(uid=uid))
        record = self._get_record(uid)
        try:
            LOG.debug("before: [{record.event_start}, {record.event_end}]"
                      .format(record=record))
            record.event_start += timedelta
            record.event_end += timedelta
            LOG.debug("after:  [{record.event_start}, {record.event_end}]"
                      .format(record=record))
            transaction.commit()
        except:
            transaction.abort()
            raise
