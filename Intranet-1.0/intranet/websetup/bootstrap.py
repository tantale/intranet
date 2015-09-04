# -*- coding: utf-8 -*-
"""Setup the Intranet application"""
import collections
import logging

from sqlalchemy.exc import IntegrityError
import transaction

from intranet import model
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.frequency import FrequencyAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.websetup.employee_list import get_employee_list

LOG = logging.getLogger(__name__)


def bootstrap(command, conf, vars):  # @ReservedAssignment
    """Place any commands to setup intranet here"""
    # -- initialize the order categories
    try:
        cat_dict = collections.OrderedDict()
        cat_dict.update({u"Commandes client":
                             [dict(cat_name=u"colorMagasin",
                                   label=u"Magasin",
                                   css_def=u"background-color: #ea750c; color: white;"),  # @IgnorePep8
                              dict(cat_name=u"colorBureau",
                                   label=u"Bureau",
                                   css_def=u"background-color: #f6a9bc; color: black;"),  # @IgnorePep8
                              dict(cat_name=u"colorDressing",
                                   label=u"Dressing",
                                   css_def=u"background-color: #37ab51; color: white;"),  # @IgnorePep8
                              dict(cat_name=u"colorMeuble",
                                   label=u"Meuble",
                                   css_def=u"background-color: #bf0e1d; color: white;"),  # @IgnorePep8
                              dict(cat_name=u"colorMenuiserie",
                                   label=u"Menuiserie",
                                   css_def=u"background-color: #f7c181; color: black;"),  # @IgnorePep8
                              dict(cat_name=u"colorBain",
                                   label=u"Salle de bain",
                                   css_def=u"background-color: #009fe5; color: white;"),  # @IgnorePep8
                              dict(cat_name=u"colorCuisine",
                                   label=u"Cuisine",
                                   css_def=u"background-color: #fcc51c; color: black;")]})  # @IgnorePep8
        cat_dict.update({u"Projets interne":
                             [dict(cat_name=u"colorRenovation",
                                   label=u"Rénovation",
                                   css_def=u"background-color: #0B610B; color: white;")]})  # @IgnorePep8
        cat_dict.update({u"Hors projet":
                             [dict(cat_name=u"colorConges",
                                   label=u"Congés",
                                   css_def=u"background-color: #6A0888; color: white;"),  # @IgnorePep8
                              dict(cat_name=u"colorNettoyage",
                                   label=u"Nettoyage",
                                   css_def=u"background-color: #61380B; color: white;"),  # @IgnorePep8
                              dict(cat_name=u"colorDechargement",
                                   label=u"Déchargement",
                                   css_def=u"background-color: #8A2908; color: white;")]})  # @IgnorePep8
        for group, entry_list in cat_dict.iteritems():
            LOG.info(u"Add order category's group: {}".format(group))
            for entry in entry_list:
                LOG.info(u"- Add order category: {}".format(entry['cat_name']))
                order_cat = model.OrderCat(cat_group=group, **entry)
                model.DBSession.add(order_cat)
            transaction.commit()
    except IntegrityError:
        LOG.warning(('There was a problem adding your order categories data, '
                     'they may have already been added'), exc_info=True)
        transaction.abort()

    # -- initialize the employee list
    employee_list = get_employee_list()
    try:
        model.DBSession.add_all(employee_list)
        transaction.commit()
    except IntegrityError:
        LOG.warning(('There was a problem adding your employees data, '
                     'they may have already been added:'), exc_info=True)

    week_day_accessor = WeekDayAccessor(model.DBSession)
    week_hours_accessor = WeekHoursAccessor(model.DBSession)
    day_period_accessor = DayPeriodAccessor(model.DBSession)
    hours_interval_accessor = HoursIntervalAccessor(model.DBSession)
    calendar_accessor = CalendarAccessor(model.DBSession)
    frequency_accessor = FrequencyAccessor(model.DBSession)

    week_day_accessor.setup()
    week_hours_accessor.setup()
    week_hours_list = week_hours_accessor.get_week_hours_list()
    for week_hours in week_hours_list:
        day_period_accessor.setup(week_hours.uid)
        hours_interval_accessor.setup(week_hours.uid)
        calendar_accessor.setup(week_hours.uid)
    frequency_accessor.setup()
