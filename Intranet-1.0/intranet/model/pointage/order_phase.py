"""
:module: intranet.model.pointage.order_phase
:date: 2013-08-09
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from sqlalchemy import Column, Integer, String, Float, Enum, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

from intranet.model import DeclarativeBase

STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE = "PENDING", "IN_PROGRESS", "DONE"
ALL_STATUS = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE]


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

    # -- Relationship(s)
    order = relationship('Order', back_populates="order_phase_list")
    cal_event_list = relationship('CalEvent',
                                  back_populates="order_phase",
                                  order_by="CalEvent.event_start",
                                  cascade='all,delete-orphan')

    # -- New fields/relationships for order planning (since: 2.2.0)
    estimated_duration = Column(Float, nullable=True)
    remain_duration = Column(Float, nullable=True)
    task_status = Column(Enum(*ALL_STATUS), nullable=False, default=STATUS_PENDING)

    assignation_list = relationship('Assignation',
                                    back_populates="order_phase",
                                    cascade='all,delete-orphan')

    def __init__(self, position, label):
        """
        Initialize a phase for the given order.

        :param position: the index position of the phase in it's parent order.
        :type position: int

        :param label: the phase's label (required)
        """
        self.position = position
        self.label = label
        self.estimated_duration = None
        self.remain_duration = None
        self.task_status = STATUS_PENDING

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "order.uid={self.order_uid!r}, "
                    "position={self.position!r}, "
                    "label={self.label!r}, "
                    "estimated_duration={self.estimated_duration!r}, "
                    "remain_duration={self.remain_duration!r}, "
                    "task_status={self.task_status!r})")
        return repr_fmt.format(self=self)

    @property
    def tracked_duration(self):
        return sum(c.event_duration for c in self.cal_event_list)

    @property
    def total_duration(self):
        if self.remain_duration is None:
            return None
        return self.remain_duration + self.tracked_duration
