# -*- coding: utf-8 -*-

import sqlalchemy.exc
import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.model.planning.week_day import WeekDay

try:
    _("")
except TypeError:
    def _(x):
        return x


class WeekDayAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(WeekDayAccessor, self).__init__(WeekDay, session=session)

    def setup(self):
        try:
            with transaction.manager:
                # ISO iso_weekday: Monday is 1 and Sunday is 7
                self.session.add_all([
                    WeekDay(1, _(u"Lundi"), _(u"Le Lundi")),
                    WeekDay(2, _(u"Mardi"), _(u"Le Mardi")),
                    WeekDay(3, _(u"Mercredi"), _(u"Le Mercredi")),
                    WeekDay(4, _(u"Jeudi"), _(u"Le Jeudi")),
                    WeekDay(5, _(u"Vendredi"), _(u"Le Vendredi")),
                    WeekDay(6, _(u"Samedi"), _(u"Le Samedi")),
                    WeekDay(7, _(u"Dimanche"), _(u"Le Dimanche"))
                ])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()

    def delete_week_day(self, uid):
        """
        Delete the week_day.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: WeekDay
        :return: The old WeekDay.
        """
        return super(WeekDayAccessor, self)._delete_record(uid)

    def get_week_day(self, uid):
        """
        Get a week_day given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: WeekDay
        :return: The WeekDay.
        """
        return super(WeekDayAccessor, self)._get_record(uid)

    def get_by_label(self, label):
        return self.session.query(WeekDay).filter(WeekDay.label == label).one()

    def insert_week_day(self, iso_weekday, label, description=None, **kwargs):
        """
        Create and insert a new WeekDay.

        :type iso_weekday: int
        :param iso_weekday: ISO iso_weekday: Monday is 1 and Sunday is 7.
        :type label: unicode
        :param label: Display name of the day => used in selection.
        :type description: unicode
        :param description: Description of the day => used in tooltip.
        :param kwargs: additional keywords.
        :rtype: WeekDay
        :return: The new WeekDay.
        """
        return super(WeekDayAccessor, self)._insert_record(iso_weekday=iso_weekday,
                                                           label=label,
                                                           description=description,
                                                           **kwargs)

    def get_week_day_list(self, filter_cond=None, order_by_cond=None):
        """
        Search the records matching the given *filter* and sorted according to the given *order-by* condition.

        :param filter_cond: Matching predicate, can be a list of predicates.
        :param order_by_cond: Order-by condition, can be a list of conditions.
        :rtype: list[WeekDay]
        :return: Ordered list of WeekDay instances.
        """
        return super(WeekDayAccessor, self)._get_record_list(filter_cond, order_by_cond)

    def update_week_day(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :param kwargs: keywords arguments: "label", "description", "modulo", "quotient".
        :rtype: WeekDay
        :return: The updated WeekDay.
        """
        return super(WeekDayAccessor, self)._update_record(uid, **kwargs)
