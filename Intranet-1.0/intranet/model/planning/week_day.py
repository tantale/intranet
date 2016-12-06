# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy.orm import relationship
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer
from sqlalchemy.types import SmallInteger
from sqlalchemy.types import String

from intranet.model import DeclarativeBase


class WeekDay(DeclarativeBase):
    """
    WeekDay management.

    .. versionchanged:: 2.2.0
       Add the *hours_interval_list* relationship.
    """
    __tablename__ = 'WeekDay'
    # ISO iso_weekday: Monday is 1 and Sunday is 7
    __table_args__ = (CheckConstraint("1 <= iso_weekday AND iso_weekday <= 7", name="iso_weekday_check"),)

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    iso_weekday = Column(SmallInteger, unique=True, index=True, nullable=False)  # without duplicates
    label = Column(String(length=32), unique=True, nullable=False, index=True)  # without duplicates
    description = Column(String(length=200))

    hours_interval_list = relationship('HoursInterval',
                                       back_populates='week_day',
                                       cascade='all,delete-orphan')

    def __init__(self, iso_weekday, label, description=None):
        """
        The day of the week, from monday to sunday.

        Examples:

        .. code-block::

            WeekDay(1, u"Monday")
            WeekDay(2, u"Tuesday")
            WeekDay(3, u"Wednesday")
            WeekDay(4, u"Thursday")
            WeekDay(5, u"Friday")
            WeekDay(6, u"Saturday")
            WeekDay(7, u"Sunday")

        :type iso_weekday: int
        :param iso_weekday: ISO iso_weekday: Monday is 1 and Sunday is 7.
        :type label: unicode
        :param label: Display name of the day => used in selection.
        :type description: unicode
        :param description: Description of the day => used in tooltip.
        """
        self.iso_weekday = iso_weekday
        self.label = label
        self.description = description

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.iso_weekday!r}, "
                    "{self.label!r}, "
                    "{self.description!r})")
        return repr_fmt.format(self=self)
