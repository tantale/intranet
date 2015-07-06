# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, SmallInteger, String

from intranet.model import DeclarativeBase


class WeekHour(DeclarativeBase):
    """
    WeekHour management.
    """
    __tablename__ = 'WeekHour'

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    label = Column(String(length=32), unique=True, nullable=False, index=True)
    description = Column(String(length=200))
    position = Column(SmallInteger, nullable=False)

    def __init__(self, label, description, position):
        """
        Hours of the week.

        Examples:

        .. code-block::

            WeekHour(u"Open hours", u"Open hours of the company", 1)

        :type label: unicode
        :param label: Display name of the day => used in selection.
        :type description: unicode
        :param description: Description of the day => used in tooltip.
        :type position: int
        :param position: Relative position: quotient > 0
        """
        if position <= 0:
            msg_fmt = "Invalid position value {position}: required position > 0"
            raise ValueError(msg_fmt.format(position=position))
        self.label = label
        self.description = description
        self.position = position

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.label!r}, "
                    "{self.description!r}, "
                    "{self.position!r})")
        return repr_fmt.format(self=self)

    def __lt__(self, other):
        return self.position < other.position

    def __le__(self, other):
        return self.position <= other.position

    def __gt__(self, other):
        return self.position > other.position

    def __ge__(self, other):
        return self.position >= other.position
