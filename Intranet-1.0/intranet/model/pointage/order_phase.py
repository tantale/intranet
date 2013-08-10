"""
:module: intranet.model.pointage.order_phase
:date: 2013-08-09
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.model import DeclarativeBase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey


class OrderPhase(DeclarativeBase):
    """A phase in an order."""
    __tablename__ = 'OrderPhase'

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    order_uid = Column(Integer, ForeignKey('Order.uid',
                                           ondelete='CASCADE',
                                           onupdate='CASCADE'),
                       nullable=False, index=True)
    position = Column(Integer, nullable=False)
    label = Column(Text, nullable=False)
    order = relationship("Order", backref=backref('order_phase_list',
                                                  order_by=position,
                                                  cascade='all,delete-orphan'))

    def __init__(self, order, label):
        """
        Initialize a phase for the given order.

        :param order: the order which will contains this new phase (required)
        :type order: Order

        :param label: the phase's label (required)
        """
        # -- calc the new position to place this phase at the end of the list
        position_list = [0]
        position_list.extend([phase.position
                              for phase in order.order_phase_list])
        position = max(position_list) + 1
        self.order = order
        self.position = position
        self.label = label

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "order.uid={self.order_uid!r}, "
                    "position={self.position!r}, "
                    "label={self.label!r})")
        return repr_fmt.format(self=self)
