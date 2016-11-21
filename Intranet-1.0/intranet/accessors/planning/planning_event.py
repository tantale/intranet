# -*- coding: utf-8 -*-
import sqlalchemy.exc
import transaction
from sqlalchemy import and_
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.pointage.employee import overlap_cond
from intranet.model.planning.planning_event import PlanningEvent

try:
    _("")
except TypeError:
    def _(x):
        return x


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

    def get_event_by_dates(self, calendar_uid, event_start, event_end):
        """
        Get a planning_event given the Calendar UID, the start and end dates.

        :type calendar_uid: int
        :param calendar_uid: Calendar UID.
        :type event_start: datetime.datetime
        :param event_start: Start date/time of the event
        :type event_end: datetime.datetime
        :param event_end: End date/time of the event
        :rtype: PlanningEvent
        :return: The PlanningEvent (it is unique, there is a unique constraint).
        """
        filter_cond = and_(PlanningEvent.calendar_uid == calendar_uid,
                           PlanningEvent.event_start == event_start,
                           PlanningEvent.event_end == event_end)
        return self.session.query(self.record_class).filter(filter_cond).one()

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
        :param event_start: The UTC date/time of the event begins.
        :type event_end: datetime.datetime
        :param event_end: The UTC date/time of the event ends (exclusive).
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

        :type uid: int
        :param uid: UID of the event in the calendar (parent).
        :param kwargs: keywords arguments: "label", "description", "event_start", "event_end", "editable", "all_day".
        :rtype: PlanningEvent
        :return: The updated PlanningEvent.
        """
        return super(PlanningEventAccessor, self)._update_record(uid, **kwargs)

    def increase_duration(self, uid, end_timedelta):
        """
        Event has changed in duration.

        :type uid: int
        :param uid: UID of the event in the calendar (parent).
        :param end_timedelta:
        """
        with transaction.manager:
            event = self._get_record(uid)
            event.event_end += end_timedelta

    def move_datetime(self, uid, timedelta, all_day=False):
        """
        Event has moved to a different day/time.

        :type uid: int
        :param uid: UID of the event in the calendar (parent).
        :type timedelta: datetime.timedelta
        :param timedelta: Amount of time the event was moved by.
        :type all_day: bool
        :param all_day: Whether an event occurs at a specific time-of-day.
        """
        with transaction.manager:
            record = self._get_record(uid)
            record.event_start += timedelta
            record.event_end += timedelta
            record.all_day = all_day

    def search_planning_events(self, calendar_uid, start_date_utc, end_date_utc):
        """
        Search matching planning events.

        :type calendar_uid: int or str or unicode
        :param calendar_uid: UID of the calendar.

        :type start_date_utc: datetime.datetime
        :param start_date_utc: The UTC date/time of the event begins.

        :type end_date_utc: datetime.datetime
        :param end_date_utc: The UTC date/time of the event ends (exclusive).

        :rtype: list[intranet.model.planning.planning_event.PlanningEvent]
        :return: list of events
        """
        query = self.session.query(self.record_class)
        query = query.filter(PlanningEvent.calendar_uid == calendar_uid,
                             overlap_cond(start_date_utc, end_date_utc,
                                          PlanningEvent.event_start,
                                          PlanningEvent.event_end))
        return query.all()
