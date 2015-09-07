# -*- coding: utf-8 -*-
"""Setup the Intranet application"""
import json
import logging
import datetime

import pkg_resources
from sqlalchemy.exc import IntegrityError

from intranet import model
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.frequency import FrequencyAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.pointage.order_cat import OrderCatAccessor

LOG = logging.getLogger(__name__)


def parse_date(date_str):
    if date_str:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        return None


def bootstrap(command, conf, vars):  # @ReservedAssignment
    """Place any commands to setup intranet here"""
    package = 'intranet.websetup'

    # -- initialize the order categories
    filename = 'order_cat_list.json'
    json_path = pkg_resources.resource_filename(package, filename)  # @UndefinedVariable  @IgnorePep8
    with file(json_path, 'rb') as json_file:
        record_list = json.load(json_file)
    order_cat_accessor = OrderCatAccessor(model.DBSession)
    for record in record_list:
        try:
            del record["uid"]
            order_cat_accessor.insert_order_cat(**record)
        except IntegrityError as exc:
            LOG.warning("Already in DB: {0}".format(record))

    # -- initialize the employee list
    filename = 'employee_list.json'
    json_path = pkg_resources.resource_filename(package, filename)  # @UndefinedVariable  @IgnorePep8
    with file(json_path, 'rb') as json_file:
        record_list = json.load(json_file)
    employee_accessor = EmployeeAccessor(model.DBSession)
    for record in record_list:
        try:
            del record["uid"]
            record["entry_date"] = parse_date(record["entry_date"])
            employee_accessor.insert_employee(**record)
        except IntegrityError as exc:
            LOG.warning("Already in DB: {0}".format(record))

    week_day_accessor = WeekDayAccessor(model.DBSession)
    week_hours_accessor = WeekHoursAccessor(model.DBSession)
    day_period_accessor = DayPeriodAccessor(model.DBSession)
    hours_interval_accessor = HoursIntervalAccessor(model.DBSession)
    calendar_accessor = CalendarAccessor(model.DBSession)
    frequency_accessor = FrequencyAccessor(model.DBSession)

    week_day_accessor.setup()
    week_hours_accessor.setup()
    week_hours_list = week_hours_accessor.get_week_hours_list()
    for week_hours in week_hours_list:
        day_period_accessor.setup(week_hours.uid)
        hours_interval_accessor.setup(week_hours.uid)
        calendar_accessor.setup(week_hours.uid)
    frequency_accessor.setup()
