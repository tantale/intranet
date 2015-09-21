# -*- coding: utf-8 -*-
import json
import logging

from tg import expose
from tg.controllers import RestController

from tg.decorators import with_trailing_slash

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.planning_event import PlanningEventAccessor
from intranet.controllers.session_obj.calendar_selection import CalendarSelectionController
from intranet.model.planning.calendar import Calendar

LOG = logging.getLogger(__name__)


class PlanningEventController(RestController):
    def _before(self, *args, **kw):
        self.accessor = PlanningEventAccessor()
        self.calendar_accessor = CalendarAccessor()
        url = kw["url"]  # /admin/planning/sources/1/events'
        parts = url.split("/")
        self.uid = int(parts[parts.index("sources") + 1])

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose()
    def get_all(self, start, end, **kwargs):
        calendar = self.calendar_accessor.get_calendar(self.uid)
        result = [event.event_obj() for event in calendar.planning_event_list]
        return json.dumps(result)


class EventSourceController(RestController):
    calendar_selections = CalendarSelectionController("planning")
    events = PlanningEventController()

    def _before(self, *args, **kw):
        self.accessor = CalendarAccessor()

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('intranet.templates.planning.event_source')
    def get_all(self):
        # -- find all and filter
        selections = self.calendar_selections.get_all()["selections"]
        calendar_list = self.accessor.get_calendar_list(Calendar.uid.in_(selections))
        event_source_list = [calendar.event_source_obj() for calendar in calendar_list]
        for event_source in event_source_list:
            event_source["url"] = "./sources/{id}/events".format(id=event_source["id"])
        return dict(eventSources=json.dumps(event_source_list, indent=True))

    @expose()
    def get_one(self, uid):
        return dict(uid=uid)
