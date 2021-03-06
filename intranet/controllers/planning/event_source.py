# -*- coding: utf-8 -*-
import json
import logging

from tg import expose
from tg.controllers import RestController
from tg.decorators import with_trailing_slash

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.controllers.planning.planning_event import PlanningEventController
from intranet.controllers.session_obj.calendar_selection import CalendarSelectionController
from intranet.model import Calendar

LOG = logging.getLogger(__name__)


# noinspection PyAbstractClass
class EventSourceController(RestController):
    events = PlanningEventController()
    calendar_selections = CalendarSelectionController("planning")

    def _before(self, *args, **kw):
        self.calendar_accessor = CalendarAccessor()

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('intranet.templates.planning.event_source')
    def get_all(self, tz_offset):
        """
        Get all event sources.

        .. versionchanged:: 2.2.0
           Add the *tz_offset* parameter.

        :param tz_offset: Time zone offset.
        """
        # -- find all and filter
        selections = self.calendar_selections.get_all()["selections"]
        if selections:
            predicate = Calendar.uid.in_(selections)
            calendar_list = self.calendar_accessor.get_calendar_list(predicate)
        else:
            # The list is empty if there is no selection.
            calendar_list = []
        event_source_list = [calendar.event_source_obj() for calendar in calendar_list]
        url_fmt = "./sources/{id}/events?tz_offset={tz_offset}"
        for event_source in event_source_list:
            event_source["url"] = url_fmt.format(id=event_source["id"], tz_offset=tz_offset)
        return dict(eventSources=json.dumps(event_source_list, indent=True))

    @expose('json')
    def get_one(self, uid, **kwargs):
        """
        Get one event source.

        .. versionchanged:: 2.2.0
           Handle the *tz_offset* parameter in *kwargs*.

        :param uid: UID of the calendar.
        """
        # .. warning:: *tz_offset* must be passed as *kwargs* (TG2 limitation).
        calendar = self.calendar_accessor.get_calendar(uid)
        event_source = calendar.event_source_obj()
        url_fmt = "./sources/{id}/events?tz_offset={tz_offset}"
        event_source["url"] = url_fmt.format(id=event_source["id"], tz_offset=kwargs['tz_offset'])
        return event_source
