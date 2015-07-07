# -*- coding: utf-8 -*-
import sqlalchemy.exc

import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.model.worked_hours.week_hours import WeekHours

try:
    _("")
except TypeError:
    _ = lambda x: x


class WeekHoursAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(WeekHoursAccessor, self).__init__(WeekHours, session=session)

    def setup(self):
        try:
            with transaction.manager:
                self.session.add_all([
                    WeekHours(1, _(u"Horaires d’ouverture"), _(u"Horaires d’ouverture de l’entreprise"))
                ])
        except sqlalchemy.exc.IntegrityError:
            pass  # setup already done.

    def delete_week_hours(self, uid):
        """
        Delete the week_hours.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: WeekHours
        :return: The old WeekHours.
        """
        return super(WeekHoursAccessor, self)._delete_record(uid)

    def get_week_hours(self, uid):
        """
        Get a week_hours given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: WeekHours
        :return: The WeekHours.
        """
        return super(WeekHoursAccessor, self)._get_record(uid)

    def insert_week_hours(self, position, label, description, **kwargs):
        """
        Create and insert a new WeekHours.

        :type position: int
        :param position: Relative position.
        :type label: unicode
        :param label: Display name of the day => used in selection.
        :type description: unicode
        :param description: Description of the day => used in tooltip.
        :param kwargs: additional keywords.
        :rtype: WeekHours
        :return: The new WeekHours.
        """
        return super(WeekHoursAccessor, self)._insert_record(position=position,
                                                             label=label,
                                                             description=description,
                                                             **kwargs)

    def get_week_hours_list(self, filter_cond=None, order_by_cond=None):
        """
        Search the records matching the given *filter* and sorted according to the given *order-by* condition.

        :param filter_cond: Matching predicate, can be a list of predicates.
        :param order_by_cond: Order-by condition, can be a list of conditions.
        :rtype: list[WeekHours]
        :return: Ordered list of WeekHours instances.
        """
        return super(WeekHoursAccessor, self)._get_record_list(filter_cond, order_by_cond)

    def update_week_hours(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :param kwargs: keywords arguments: "label", "description", "modulo", "quotient".
        :rtype: WeekHours
        :return: The updated WeekHours.
        """
        return super(WeekHoursAccessor, self)._update_record(uid, **kwargs)
