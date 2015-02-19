"""
:module: intranet.controllers.pointage.prefs
:date: 2014-01-16
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.lib.base import BaseController
import logging

from tg.decorators import without_trailing_slash, expose


LOG = logging.getLogger(__name__)


class PrefsController(BaseController):
    def __init__(self, main_menu):
        self.main_menu = main_menu

    @without_trailing_slash
    @expose('intranet.templates.pointage.prefs.index')
    def index(self):
        """
        Display the index page.
        """
        return dict(main_menu=self.main_menu)
