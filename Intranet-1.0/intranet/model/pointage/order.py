# coding=utf-8
"""
:module: intranet.model.pointage.order
:date: 2013-08-09
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Date

from intranet.model import DeclarativeBase
from intranet.model.pointage.order_phase import STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE, OrderPhase


class Order(DeclarativeBase):
    """
    Order Management.

    .. versionadded:: 1.2.0
        - The UID is the order ID.
        - The order reference isn't anymore unique: it can't a client's name so
          we tolerate duplicates.
    """
    __tablename__ = 'Order'

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    order_ref = Column(String(length=50), unique=False, nullable=False, index=True)  # @IgnorePep8
    project_cat = Column(String(length=50), unique=False, nullable=False)
    creation_date = Column(Date, nullable=False, index=True)
    close_date = Column(Date, nullable=True, index=True)

    order_phase_list = relationship('OrderPhase',
                                    back_populates='order',
                                    order_by='OrderPhase.position',
                                    cascade='all,delete-orphan')

    def __init__(self, order_ref, project_cat, creation_date, close_date=None):
        """
        Order Management

        :param order_ref: the order's reference (unique and not null)

        :param project_cat: the project's category which determines
        its color (required)

        :param creation_date: creation date (required)
        :type creation_date: datetime.date

        :param close_date: close date, or None if it's status is in progress.
        :type close_date: datetime.date
        """
        self.order_ref = order_ref
        self.project_cat = project_cat
        self.creation_date = creation_date
        self.close_date = close_date

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.order_ref!r}, "
                    "{self.project_cat!r}, "
                    "{self.creation_date!r}, "
                    "close_date={self.close_date!r})")
        return repr_fmt.format(self=self)

    @property
    def statistics(self):
        """
        Compute the time tracking statistics.

        :rtype: collections.Counter
        :return: Time tracking statistics for each order phase.
        """
        statistics = collections.Counter()
        for order_phase in self.order_phase_list:
            key = order_phase.label
            statistics[key] = order_phase.tracked_duration
        return statistics

    @property
    def estimated_duration(self):
        estimated_durations = filter(None, [order_phase.estimated_duration for order_phase in self.order_phase_list])
        return sum(estimated_durations)

    @property
    def tracked_duration(self):
        tracked_durations = filter(None, [order_phase.tracked_duration for order_phase in self.order_phase_list])
        return sum(tracked_durations)

    @property
    def remain_duration(self):
        remain_durations = filter(None, [order_phase.remain_duration for order_phase in self.order_phase_list])
        return sum(remain_durations)

    @property
    def total_duration(self):
        total_durations = filter(None, [order_phase.total_duration for order_phase in self.order_phase_list])
        return sum(total_durations)

    @property
    def all_status_info(self):
        task_status_list = [order_phase.task_status for order_phase in self.order_phase_list]
        # noinspection PyArgumentList
        count_status = collections.Counter(task_status_list)
        if STATUS_PENDING in count_status:
            if STATUS_IN_PROGRESS in count_status or STATUS_DONE in count_status:
                task_status = STATUS_IN_PROGRESS
            else:
                task_status = STATUS_PENDING
        elif STATUS_DONE in count_status:
            if STATUS_IN_PROGRESS in count_status or STATUS_PENDING in count_status:
                task_status = STATUS_IN_PROGRESS
            else:
                task_status = STATUS_DONE
        else:
            task_status = STATUS_IN_PROGRESS
        return [dict(value=STATUS_PENDING,
                     label=u"Attente",
                     description=u"Les tâches sont estimées et en attente de planification",
                     checked=task_status == STATUS_PENDING),
                dict(value=STATUS_IN_PROGRESS,
                     label=u"En cours",
                     description=u"Les tâches sont en cours de planification, "
                                 u"il est encore possible d’ajuster le reste à faire",
                     checked=task_status == STATUS_IN_PROGRESS),
                dict(value=STATUS_DONE,
                     label=u"Terminée",
                     description=u"Les tâches sont terminées.",
                     checked=task_status == STATUS_DONE)]

    def plan_order(self, tz_delta, minutes=15, max_months=4):
        """
        Plan the Order tasks and assignations (if possible).

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
        if self.close_date:
            # -- "Planification impossible car la commande est clôturée."
            return []
        checked = next(info for info in self.all_status_info if info["checked"])
        if checked["value"] == STATUS_DONE:
            # -- "Planification impossible\xa0: " + checked["description"]
            return []

        # Sélection des tâches planifiables
        task_list = [order_phase for order_phase in self.order_phase_list
                     if order_phase.plan_status_info["can_plan"]]
        if not task_list:
            # -- "Planification impossible\xa0: aucune tâche ne peut être planifiée."
            return []

        # Il nous faut choisir une date de début de planification
        # Cette date sera la valeur minimale des dates de début
        # de toutes les affectations de la première tâche.
        # Ensuite, cette date sera mise à jour après chaque planification
        # avec la valeur maximale de la date de fin de toutes les affectations.

        min_date_utc = None
        shifts = []
        for task in task_list:
            assert isinstance(task, OrderPhase)
            task_shifts = task.plan_task(tz_delta,
                                         minutes=minutes,
                                         max_months=max_months,
                                         min_date_utc=min_date_utc)
            if task_shifts:
                start_date = min([shift[0] for shift in task_shifts])
                end_date = max([shift[1] for shift in task_shifts])
                shifts.append((start_date, end_date))
                min_date_utc = end_date + tz_delta
        return shifts
