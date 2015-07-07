# -*- coding: utf-8 -*-
"""
:package: intranet.controllers.pointage
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.accessors.pointage.menu_item import MenuItemAccessor
from intranet.controllers.pointage.chart import ChartController
from intranet.controllers.pointage.employee import EmployeeController
from intranet.controllers.pointage.order import OrderController
from intranet.controllers.pointage.order_cat import OrderCatController
from intranet.controllers.pointage.order_phase import OrderPhaseController
from intranet.controllers.pointage.trcal import CalendarController
from intranet.lib.base import BaseController


class PointageControoler(BaseController):
    """
    Root controller for Pointage
    """
    menu_accessor = MenuItemAccessor()
    main_menu = menu_accessor.get_main_menu(u"Gestion des pointages")

    order_cat = OrderCatController()
    order_phase = OrderPhaseController()
    trcal = CalendarController(main_menu)  # Time Recording Calendar
    chart = ChartController(main_menu)
