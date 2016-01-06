# -*- coding: utf-8 -*-
import collections
import logging
import pprint

from pylons.i18n import ugettext as _
from tg.controllers.restcontroller import RestController
from tg.decorators import without_trailing_slash, expose

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.controllers.planning.calendar import CalendarController
from intranet.controllers.planning.event_source import EventSourceController
from intranet.controllers.planning.week_hours import WeekHoursController
from intranet.controllers.session_obj.calendar_selection import CalendarSelectionController
from intranet.controllers.session_obj.full_calendar import FullCalendarController
from intranet.controllers.session_obj.layout import LayoutController

LOG = logging.getLogger(__name__)


class ResourcesController(RestController):
    calendar_selections = CalendarSelectionController("planning")

    def _before(self, *args, **kw):
        self.calendar_accessor = CalendarAccessor()

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('intranet.templates.planning.resources')
    def get_all(self):
        # -- find all
        calendar_list = self.calendar_accessor.get_calendar_list()

        # -- add checked flag
        selections = self.calendar_selections.get_all()["selections"]
        for calendar in calendar_list:
            calendar.checked = calendar.uid in selections

        # -- Group resources
        group_dict = collections.OrderedDict()
        group_dict[_(u"Calendrier des employés")] = filter(lambda x: x.employee, calendar_list)
        group_dict[_(u"Autres calendriers")] = filter(lambda x: not x.employee, calendar_list)

        return dict(title_msg=_(u"Calendriers"),
                    empty_msg=_(u"Aucun calendriers"),
                    group_dict=group_dict)

    @expose()
    def put(self, uid, checked):
        LOG.debug("put: uid={uid}, checked={checked}".format(uid=pprint.pformat(uid),
                                                             checked=pprint.pformat(checked)))
        self.calendar_selections.put(uid, checked)
        return dict(uid=int(uid), checked=bool(checked))


# noinspection PyAbstractClass
class PlanningController(RestController):
    week_hours = WeekHoursController()
    calendar = CalendarController()

    layout = LayoutController("planning")
    full_calendar = FullCalendarController("planning")
    resources = ResourcesController()
    sources = EventSourceController()

    def __init__(self, main_menu):
        self.main_menu = main_menu

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('intranet.templates.planning.index')
    def index(self):
        """
        Display the index page.
        """
        return dict(main_menu=self.main_menu)
