# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlalchemy.exc

import transaction
from tg.i18n import ugettext as _

from intranet.accessors import BasicAccessor
from intranet.model.worked_hours.frequency import Frequency

try:
    _("")
except TypeError:
    _ = lambda x: x


class FrequencyAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(FrequencyAccessor, self).__init__(Frequency, session=session)

    def setup(self):
        try:
            with transaction.manager:
                self.session.add_all([
                    Frequency(_("Apériodique"), _("Horaires valables toute l'année"), 0, 1),
                    Frequency(_("Semaines impaires"), _("Horaires valables les semaines impaires"), 1, 2),
                    Frequency(_("Semaines paires"), _("Horaires valables les semaines paires"), 0, 2)
                ])
        except sqlalchemy.exc.IntegrityError:
            pass  # setup already done.

    def delete_frequency(self, uid):
        """
        Delete the frequency.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: Frequency
        :return: The old Frequency.
        """
        return super(FrequencyAccessor, self)._delete_record(uid)

    def get_frequency(self, uid):
        """
        Get a frequency given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: Frequency
        :return: The Frequency.
        """
        return super(FrequencyAccessor, self)._get_record(uid)

    def insert_frequency(self, label, description, modulo, quotient, **kwargs):
        """
        Create and insert a new Frequency.

        :type label: unicode
        :param label: Display name of the frequency (no duplicate) => used in selection.
        :type description: unicode
        :param description: Description of the frequency => used in tooltip.
        :type modulo: int
        :param modulo: Modulo value of the frequency: 0 <= modulo < quotient
        :type quotient: int
        :param quotient: Quotient value of the frequency: quotient > 0
        :param kwargs: additional keywords.
        :rtype: Frequency
        :return: The new Frequency.
        """
        return super(FrequencyAccessor, self)._insert_record(label=label,
                                                             description=description,
                                                             modulo=modulo,
                                                             quotient=quotient,
                                                             **kwargs)

    def get_frequency_list(self, filter_cond=None, order_by_cond=None):
        """
        Search the records matching the given *filter* and sorted according to the given *order-by* condition.

        :param filter_cond: Matching predicate, can be a list of predicates.
        :param order_by_cond: Order-by condition, can be a list of conditions.
        :rtype: list[Frequency]
        :return: Ordered list of Frequency instances.
        """
        return super(FrequencyAccessor, self)._get_record_list(filter_cond, order_by_cond)

    def update_frequency(self, uid, **kwargs):
        """
        Update the fields of a given record.

        :param kwargs: keywords arguments: "label", "description", "modulo", "quotient".
        :rtype: Frequency
        :return: The updated Frequency.
        """
        return super(FrequencyAccessor, self)._update_record(uid, **kwargs)
