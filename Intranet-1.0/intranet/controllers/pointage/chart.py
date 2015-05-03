# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.chart
:date: 2013-10-19
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import logging
import collections

from tg.i18n import ugettext as _
from tg.controllers.restcontroller import RestController
from tg.decorators import expose, without_trailing_slash, with_trailing_slash

from intranet.accessors.order import OrderAccessor
from intranet.model.pointage.order import Order


LOG = logging.getLogger(__name__)


class ChartController(RestController):
    """
    The 'chart' controller
    """
    MISSING_ORDER_CAT_LABEL = _(u"(sans catégorie)")

    def __init__(self, main_menu):
        self.main_menu = main_menu

    @without_trailing_slash
    @expose('intranet.templates.pointage.chart.index')
    def index(self):
        """
        Display the index page.
        """
        return dict(main_menu=self.main_menu)

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

        return dict(order=order,
                    order_cat_label=cat_label_dict.get(order.project_cat, self.MISSING_ORDER_CAT_LABEL),
                    statistics=order.statistics)

    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.chart.get_all')
    def get_all(self, **kwargs):
        """
        Display a chart for one order.

        GET /pointage/chart/
        GET /pointage/chart.json
        GET /pointage/chart/get_all
        GET /pointage/chart/get_all.json
        """
        # ADD: New feature: "time tracking statistics"
        # TODO: handle form parameters => filters
        # Prendre en charge les paramètres du formulaire pour filtrer l'affichage
        accessor = OrderAccessor()
        rows = []
        statistics = collections.Counter()
        for order in accessor.get_order_list(Order.project_cat == "colorMeuble", Order.creation_date):
            statistics.update(order.statistics)
            rows.append(order)

        headers = list(sorted(statistics.keys()))
        return dict(headers=headers, rows=rows, statistics=statistics)
