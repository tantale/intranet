"""
:module: intranet.validators.iso_date_converter
:date: 2013-08-12
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from formencode.api import FancyValidator, Invalid
import datetime


class IsoDateConverter(FancyValidator):
    """
    Date converter for ISO formatted dates.
    """

    messages = dict(invalidDate=u'Date invalide : "%(value)s"')

    def _to_python(self, value, state):
        try:
            datetime_value = datetime.datetime.strptime(value, "%Y-%m-%d")
            return datetime_value.date()
        except ValueError:
            raise Invalid(self.message('invalidDate', state, value=value),
                          value, state)

    def _from_python(self, value, state=None):
        return datetime.datetime.strftime("%Y-%m-%d")
