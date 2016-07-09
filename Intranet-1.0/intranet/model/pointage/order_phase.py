# -*- coding: utf-8 -*-
"""
:module: intranet.model.pointage.order_phase
:date: 2013-08-09
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from sqlalchemy import Column, Integer, String, Float, Enum, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

from intranet.model import DeclarativeBase

STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE = "PENDING", "IN_PROGRESS", "DONE"
ALL_TASK_STATUS = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE]


class OrderPhase(DeclarativeBase):
    """A phase in an order."""
    __tablename__ = 'OrderPhase'
    __table_args__ = (CheckConstraint("position > 0", name="position_check"),
                      {'mysql_engine': 'InnoDB'})

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    order_uid = Column(Integer, ForeignKey('Order.uid',
                                           ondelete='CASCADE',
                                           onupdate='CASCADE'),
                       nullable=False, index=True)
    position = Column(Integer, nullable=False)
    label = Column(String(length=50), nullable=False)

    # -- New 'description' field for order planning (since: 2.2.0)
    description = Column(String(length=200), nullable=True)

    # -- Relationship(s)
    order = relationship('Order', back_populates="order_phase_list")
    cal_event_list = relationship('CalEvent',
                                  back_populates="order_phase",
                                  order_by="CalEvent.event_start",
                                  cascade='all,delete-orphan')

    # -- New fields/relationships for order planning (since: 2.2.0)
    estimated_duration = Column(Float, nullable=True)
    remain_duration = Column(Float, nullable=True)
    task_status = Column(Enum(*ALL_TASK_STATUS), nullable=False, default=STATUS_PENDING)

    assignation_list = relationship('Assignation',
                                    back_populates="order_phase",
                                    cascade='all,delete-orphan')

    def __init__(self, position, label, description=None):
        """
        Initialize a phase for the given order.

        :param position: the index position of the phase in it's parent order.
        :type position: int
        :type label: unicode
        :param label: the order phase label (required)
        """
        self.position = position
        self.label = label
        self.description = description
        self.estimated_duration = None
        self.remain_duration = None
        self.task_status = STATUS_PENDING

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "order.uid={self.order_uid!r}, "
                    "position={self.position!r}, "
                    "label={self.label!r}, "
                    "description={self.description!r}, "
                    "estimated_duration={self.estimated_duration!r}, "
                    "remain_duration={self.remain_duration!r}, "
                    "task_status={self.task_status!r})")
        return repr_fmt.format(self=self)

    @property
    def tracked_duration(self):
        return sum(c.event_duration for c in self.cal_event_list)

    @property
    def total_duration(self):
        if self.remain_duration:
            return self.remain_duration + self.tracked_duration
        return self.tracked_duration

    @property
    def all_status_info(self):
        return [dict(value=STATUS_PENDING,
                     label=u"Attente",
                     description=u"La tâche est estimée et en attente de planification",
                     checked=self.task_status == STATUS_PENDING),
                dict(value=STATUS_IN_PROGRESS,
                     label=u"En cours",
                     description=u"La tâche est cours de planification, "
                                 u"il est encore possible d’ajuster le reste à faire",
                     checked=self.task_status == STATUS_IN_PROGRESS),
                dict(value=STATUS_DONE,
                     label=u"Terminée",
                     description=u"La tâche est terminée.",
                     checked=self.task_status == STATUS_DONE)]

    @property
    def assigned_employees(self):
        return frozenset([assignation.employee for assignation in self.assignation_list])

    def get_unassigned_employees(self, active_employees):
        return frozenset(active_employees) - self.assigned_employees

    @property
    def plan_status_info(self):
        count = len(self.assignation_list)
        can_plan = any([assignation.plan_status_info["can_plan"] for assignation in self.assignation_list])
        if self.task_status == STATUS_DONE:
            return dict(can_plan=False,
                        label=u"Terminée",
                        description=u"La tâche ne peut pas être planifiée "
                                    u"car elle est terminée.")
        elif self.estimated_duration == 0:
            return dict(can_plan=False,
                        label=u"Non estimée",
                        description=u"La tâche ne peut pas être planifiée "
                                    u"car la durée estimée est nulle.")
        elif count == 0:
            return dict(can_plan=False,
                        label=u"Non affectée",
                        description=u"La tâche ne peut pas être planifiée "
                                    u"car personne n’est affecté.")
        elif count == 1:
            if can_plan:
                return dict(can_plan=True,
                            label=u"À planifier",
                            description=u"La tâche comporte une affectation "
                                        u"restante à planifier.")
            else:
                return dict(can_plan=False,
                            label=u"Déjà planifiée",
                            description=u"La tâche ne peut pas être planifiée "
                                        u"car l’affectation est déjà planifiée.")
        else:
            if can_plan:
                return dict(can_plan=True,
                            label=u"Partiellement planifiée",
                            description=u"La tâche comporte une (ou plusieurs) affectation(s) "
                                        u"restant à planifier.")
            else:
                return dict(can_plan=False,
                            label=u"Déjà planifiée",
                            description=u"La tâche ne peut pas être planifiée "
                                        u"car toutes les affectations sont déjà planifiées.")
