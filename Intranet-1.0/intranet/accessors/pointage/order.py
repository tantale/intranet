# -*- coding: utf-8 -*-
"""
:module: intranet.accessors.order
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections
import datetime

import transaction

from intranet.accessors import BasicAccessor
from intranet.accessors.pointage.order_cat import OrderCatAccessor
from intranet.accessors.statistics import gauss_filter, mean
from intranet.model.pointage.order import Order
from intranet.model.pointage.order_phase import OrderPhase


class OrderAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(OrderAccessor, self).__init__(record_class=Order,
                                            session=session)
        self.order_cat_accessor = OrderCatAccessor(session)

    def get_order_cat_list(self, filter_cond=None, order_by_cond=None):
        return self.order_cat_accessor.get_order_cat_list(filter_cond,
                                                          order_by_cond)

    def get_order(self, uid):
        return super(OrderAccessor, self)._get_record(uid)

    def get_order_list(self, filter_cond=None, order_by_cond=None):
        return super(OrderAccessor, self)._get_record_list(filter_cond,
                                                           order_by_cond)

    def duplicate(self, uid):
        # -- search a new order reference
        actual_order = self.get_order(uid)
        new_order_ref = (u"Copie de {order_ref}"
                         .format(order_ref=actual_order.order_ref))
        order_list = self.get_order_list(Order.order_ref == new_order_ref)
        counter = 1
        while order_list:
            counter += 1
            new_order_ref = (u"Copie de {order_ref} ({counter})"
                             .format(order_ref=actual_order.order_ref,
                                     counter=counter))
            order_list = self.get_order_list(Order.order_ref == new_order_ref)

        # -- create a clone
        new_creation_date = datetime.date.today()
        new_project_cat = actual_order.project_cat
        new_order = Order(order_ref=new_order_ref,
                          project_cat=new_project_cat,
                          creation_date=new_creation_date)
        new_order_phase_list = [OrderPhase(position=phase.position,
                                           label=phase.label)
                                for phase in actual_order.order_phase_list]
        new_order.order_phase_list.extend(new_order_phase_list)
        with transaction.manager:
            self.session.add(new_order)
        return dict(order_ref=new_order_ref,
                    project_cat=new_project_cat,
                    creation_date=new_creation_date,
                    close_date=None)

    def insert_order(self, **kwargs):
        order = self.record_class(**kwargs)
        # todo: Put default phases in OrderCatPhases (parameter)
        phases = [u"Commercialisation / Étude",
                  u"Fabrication",
                  u"Finition",
                  u"Livraison / Pose",
                  u"Divers"]
        order_phase_list = [OrderPhase(position=position,
                                       label=label)
                            for position, label in enumerate(phases, 1)]
        order.order_phase_list.extend(order_phase_list)
        with transaction.manager:
            self.session.add(order)
        return kwargs

    def update_order(self, uid, **kwargs):
        return super(OrderAccessor, self)._update_record(uid, **kwargs)

    def delete_order(self, uid):
        return super(OrderAccessor, self)._delete_record(uid)

    def estimate_duration(self, uid, closed=True, max_count=64):
        new_order = self.get_order(uid)
        criterion = [Order.project_cat == new_order.project_cat]
        if closed is True:
            # noinspection PyComparisonWithNone
            criterion.append(Order.close_date != None)
        elif closed is False:
            # noinspection PyComparisonWithNone
            criterion.append(Order.close_date == None)
        # in reverse order => to use LIMIT
        order_by_cond = Order.creation_date.desc()
        order_list = self.session.query(Order).filter(*criterion).order_by(order_by_cond).limit(max_count).all()

        tracked_time_by_label = collections.defaultdict(list)
        for order in order_list:
            statistics = order.statistics
            for order_phase in new_order.order_phase_list:
                tracked_time = statistics.get(order_phase.label, 0)
                if tracked_time:
                    tracked_time_by_label[order_phase].append(tracked_time)

        with transaction.manager:
            for order_phase, tracked_times in tracked_time_by_label.iteritems():
                pertinents = gauss_filter(tracked_times) if tracked_times else []
                mean_time = int(mean(pertinents) * 4) / 4.0 if pertinents else 0
                order_phase.estimated_duration = mean_time or None
