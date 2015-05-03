# -*- coding: utf-8 -*-
"""
:package: intranet.controllers.admin
:date: 2013-10-08
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.accessors.menu_item import MenuItemAccessor
from intranet.controllers.pointage.chart import ChartController
from intranet.controllers.pointage.employee import EmployeeController
from intranet.controllers.pointage.order import OrderController
from intranet.controllers.pointage.order_cat import OrderCatController
from intranet.controllers.pointage.order_phase import OrderPhaseController
from intranet.controllers.pointage.prefs import PrefsController
from intranet.controllers.pointage.trcal import CalendarController
from intranet.lib.base import BaseController


class AdminController(BaseController):
    """
    Root controller for Pointage
    """
    menu_accessor = MenuItemAccessor()
    main_menu = menu_accessor.get_main_menu(u"Administration")

    employee = EmployeeController(main_menu)
    order = OrderController(main_menu)
    order_cat = OrderCatController()
    order_phase = OrderPhaseController()
    trcal = CalendarController(main_menu)  # Time Recording Calendar
    chart = ChartController(main_menu)
    prefs = PrefsController(main_menu)
