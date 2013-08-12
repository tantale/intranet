"""
:package: intranet.controllers.pointage
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.controllers.pointage.employee import EmployeeController
from intranet.controllers.pointage.order import OrderController
from intranet.controllers.pointage.order_cat import OrderCatController
from intranet.lib.base import BaseController


class PointageControoler(BaseController):
    """
    Root controller for Pointage
    """

    employee = EmployeeController()
    order = OrderController()
    order_cat = OrderCatController()
