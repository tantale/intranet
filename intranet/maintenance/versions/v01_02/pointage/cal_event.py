"""
:module: intranet.model.pointage.cal_event
:date: 2013-09-16
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Boolean

from intranet.maintenance.versions.v01_02.model import DeclarativeBase


class CalEvent(DeclarativeBase):
    """
    Calendar event.

    :see: http://arshaw.com/fullcalendar/docs/event_data/Event_Object/
    
    :since: 1.2.0

    - Add `editable` field: an event can be editable or not (read only).
    """
    __tablename__ = 'CalEvent'

    # uid -- non-standard field
    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # employee_uid -- non-standard field
    employee_uid = Column(Integer, ForeignKey('Employee.uid',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                          nullable=True, index=True)

    # order_phase_uid -- non-standard field
    order_phase_uid = Column(Integer, ForeignKey('OrderPhase.uid',
                                                 ondelete='CASCADE',
                                                 onupdate='CASCADE'),
                             nullable=True, index=True)

    # start -- The date/time an event begins.
    event_start = Column(DateTime, nullable=False, index=True)

    # end -- The date/time an event ends (exclusive).
    event_end = Column(DateTime, nullable=False, index=True)

    # comment -- non-standard field: employee's comment
    comment = Column(String(length=200), nullable=True)

    # editable -- Determine if the events can be dragged and resized.
    editable = Column(Boolean(), nullable=True, default=True)

    # -- relationships
    employee = relationship('Employee',
                            backref=backref('cal_event_list',
                                            order_by='CalEvent.event_start',
                                            cascade='all,delete-orphan'))
    order_phase = relationship('OrderPhase',
                               backref=backref('cal_event_list',
                                               order_by='CalEvent.event_start',
                                               cascade='all,delete-orphan'))  # @IgnorePep8

    def __init__(self, event_start, event_end, comment, editable=True):
        """
        Initialize an calendar's event.

        :param event_start: The date/time an event begins.
        :type event_start: datetime.datetime

        :param event_end: The date/time an event ends (exclusive).
        :type event_end: datetime.datetime

        :param comment: The employee's comment
        
        :param editable: Determine if the events can be dragged and resized.
        :type editable: bool
        """
        self.event_start = event_start
        self.event_end = event_end
        self.comment = comment
        self.editable = editable

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "employee.uid={self.employee_uid!r}, "
                    "order_phase.uid={self.order_phase_uid!r}, "
                    "event_start={self.event_start!r}, "
                    "event_end={self.event_end!r}, "
                    "comment={self.comment!r}, "
                    "editable={self.editable!r})")
        return repr_fmt.format(self=self)

    def event_obj(self):
        """
        http://arshaw.com/fullcalendar/docs/event_data/Event_Object/
        @return: Event object as a Python dictionary
        """
        dict_ = dict()
        # -- Standard fields
        dict_['id'] = ('cal_event_{uid}'.format(uid=self.uid))
        dict_['title'] = u"{ref}\u00a0: {label}".format(ref=self.order_phase.order.order_ref,  # @IgnorePep8
                                                        label=self.order_phase.label)  # @IgnorePep8
        dict_['allDay'] = False
        dict_['start'] = self.event_start.strftime('%Y-%m-%dT%H:%M:%SZ')
        dict_['end'] = self.event_end.strftime('%Y-%m-%dT%H:%M:%SZ')
        dict_['className'] = self.order_phase.order.project_cat
        # -- Non-standard Fields
        dict_['employee_name'] = self.employee.employee_name
        dict_['order_ref'] = self.order_phase.order.order_ref
        dict_['order_phase_label'] = self.order_phase.label
        dict_['comment'] = self.comment
        dict_['editable'] = self.editable
        return dict_
