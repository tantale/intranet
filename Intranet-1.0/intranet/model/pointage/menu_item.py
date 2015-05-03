# -*- coding: utf-8 -*-
"""
Menu item
=========

Date: 2013-10-08

Author: Laurent LAPORTE <sandlol2009@gmail.com>
"""


class MenuItem(object):

    _AUTO_INCREMENT = 0

    ITEM_PAGE = u"PAGE"
    ITEM_HEADER = u"HEADER"
    ITEM_SEPARATOR = u"SEPARATOR"

    def __init__(self, display_name, description, icon_name, target_page=None, item_type=ITEM_PAGE):
        MenuItem._AUTO_INCREMENT += 1
        self._uid = self._AUTO_INCREMENT
        self._parent_menu = None
        self._item_list = []
        self.display_name = display_name
        self.description = description
        self.icon_name = icon_name
        self.target_page = target_page
        self.item_type = item_type

    @property
    def is_header(self):
        return self.item_type == self.ITEM_HEADER

    @property
    def is_separator(self):
        return self.item_type == self.ITEM_SEPARATOR

    @property
    def uid(self):
        return self._uid

    @property
    def parent_menu(self):
        return self._parent_menu

    @parent_menu.setter
    def parent_menu(self, menu_item):
        self._parent_menu = menu_item

    @property
    def item_list(self):
        return self._item_list

    def append(self, menu_item):
        menu_item.parent_menu = self
        self.item_list.append(menu_item)

    def extend(self, item_list):
        for item in item_list:
            self.append(item)


class MenuHeader(MenuItem):
    def __init__(self, display_name, description, icon_name=None):
        super(MenuHeader, self).__init__(display_name, description, icon_name, item_type=self.ITEM_HEADER)


class MenuSeparator(MenuItem):
    def __init__(self, display_name=u""):
        super(MenuSeparator, self).__init__(display_name, None, None, item_type=self.ITEM_SEPARATOR)
