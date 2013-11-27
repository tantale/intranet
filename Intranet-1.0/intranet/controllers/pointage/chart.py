"""
:module: intranet.controllers.pointage.chart
:date: 2013-10-19
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.accessors.order import OrderAccessor
from intranet.model.pointage.order import Order
from tg.controllers.restcontroller import RestController
from tg.decorators import with_trailing_slash, expose, without_trailing_slash
import collections
import logging
import math

LOG = logging.getLogger(__name__)


class ChartController(RestController):
    """
    The 'chart' controller
    """

    @without_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.chart.get_one')
    def get_one(self, uid):
        """
        Display a chart for one order.

        GET /pointage/chart/1
        GET /pointage/chart/1.json
        GET /pointage/chart/get_one?uid=1
        GET /pointage/chart/get_one.json?uid=1

        :param uid: UID of the order to display.
        """
        accessor = OrderAccessor()
        order = accessor.get_order(uid)
        order_cat_list = accessor.get_order_cat_list()
        cat_label_dict = {order_cat.cat_name: order_cat.label
                          for order_cat in order_cat_list}

        # -- compute statistics
        statistics = collections.Counter()
        for order_phase in order.order_phase_list:
            key = (order_phase.position, order_phase.label)
            for cal_event in order_phase.cal_event_list:
                delta = cal_event.event_end - cal_event.event_start
                event_duration = delta.seconds / 3600.0
                statistics[key] += event_duration

        return dict(order=order,
                    order_cat_label=cat_label_dict[order.project_cat],
                    statistics=statistics)

    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.chart.get_all')
    def get_all(self, keyword=None, uid=None):
        """
        Display a chart for a order list: a time recording sum.

        GET /pointage/chart/
        GET /pointage/chart.json
        GET /pointage/chart/get_all
        GET /pointage/chart/get_all.json

        :param uid: Active order's UID if any
        """
        # -- filter the order list/keyword
        accessor = OrderAccessor()
        order_by_cond = Order.order_ref
        filter_cond = (Order.order_ref.like('%' + keyword + '%')
                       if keyword else None)
        order_list = accessor.get_order_list(filter_cond, order_by_cond)

        # -- active_index of the order by uid
        active_index = False
        if uid:
            uid = int(uid)
            for index, order in enumerate(order_list):
                if order.uid == uid:
                    active_index = index
                    break
        return dict(order_list=order_list, keyword=keyword,
                    active_index=active_index)
