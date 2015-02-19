# -*- coding: utf-8 -*-
"""
:module: intranet.validators.iso_date_converter
:date: 2013-08-12
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import datetime

from formencode.api import FancyValidator, Invalid
from tg.i18n import ugettext as _


def update_century(datetime_value, years=1):
    """
    Update the century of a date/time when 0 <= year < 100.

    :param datetime_value:
    :type datetime_value: datetime.datetime

    :param years: number of years to add for the boundary year.
    :type years: int

    :return: datetime value fixed
    :rtype: datetime.datetime
    """
    boundary_year = datetime.date.today().year + years
    century, short_year = divmod(boundary_year, 100)
    year = datetime_value.year
    if 0 <= year <= short_year:
        year = century * 100 + year
    elif short_year < year < 100:
        year = (century - 1) * 100 + year
    elif 100 <= year < 1900:
        raise ValueError("Invalid year: {year}"
                         .format(year=datetime_value.year))
    datetime_value = datetime_value.replace(year=year)
    return datetime_value


class IsoDateConverter(FancyValidator):
    """
    Date converter for ISO formatted dates.
    """

    messages = dict(invalidDate=_(u'Date invalide : "%(value)s"'))

    def _to_python(self, value, state):
        fmt_list = ["%Y-%m-%d"]
        for fmt in fmt_list:
            try:
                datetime_value = datetime.datetime.strptime(value, fmt)
                datetime_value = update_century(datetime_value)
                return datetime_value.date()  # datetime.date
            except ValueError:
                pass
        raise Invalid(self.message('invalidDate', state, value=value),
                      value, state)

    def _from_python(self, value, state=None):
        return value.strftime("%Y-%m-%d")


class IsoDatetimeConverter(FancyValidator):
    """
    Date/time converter for ISO formatted dates.
    """

    messages = dict(invalidDate=_(u'Date/Heure invalide : "%(value)s"'))

    def _to_python(self, value, state):
        fmt_list = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"]
        for fmt in fmt_list:
            try:
                datetime_value = datetime.datetime.strptime(value, fmt)
                datetime_value = update_century(datetime_value)
                return datetime_value  # datetime.datetime
            except ValueError:
                pass
        raise Invalid(self.message('invalidDate', state, value=value),
                      value, state)

    def _from_python(self, value, state=None):
        return value.isoformat()
