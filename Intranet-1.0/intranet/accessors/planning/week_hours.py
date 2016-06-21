# -*- coding: utf-8 -*-
import copy

import sqlalchemy.exc
import transaction
from sqlalchemy.sql.functions import func
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.model.planning.week_hours import WeekHours

try:
    _("")
except TypeError:
    def _(x):
        return x


class WeekHoursAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(WeekHoursAccessor, self).__init__(WeekHours, session=session)

    def setup(self):
        try:
            with transaction.manager:
                # noinspection SpellCheckingInspection
                self.session.add_all([
                    WeekHours(1, _(u"Grille d’horaires normales"), _(u"Grille d’horaires d’ouverture de l’entreprise"))
                ])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()

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

    def get_by_label(self, label):
        """
        Get the week hours by label

        :type label: unicode
        :param label: Week hours label.
        :rtype: WeekHours
        :return: The matching week hours.
        :raise sqlalchemy.orm.exc.NoResultFound: if the record is not found.
        """
        return self.session.query(WeekHours).filter(WeekHours.label == label).one()

    def insert_week_hours(self, label, description):
        """
        Create and insert a new WeekHours.

        :type label: unicode
        :param label: Display name of the day => used in selection.
        :type description: unicode
        :param description: Description of the day => used in tooltip.
        :rtype: WeekHours
        :return: The new WeekHours.
        """
        with transaction.manager:
            last_position = self.session.query(func.max(WeekHours.position)).scalar() or 0
            week_hours = WeekHours(last_position + 1, label, description)
            first = self.session.query(WeekHours).filter(WeekHours.label != label).first()
            if first:
                week_hours.day_period_list = copy.deepcopy(first.day_period_list)
            self.session.add(week_hours)

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

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :param kwargs: keywords arguments: "label", "description", "modulo", "quotient".
        :rtype: WeekHours
        :return: The updated WeekHours.
        """
        return super(WeekHoursAccessor, self)._update_record(uid, **kwargs)
