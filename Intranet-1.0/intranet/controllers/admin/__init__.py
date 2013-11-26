# -*- coding: utf-8 -*-
"""
:package: intranet.controllers.admin
:date: 2013-10-08
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.controllers.pointage.chart import ChartController
from intranet.controllers.pointage.employee import EmployeeController
from intranet.controllers.pointage.order import OrderController
from intranet.controllers.pointage.order_cat import OrderCatController
from intranet.controllers.pointage.order_phase import OrderPhaseController
from intranet.controllers.pointage.trcal import CalendarController
from intranet.lib.base import BaseController

import tg


main_menu = dict(title=u"Administration",
                 item_list=[dict(id='toolbar_employee',
                                 href=tg.url('/admin/employee/index.html'),
                                 title=u"Gestion des employés",
                                 content=u"Employés"),
                            dict(id='toolbar_order',
                                 href=tg.url('/admin/order/index.html'),
                                 title=u"Gestion des commandes et des phases",
                                 content=u"Commandes"),
                            dict(id='toolbar_calendar',
                                 href=tg.url('/admin/trcal/index.html'),
                                 title=u"Gestion des pointages des opérations",
                                 content=u"Calendrier")])


class AdminController(BaseController):
    """
    Root controller for Pointage
    """

    employee = EmployeeController(main_menu)
    order = OrderController(main_menu)
    order_cat = OrderCatController()
    order_phase = OrderPhaseController()
    trcal = CalendarController(main_menu)  # Time Recording Calendar
    chart = ChartController()
