# -*- coding: utf-8 -*-
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor, RecordNotFoundError
from intranet.model.worked_hours.week_day import WeekDay

try:
    _("")
except TypeError:
    _ = lambda x: x


class WeekDayAccessor(BasicAccessor):
    RECORDS = dict((r.uid, r) for r in [
        WeekDay(0, _(u"Lundi")),
        WeekDay(1, _(u"Mardi")),
        WeekDay(2, _(u"Mercredi")),
        WeekDay(3, _(u"Jeudi")),
        WeekDay(4, _(u"Vendredi")),
        WeekDay(5, _(u"Samedi")),
        WeekDay(6, _(u"Dimanche"))
    ])

    def __init__(self, session=None):
        super(WeekDayAccessor, self).__init__(WeekDay, session=session)

    def get_week_day(self, uid):
        """
        Get a week_day given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: WeekDay
        :return: The WeekDay.
        """
        try:
            return self.RECORDS[uid]
        except KeyError:
            raise RecordNotFoundError(self.class_name, uid)

    def get_week_day_list(self, filter_cond=None, order_by_cond=None):
        """
        Search the records matching the given *filter* and sorted according to the given *order-by* condition.

        :param filter_cond: Matching predicate, can be a list of predicates.
        :param order_by_cond: Order-by condition, can be a list of conditions.
        :rtype: list[WeekDay]
        :return: Ordered list of WeekDay instances.
        """
        return sorted(self.RECORDS.itervalues())
