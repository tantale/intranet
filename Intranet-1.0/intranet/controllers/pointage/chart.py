# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.chart
:date: 2013-10-19
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import logging
import collections

from sqlalchemy.sql.expression import and_, or_
from tg.i18n import ugettext as _
from tg.controllers.restcontroller import RestController

from tg.decorators import expose, without_trailing_slash, with_trailing_slash

from intranet.accessors.order import OrderAccessor
from intranet.controllers.session_obj.layout import LayoutController
from intranet.model.pointage.order import Order

LOG = logging.getLogger(__name__)


class ChartController(RestController):
    """
    The 'chart' controller
    """
    layout = LayoutController("chart")

    MISSING_ORDER_CAT_LABEL = _(u"(sans catégorie)")

    def __init__(self, main_menu):
        self.main_menu = main_menu

    def _get_cat_dict(self):
        """
        :return: order categories grouped by category's group.
        """
        cat_dict = collections.OrderedDict()
        accessor = OrderAccessor()
        order_cat_list = accessor.get_order_cat_list()
        for order_cat in order_cat_list:
            if order_cat.cat_group not in cat_dict:
                cat_dict[order_cat.cat_group] = []
            cat_dict[order_cat.cat_group].append(order_cat)
        return cat_dict

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('intranet.templates.pointage.chart.index')
    def index(self):
        """
        Display the index page.
        """
        return dict(main_menu=self.main_menu,
                    cat_dict=self._get_cat_dict(),
                    missing_order_cat_label=self.MISSING_ORDER_CAT_LABEL,
                    values=dict())

    # noinspection PyArgumentList
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

    # noinspection PyArgumentList
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

        .. versionchanged:: 1.4.0
            The statistics are filtered by keyword arguments.
        """
        LOG.info("intranet.controllers.pointage.chart.ChartController#get_all: {0!r}".format(kwargs))

        # -- Collect the criteria
        criteria = []
        uid = kwargs.get("uid")
        if uid:
            criteria.append(Order.uid == uid)
        order_ref = kwargs.get("order_ref")
        if order_ref:
            criteria.append(Order.order_ref.like('%' + order_ref + '%'))
        project_cat = kwargs.get("project_cat")
        if project_cat:
            criteria.append(Order.project_cat == project_cat)
        start_date = kwargs.get("start_date")
        if start_date:
            criteria.append(Order.creation_date >= start_date)
        end_date = kwargs.get("end_date")
        if end_date:
            criteria.append(or_(and_(Order.close_date != None, Order.close_date <= end_date),
                                and_(Order.close_date == None, Order.creation_date <= end_date)))
        closed = kwargs.get("closed")
        if closed:
            if closed == "true":
                criteria.append(Order.close_date != None)
            else:
                criteria.append(Order.close_date == None)

        accessor = OrderAccessor()
        rows = []
        statistics = collections.Counter()
        for order in accessor.get_order_list(and_(*criteria), Order.creation_date):
            statistics.update(order.statistics)
            rows.append(order)

        headers = list(sorted(statistics.keys()))
        return dict(headers=headers, rows=rows, statistics=statistics)
