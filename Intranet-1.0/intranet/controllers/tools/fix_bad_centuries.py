# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.tools.fix_bad_centuries
:date: 2014-01-26
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import datetime
from intranet.accessors.cal_event import CalEventAccessor
from intranet.accessors.employee import EmployeeAccessor
from intranet.accessors.order import OrderAccessor
from intranet.lib.base import BaseController
from intranet.model.pointage.cal_event import CalEvent
from intranet.model.pointage.employee import Employee
from intranet.model.pointage.order import Order
import logging

from pylons import url
from pylons.controllers.util import redirect
from sqlalchemy.sql.expression import or_, and_
from tg.decorators import expose, with_trailing_slash
from tg.i18n import ugettext as _
from intranet.validators.iso_date_converter import update_century


# from pylons import request, response, session, tmpl_context as c, url
# from pylons.controllers.util import abort, redirect
LOG = logging.getLogger(__name__)


def century_cond(field_start, field_end):
    """
    Construct a sqlalchemy's predicate to check if a date interval contains
    at least one date with a too small century (century < 1900).

    :param field_start: field insterval's start date

    :param field_end: field insterval's end date, or None for eternity

    :return: field_start < 1900 or field_end < 1900
    """
    boundary_century = datetime.datetime(1900, 1, 1)
    return or_(field_start < boundary_century,
               and_(field_end != None, field_end < boundary_century))


def fix_century(datetime_value):
    if datetime_value is None:
        return datetime_value
    return update_century(datetime_value, years=1)


class FixBadCenturiesController(BaseController):

    TOOL = dict(href='fix_bad_centuries.html',
                label=_(u"Diagnostique les dates trop petites"),
                title=_(u"Recherche dans les employés, les commandes et "
                        u"le calendrier de pointages les dates dont l'année "
                        u"est inférieure à 1900"))  # @IgnorePep8

    @expose()
    def default(self, *args, **kwargs):
        redirect(url(controller='/tools/fix_bad_centuries',
                     action='find_bad_centuries'))

    def get_employee_list(self):
        accessor = EmployeeAccessor()
        order_by_cond = Employee.uid
        filter_cond = century_cond(Employee.entry_date, Employee.exit_date)
        employee_list = accessor.get_employee_list(filter_cond=filter_cond,
                                                   order_by_cond=order_by_cond)
        return employee_list

    def get_order_list(self):
        accessor = OrderAccessor()
        order_by_cond = Order.uid
        filter_cond = century_cond(Order.creation_date, Order.close_date)
        order_list = accessor.get_order_list(filter_cond=filter_cond,
                                             order_by_cond=order_by_cond)
        return order_list

    def get_cal_event_list(self):
        accessor = CalEventAccessor()
        order_by_cond = CalEvent.uid
        filter_cond = century_cond(CalEvent.event_start, CalEvent.event_end)
        cal_event_list = accessor.get_cal_event_list(filter_cond=filter_cond,
                                                     order_by_cond=order_by_cond)  # @IgnorePep8
        return cal_event_list

    @with_trailing_slash
    @expose('intranet.templates.tools.find_bad_centuries')
    @expose('json')
    def index(self):
        """Display the records list with contains problematic dates."""
        employee_list = self.get_employee_list()
        order_list = self.get_order_list()
        cal_event_list = self.get_cal_event_list()
        return dict(tool=self.TOOL,
                    order_list=order_list,
                    employee_list=employee_list,
                    cal_event_list=cal_event_list)

    def fix_employee_list(self):
        employee_list = self.get_employee_list()
        record_list = [dict(uid=employee.uid,
                            entry_date=fix_century(employee.entry_date),
                            exit_date=fix_century(employee.exit_date))
                       for employee in employee_list]
        accessor = EmployeeAccessor()
        for record in record_list:
            accessor.update_employee(**record)

    def fix_order_list(self):
        order_list = self.get_order_list()
        record_list = [dict(uid=order.uid,
                            creation_date=fix_century(order.creation_date),
                            close_date=fix_century(order.close_date))
                       for order in order_list]
        accessor = OrderAccessor()
        for record in record_list:
            accessor.update_order(**record)

    def fix_cal_event_list(self):
        cal_event_list = self.get_cal_event_list()
        record_list = [dict(uid=cal_event.uid,
                            event_start=fix_century(cal_event.event_start),
                            event_end=fix_century(cal_event.event_end))
                       for cal_event in cal_event_list]
        accessor = CalEventAccessor()
        for record in record_list:
            accessor.update_cal_event(**record)

    @expose()
    def fix_bad_centuries(self):
        """Handle the front-page."""
        self.fix_employee_list()
        self.fix_order_list()
        self.fix_cal_event_list()
        redirect('/tools/fix_bad_centuries/')
