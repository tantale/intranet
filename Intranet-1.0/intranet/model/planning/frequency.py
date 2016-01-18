# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, UniqueConstraint, CheckConstraint
from sqlalchemy.types import Integer, String, SmallInteger

from intranet.model import DeclarativeBase


class Frequency(DeclarativeBase):
    """
    Frequency management.
    """
    __tablename__ = 'Frequency'
    __table_args__ = (UniqueConstraint('modulo', 'quotient',
                                       name="modulo_quotient_unique"),
                      CheckConstraint("quotient > 0 and 0 <= modulo and modulo < quotient",
                                      name="modulo_quotient_check"))

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    label = Column(String(length=32), unique=True, nullable=False, index=True)
    description = Column(String(length=200))
    modulo = Column(SmallInteger, nullable=False)
    quotient = Column(SmallInteger, nullable=False)

    year_period_list = relationship('YearPeriod',
                                    back_populates='frequency',
                                    cascade='all,delete-orphan')

    def __init__(self, label, description, modulo, quotient):
        """
        Year period's frequency (parity) in number of weeks.

        Examples:

        .. code-block::

            Frequency(u"aperiodic", u"all the year", 0, 1)
            Frequency(u"even", u"even weeks", 0, 2)
            Frequency(u"odd", u"odd weeks", 1, 2)

        :type label: unicode
        :param label: Display name of the frequency (no duplicate) => used in selection.
        :type description: unicode
        :param description: Description of the frequency => used in tooltip.
        :type modulo: int
        :param modulo: Modulo value of the frequency: 0 <= modulo < quotient
        :type quotient: int
        :param quotient: Quotient value of the frequency: quotient > 0
        """
        self.label = label
        self.description = description
        self.modulo = modulo
        self.quotient = quotient

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.label!r}, "
                    "{self.description!r}, "
                    "{self.modulo!r}, "
                    "{self.quotient!r})")
        return repr_fmt.format(self=self)

    def match_week(self, week):
        """
        Check is a week matches the current frequency.

        :type week: int
        :param week: The ISO 8601 week number of the current year (1 to 53).
        :rtype: bool
        :return: ``True`` if the week matches the current frequency.
        """
        return week % self.quotient == self.modulo
