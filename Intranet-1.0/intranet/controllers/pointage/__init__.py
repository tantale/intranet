# -*- coding: utf-8 -*-
"""
:package: intranet.controllers.pointage
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.controllers.pointage.employee import EmployeeController
from intranet.controllers.pointage.order import OrderController
from intranet.controllers.pointage.order_cat import OrderCatController
from intranet.controllers.pointage.order_phase import OrderPhaseController
from intranet.controllers.pointage.trcal import CalendarController
from intranet.lib.base import BaseController
import tg


main_menu = dict(title=u"Gestion des pointages",
                 item_list=[dict(id='toolbar_calendar',
                                 href=tg.url('/pointage/trcal/index'),
                                 title=u"Gestion des pointages des opérations",
                                 content=u"Calendrier")])


class PointageControoler(BaseController):
    """
    Root controller for Pointage
    """

    order_cat = OrderCatController()
    order_phase = OrderPhaseController()
    trcal = CalendarController(main_menu)  # Time Recording Calendar
