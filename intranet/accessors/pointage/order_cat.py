"""
:module: intranet.accessors.order_cat
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections
import copy

import sqlalchemy.exc
import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor, LOG
from intranet.model.pointage.order_cat import OrderCat

try:
    _("")
except TypeError:
    def _(x):
        return x

_ORDER_CAT_LIST = [
    {
        "cat_group": _(u"Commandes client"),
        "css_def": _(u"background-color: #ea750c; color: #ffffff;"),
        "uid": 1,
        "cat_name": _(u"colorMagasin"),
        "label": _(u"Magasin")
    },
    {
        "cat_group": _(u"Commandes client"),
        "css_def": _(u"background-color: #f6a9bc; color: #000000;"),
        "uid": 2,
        "cat_name": _(u"colorBureau"),
        "label": _(u"Bureau")
    },
    {
        "cat_group": _(u"Commandes client"),
        "css_def": _(u"background-color: #37ab51; color: #ffffff;"),
        "uid": 3,
        "cat_name": _(u"colorDressing"),
        "label": _(u"Dressing")
    },
    {
        "cat_group": _(u"Commandes client"),
        "css_def": _(u"background-color: #bf0e1d; color: #ffffff;"),
        "uid": 4,
        "cat_name": _(u"colorMeuble"),
        "label": _(u"Meuble")
    },
    {
        "cat_group": _(u"Commandes client"),
        "css_def": _(u"background-color: #f7c181; color: #000000;"),
        "uid": 5,
        "cat_name": _(u"colorMenuiserie"),
        "label": _(u"Menuiserie")
    },
    {
        "cat_group": _(u"Commandes client"),
        "css_def": _(u"background-color: #009fe5; color: #ffffff;"),
        "uid": 6,
        "cat_name": _(u"colorBain"),
        "label": _(u"Salle de bain")
    },
    {
        "cat_group": _(u"Commandes client"),
        "css_def": _(u"background-color: #fcc51c; color: #000000;"),
        "uid": 7,
        "cat_name": _(u"colorCuisine"),
        "label": _(u"Cuisine")
    },
    {
        "cat_group": _(u"Projets interne"),
        "css_def": _(u"background-color: #0B610B; color: #ffffff;"),
        "uid": 8,
        "cat_name": _(u"colorRenovation"),
        "label": _(u"R\u00e9novation")
    },
    {
        "cat_group": _(u"Hors projet"),
        "css_def": _(u"background-color: #6A0888; color: #ffffff;"),
        "uid": 9,
        "cat_name": _(u"colorConges"),
        "label": _(u"Cong\u00e9s")
    },
    {
        "cat_group": _(u"Hors projet"),
        "css_def": _(u"background-color: #61380B; color: #ffffff;"),
        "uid": 10,
        "cat_name": _(u"colorNettoyage"),
        "label": _(u"Nettoyage")
    },
    {
        "cat_group": _(u"Hors projet"),
        "css_def": _(u"background-color: #8A2908; color: #ffffff;"),
        "uid": 11,
        "cat_name": _(u"colorDechargement"),
        "label": _(u"D\u00e9chargement")
    }
]


class OrderCatAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(OrderCatAccessor, self).__init__(record_class=OrderCat,
                                               session=session)

    def setup(self):
        LOG.info(u"Setup the default OrderCat...")
        record_list = copy.deepcopy(_ORDER_CAT_LIST)
        for r in record_list:
            r.pop("uid")
        try:
            with transaction.manager:
                # ISO iso_weekday: Monday is 1 and Sunday is 7
                self.session.add_all([
                    OrderCat(**record) for record in record_list
                ])
        except sqlalchemy.exc.IntegrityError as exc:
            LOG.warning(exc)
            # setup already done.
            transaction.abort()

    def get_order_cat(self, uid):
        return super(OrderCatAccessor, self)._get_record(uid)

    def get_order_cat_groups(self):
        """
        Get the order categories groups.

        :rtype: dict[unicode, list[OrderCat]]
        :return: order categories grouped by category's group.
        """
        cat_dict = collections.OrderedDict()
        order_cat_list = self.get_order_cat_list()
        for order_cat in order_cat_list:
            if order_cat.cat_group not in cat_dict:
                cat_dict[order_cat.cat_group] = []
            cat_dict[order_cat.cat_group].append(order_cat)
        return cat_dict

    def get_order_cat_list(self, filter_cond=None, order_by_cond=None):
        return super(OrderCatAccessor, self)._get_record_list(filter_cond,
                                                              order_by_cond)

    def insert_order_cat(self, **kwargs):
        return super(OrderCatAccessor, self)._insert_record(**kwargs)

    def update_order_cat(self, uid, **kwargs):
        return super(OrderCatAccessor, self)._update_record(uid, **kwargs)

    def delete_order_cat(self, uid):
        return super(OrderCatAccessor, self)._delete_record(uid)
