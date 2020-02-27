"""
:Module: intranet.maintenance.versions.v01_01.pointage.order_phase
:Created on: 2014-05-02
:Author: Tantale Solutions <tantale.solutions@gmail.com>
"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from intranet.maintenance.versions.v01_01.model import DeclarativeBase


class OrderPhase(DeclarativeBase):
    """A phase in an order."""
    __tablename__ = 'OrderPhase'

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    order_uid = Column(Integer, ForeignKey('Order.uid',
                                           ondelete='CASCADE',
                                           onupdate='CASCADE'),
                       nullable=False, index=True)
    position = Column(Integer, nullable=False)
    label = Column(String(length=50), nullable=False)
    order = relationship('Order',
                         backref=backref('order_phase_list',
                                         order_by='OrderPhase.position',
                                         cascade='all,delete-orphan'))

    def __init__(self, position, label):
        """
        Initialize a phase for the given order.

        :param position: the index position of the phase in it's parent order.
        :type position: int

        :param label: the phase's label (required)
        """
        self.position = position
        self.label = label

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "order.uid={self.order_uid!r}, "
                    "position={self.position!r}, "
                    "label={self.label!r})")
        return repr_fmt.format(self=self)
