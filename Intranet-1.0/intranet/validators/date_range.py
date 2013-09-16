# -*- coding: utf-8 -*-
"""
:module: intranet.validators.date_range
:date: 2013-09-15
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from formencode.validators import FormValidator
from formencode.api import Invalid


class DateRange(FormValidator):
    """
    classdocs
    """

    # TODO: i18n
    messages = dict(field_required=(u'La date "%(field_name)s" est requise.'),
                    equals=(u'Les deux dates sont identiques : %(date)s.'),
                    reversed=(u'La date %(start_date)s doit précéder '
                              u'la date %(end_date)s".'))

    # start_date and end_date fields
    start_date = None
    end_date = None

    __unpackargs__ = ('start_date', 'end_date')

    def validate_python(self, value_dict, state):
        start_date = value_dict.get(self.start_date)
        end_date = value_dict.get(self.end_date)
        if start_date is None:
            # TODO: i18n
            err_msg = (u"L'intervalle de dates n'est pas valide : "
                       u"champ obligatoire.")
            raise Invalid(err_msg,
                value_dict, state,
                error_dict={self.start_date:
                            self.message('field_required', state,
                                         field_name=self.start_date)})
        elif end_date is not None and start_date == end_date:
            # TODO: i18n
            err_msg = (u"L'intervalle de dates n'est pas valide : "
                       u"dates identiques.")
            date_fr = start_date.strftime("%d/%m/%Y")  # TODO: i18n
            raise Invalid(err_msg,
                value_dict, state,
                error_dict={self.end_date:
                            self.message('equals', state, date=date_fr)})
        elif end_date is not None and start_date >= end_date:
            # TODO: i18n
            err_msg = (u"L'intervalle de dates n'est pas valide : "
                       u"ordre des dates inversé.")
            start_date_fr = start_date.strftime("%d/%m/%Y")  # TODO: i18n
            end_date_fr = end_date.strftime("%d/%m/%Y")  # TODO: i18n
            raise Invalid(err_msg,
                value_dict, state,
                error_dict={self.end_date:
                            self.message('reversed', state,
                                         start_date=start_date_fr,
                                         end_date=end_date_fr)})
