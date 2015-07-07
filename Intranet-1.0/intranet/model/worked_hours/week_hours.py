# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy.schema import Column, CheckConstraint
from sqlalchemy.types import Integer, SmallInteger, String

from intranet.model import DeclarativeBase


class WeekHours(DeclarativeBase):
    """
    WeekHour management.
    """
    __tablename__ = 'WeekHours'
    __table_args__ = (CheckConstraint("position > 0", name="position_check"),)  # tuple

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    position = Column(SmallInteger, unique=True, index=True, nullable=False)  # no duplicates
    label = Column(String(length=32), unique=True, nullable=False, index=True)  # no duplicates
    description = Column(String(length=200))

    def __init__(self, position, label, description):
        """
        Hours of the week.

        Examples:

        .. code-block::

            WeekHour(1, u"Open hours", u"Open hours of the company")
            WeekHour(2, u"Open hours (summer)", u"Open hours of the company in summer")

        :type position: int
        :param position: Relative position.
        :type label: unicode
        :param label: Display name of the day => used in selection.
        :type description: unicode
        :param description: Description of the day => used in tooltip.
        """
        self.position = position
        self.label = label
        self.description = description

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.position!r}), "
                    "{self.label!r}, "
                    "{self.description!r}")
        return repr_fmt.format(self=self)

    def __lt__(self, other):
        return self.position < other.position

    def __le__(self, other):
        return self.position <= other.position

    def __gt__(self, other):
        return self.position > other.position

    def __ge__(self, other):
        return self.position >= other.position
