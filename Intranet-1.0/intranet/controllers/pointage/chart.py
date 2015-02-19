# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.chart
:date: 2013-10-19
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections
import logging

from tg.i18n import ugettext as _
from tg.controllers.restcontroller import RestController
from tg.decorators import expose, without_trailing_slash

from intranet.accessors.order import OrderAccessor


LOG = logging.getLogger(__name__)


class ChartController(RestController):
    """
    The 'chart' controller
    """
    MISSING_ORDER_CAT_LABEL = _(u"(sans catégorie)")

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
                    order_cat_label=cat_label_dict.get(order.project_cat, self.MISSING_ORDER_CAT_LABEL),
                    statistics=statistics)
