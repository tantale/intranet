"""
:module: intranet.model.pointage.order
:date: 2013-08-09
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import collections

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Date

from intranet.maintenance.versions.v02_00.model import DeclarativeBase


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

    # generated backref: order_phase_list
    # order_phase_list = relationship('OrderPhase,
    # backref='order',
    #                                 order_by='OrderPhase.position,
    #                                 cascade='all,delete-orphan')

    def __init__(self, order_ref, project_cat, creation_date, close_date=None):
        """
        Order Management

        :param order_ref: the order reference (not unique and not null)

        :param project_cat: the project category which determines
        its color (required)

        :param creation_date: creation date in local time (required)
        :type creation_date: datetime.date

        :param close_date: close date in local time, or None if it's status is in progress.
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
            for cal_event in order_phase.cal_event_list:
                statistics[key] += cal_event.event_duration
        return statistics
