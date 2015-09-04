# -*- coding: utf-8 -*-
from tg.controllers.restcontroller import RestController

from intranet.controllers.planning.calendar import CalendarController
from intranet.controllers.planning.week_hours import WeekHoursController


class PlanningController(RestController):
    week_hours = WeekHoursController()
    calendar = CalendarController()
