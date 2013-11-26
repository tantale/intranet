# -*- coding: utf-8 -*-
"""Main Controller"""

from intranet.controllers.admin import AdminController
from intranet.controllers.error import ErrorController
from intranet.controllers.pointage import PointageControoler
from intranet.lib.base import BaseController

from tg import expose, request, tmpl_context

# from intranet.model import DBSession, metadata
# from tg import flash, require, url, lurl, redirect
# from tg.i18n import ugettext as _, lazy_ugettext as l_

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the Intranet-1.0 application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """

    error = ErrorController()
    admin = AdminController()
    pointage = PointageControoler()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "intranet"

    @expose('intranet.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('intranet.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('intranet.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ',
                    environment=request.environ)  # @UndefinedVariable environ
