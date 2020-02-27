# -*- coding: utf-8 -*-
"""Setup the Intranet application"""

from intranet import model
from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.frequency import FrequencyAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.planning_event import PlanningEventAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.pointage.order_cat import OrderCatAccessor


def bootstrap(command, conf, vars):  # @ReservedAssignment
    order_cat_accessor = OrderCatAccessor(model.DBSession)
    week_day_accessor = WeekDayAccessor(model.DBSession)
    week_hours_accessor = WeekHoursAccessor(model.DBSession)
    day_period_accessor = DayPeriodAccessor(model.DBSession)
    hours_interval_accessor = HoursIntervalAccessor(model.DBSession)
    calendar_accessor = CalendarAccessor(model.DBSession)
    frequency_accessor = FrequencyAccessor(model.DBSession)
    planning_event_accessor = PlanningEventAccessor(model.DBSession)

    order_cat_accessor.setup()
    week_day_accessor.setup()
    week_hours_accessor.setup()
    week_hours_list = week_hours_accessor.get_week_hours_list()
    for week_hours in week_hours_list:
        day_period_accessor.setup(week_hours.uid)
        hours_interval_accessor.setup(week_hours.uid)
        calendar_accessor.setup(week_hours.uid)
    frequency_accessor.setup()
    planning_event_accessor.setup()
