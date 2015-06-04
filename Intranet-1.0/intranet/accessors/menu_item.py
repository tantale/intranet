# -*- coding: utf-8 -*-
"""
menu_item
=============

Date: 2015-03-31

Author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from __future__ import unicode_literals
import logging

import tg

from intranet.accessors import BasicAccessor
from intranet.model.pointage.menu_item import MenuItem, MenuHeader, MenuSeparator


LOG = logging.getLogger(__name__)


class MenuItemAccessor(BasicAccessor):
    ADMIN_MENU = MenuHeader("Administration", "Administration de l‘application")
    ADMIN_MENU.extend([
        MenuItem("Employés", "Gestion des employés", "ui-icon-person",
                 target_page=tg.url('/admin/employee/index.html')),
        MenuItem("Commandes", "Gestion des commandes et des phases", "ui-icon-document",
                 target_page=tg.url('/admin/order/index.html')),
        MenuItem("Pointage", "Gestion des pointages des opérations", "ui-icon-clock",
                 target_page=tg.url('/admin/trcal/index.html')),
        MenuItem("Planning", "Planning des événements", "ui-icon-calendar",
                 target_page=tg.url('/admin/planning/index.html')),
        # ADD: New feature: "time tracking statistics"
        # MenuItem("Statistiques", "Statistiques de pointages", "ui-icon-calculator",
        #          target_page=tg.url('/admin/chart/index.html')),
        MenuSeparator(),
        MenuItem("Préférences", "Paramétrage des préférences utilisateur", "ui-icon-gear",
                 target_page=tg.url('/admin/prefs/index.html'))])

    TIME_TRACKING_MENU = MenuHeader("Gestion des pointages", "Gestion des pointages")
    TIME_TRACKING_MENU.extend([
        MenuItem("Pointage", "Gestion des pointages des opérations", "ui-icon-calendar",
                 target_page=tg.url('/pointage/trcal/index.html'))])

    MENU_DICT = dict((x.display_name, x) for x in [ADMIN_MENU, TIME_TRACKING_MENU])

    def __init__(self, session=None):
        super(MenuItemAccessor, self).__init__(record_class=MenuItem, session=session)

    def get_main_menu(self, menu_name):
        """
        Get the main menu of a given view.

        :type menu_name: unicode
        :param menu_name: Menu name
        :rtype: MenuItem
        :return: the menu item
        """
        return self.MENU_DICT[menu_name]


print(MenuItemAccessor().get_main_menu("Administration"))
