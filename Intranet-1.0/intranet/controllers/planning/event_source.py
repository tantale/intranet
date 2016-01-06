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
    def get_all(self):
        # -- find all and filter
        selections = self.calendar_selections.get_all()["selections"]
        predicate = Calendar.uid.in_(selections)
        calendar_list = self.calendar_accessor.get_calendar_list(predicate)
        event_source_list = [calendar.event_source_obj() for calendar in calendar_list]
        for event_source in event_source_list:
            event_source["url"] = "./sources/{id}/events".format(id=event_source["id"])
        return dict(eventSources=json.dumps(event_source_list, indent=True))

    @expose('json')
    def get_one(self, uid):
        calendar = self.calendar_accessor.get_calendar(uid)
        event_source = calendar.event_source_obj()
        event_source["url"] = "./sources/{id}/events".format(id=event_source["id"])
        return event_source
