# -*- coding: utf-8 -*-
"""
:module: intranet.accessors.order
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections
import datetime

import sqlalchemy.exc
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

    def get_order_by_ref(self, order_ref):
        """
        Get the first Order of a given reference.

        Useful for testing but not for production because the reference may not be unique.

        .. versionadded:: 2.2.0

        :type order_ref: str | unicode
        :param order_ref: Order reference (label).
        :rtype: Order
        :return: The found Order.
        :raises: sqlalchemy.orm.exc.NoResultFound
        :raises: sqlalchemy.orm.exc.MultipleResultsFound
        """
        return self.session.query(Order).filter(Order.order_ref == order_ref).one()

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
                                           label=phase.label,
                                           description=phase.description)
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

    def update_order(self, uid, order_ref, project_cat, creation_date, close_date=None):
        """
        Update the attributes of the Order.

        .. versionchanged:: 2.2.0
           * If the Order is closed, all tasks are marked "DONE",
           * If the Order is reopened, all tasks are marked "IN_PROGRESS"
             if tracked duration is positive else "PENDING".

        :type uid: str | int
        :param uid: Order UID
        :type order_ref: unicode
        :param order_ref: the order reference (not unique and not null)
        :type project_cat: unicode
        :param project_cat: the project category which determines its color (required)
        :type creation_date: datetime.date
        :param creation_date: creation date in local time (required)
        :type close_date: datetime.date
        :param close_date: close date in local time, or None if it's status is in progress.
        """
        with transaction.manager:
            order = self._get_record(uid)
            old_close_date = order.close_date
            assert isinstance(order, Order)
            order.order_ref = order_ref
            order.project_cat = project_cat
            order.creation_date = creation_date
            order.close_date = close_date
            if not old_close_date and close_date:
                order.close_task()
            elif old_close_date and not close_date:
                order.reopen_task()

    def delete_order(self, uid):
        return super(OrderAccessor, self)._delete_record(uid)

    def estimate_duration(self, order_uid, order_phase_uid=None, closed=True, max_count=64):
        """
        Estimate the duration of ALL tasks of a given order.

        .. versionadded:: 2.2.0

        :type order_uid: int | unicode
        :param order_uid: UID of the order.
        :type order_phase_uid: int | unicode | None
        :param order_phase_uid: UID of the order phase to update, or ``None`` to update all phases.
        :type closed: bool | None
        :param closed: 3-state close flag:

            * ``True``:  select only closed orders,
            * ``False``: select only opened orders,
            * ``None``:  select all orders (opened and closed).

        :type max_count: int
        :param max_count: Limit the number of orders used for statistics.
        """
        order_uid = int(order_uid) if order_uid else None
        order_phase_uid = int(order_phase_uid) if order_phase_uid else None
        with transaction.manager:
            curr_order = self.get_order(order_uid)
            criterion = [Order.project_cat == curr_order.project_cat]
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
                for order_phase in curr_order.order_phase_list:
                    tracked_time = statistics.get(order_phase.label, 0)
                    if tracked_time:
                        tracked_time_by_label[order_phase].append(tracked_time)

            for order_phase, tracked_times in tracked_time_by_label.iteritems():
                if order_phase_uid is None or order_phase.uid == order_phase_uid:
                    pertinents = gauss_filter(tracked_times) if tracked_times else []
                    mean_time = int(mean(pertinents) * 4) / 4.0 if pertinents else 0
                    order_phase.estimated_duration = mean_time or None
                    order_phase.remain_duration = max(0, order_phase.estimated_duration - order_phase.tracked_duration)
                    order_phase.reopen_task()

    def plan_order(self, order_uid, tz_delta, minutes=15, max_months=4):
        """
        Plan the Order tasks and assignations (if possible).

        .. versionadded:: 2.2.0

        :type order_uid: int | unicode
        :param order_uid: UID of the order.
        :type tz_delta: datetime.timedelta
        :param tz_delta: time-zone delta from UTC (tz_delta = utc_date - local_date).
        :type minutes: int
        :param minutes: Minimal number of assignable duration.
        :type max_months: int
        :param max_months: Maximal number of months.
        :rtype: list[(datetime.datetime, datetime.datetime)]
        :return: List of hours shifts or empty list if not assignable.
            The couple (event_start, event_end) use date/time (local time).
        """
        try:
            with transaction.manager:
                order = self.get_order(order_uid)
                return order.plan_order(tz_delta, minutes, max_months)
        except sqlalchemy.exc.IntegrityError:
            transaction.abort()
            raise
