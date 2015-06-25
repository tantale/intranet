"""
:module: intranet.controllers.pointage.prefs
:date: 2014-01-16
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import logging

from tg.decorators import without_trailing_slash, expose

from intranet.controllers.session_obj.layout import LayoutController
from intranet.lib.base import BaseController

LOG = logging.getLogger(__name__)


class PrefsController(BaseController):
    """
    User preferences (configuration).

    .. versionchanged:: 1.4.0
        Add layout controller to memorize the position of the left frame.
    """
    layout = LayoutController("prefs")

    def __init__(self, main_menu):
        self.main_menu = main_menu

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('intranet.templates.pointage.prefs.index')
    def index(self):
        """
        Display the index page.
        """
        return dict(main_menu=self.main_menu)
