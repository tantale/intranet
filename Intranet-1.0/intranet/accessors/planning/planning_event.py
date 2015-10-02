# -*- coding: utf-8 -*-
import sqlalchemy.exc
import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.model.planning.planning_event import PlanningEvent
from intranet.accessors.planning.calendar import CalendarAccessor

try:
    _("")
except TypeError:
    _ = lambda x: x


class PlanningEventAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(PlanningEventAccessor, self).__init__(PlanningEvent, session=session)
        self.calendar_accessor = CalendarAccessor(session)

    def setup(self):
        try:
            with transaction.manager:
                self.session.add_all([])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()  # abort() is required here, why?...

    def get_calendar(self, calendar_uid):
        return self.calendar_accessor.get_calendar(calendar_uid)

    def delete_planning_event(self, uid):
        """
        Delete the planning_event.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: PlanningEvent
        :return: The old PlanningEvent.
        """
        return super(PlanningEventAccessor, self)._delete_record(uid)

    def get_planning_event(self, uid):
        """
        Get a planning_event given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: PlanningEvent
        :return: The PlanningEvent.
        """
        return super(PlanningEventAccessor, self)._get_record(uid)

    def insert_planning_event(self, calendar_uid,
                              label, description, event_start, event_end, editable=True, all_day=False,
                              location=None, private=False):
        """
        Create and insert a new PlanningEvent.

        :type calendar_uid: int
        :param calendar_uid: UID of the calendar (parent).
        :type label: unicode
        :param label: Display name of the event in the calendar grid.
        :type description: unicode or None
        :param description: Description of the event.
        :type event_start: datetime.datetime
        :param event_start: The date/time an event begins.
        :type event_end: datetime.datetime
        :param event_end: The date/time an event ends (exclusive).
        :type editable: bool
        :param editable: Determine if the events can be dragged and resized.
        :type all_day: bool
        :param all_day: Whether an event occurs at a specific time-of-day.
        :type location: unicode
        :param location: location/address of the event (if any).
        :type private: bool
        :param private: is the event private? Default is public (``False``).
        :rtype: PlanningEvent
        :return: The new PlanningEvent.
        """
        with transaction.manager:
            planning_event = PlanningEvent(label, description, event_start, event_end,
                                           editable=editable, all_day=all_day,
                                           location=location, private=private)
            planning_event.calendar_uid = calendar_uid
            self.session.add(planning_event)

    def get_planning_event_list(self, filter_cond=None, order_by_cond=None):
        """
        Search the records matching the given *filter* and sorted according to the given *order-by* condition.

        :param filter_cond: Matching predicate, can be a list of predicates.
        :param order_by_cond: Order-by condition, can be a list of conditions.
        :rtype: list[PlanningEvent]
        :return: Ordered list of PlanningEvent instances.
        """
        return super(PlanningEventAccessor, self)._get_record_list(filter_cond, order_by_cond)

    def update_planning_event(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :param kwargs: keywords arguments: "label", "description", "event_start", "event_end", "editable", "all_day".
        :rtype: PlanningEvent
        :return: The updated PlanningEvent.
        """
        return super(PlanningEventAccessor, self)._update_record(uid, **kwargs)

    def increase_duration(self, uid, end_timedelta):
        """
        Event has changed in duration.

        :param uid:
        :param end_timedelta:
        """
        with transaction.manager:
            event = self._get_record(uid)
            event.event_end += end_timedelta

    def move_datetime(self, uid, timedelta):
        """
        Event has moved to a different day/time.

        :param uid:
        :param timedelta:
        """
        with transaction.manager:
            record = self._get_record(uid)
            record.event_start += timedelta
            record.event_end += timedelta
