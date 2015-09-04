# -*- coding: utf-8 -*-
import logging
from pprint import pformat

import pylons
from pylons.i18n import ugettext as _
from tg import expose, flash
from tg.controllers import RestController

from tg.decorators import with_trailing_slash, without_trailing_slash

from intranet.accessors.planning.calendar import CalendarAccessor

LOG = logging.getLogger(__name__)


class CalendarController(RestController):

    def _before(self, *args, **kw):
        self.accessor = CalendarAccessor()

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.planning.calendar.index")
    def index(self, **kwargs):
        LOG.info("index, kw = " + pformat(kwargs))
        return dict(values=kwargs)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.planning.calendar.get_one")
    def get_one(self, uid):
        LOG.info("get_one, uid = " + pformat(uid))
        calendar = self.accessor.get_calendar(uid)
        return dict(calendar=calendar)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.planning.calendar.get_all")
    def get_all(self, **kwargs):
        LOG.info("get_all, kw = " + pformat(kwargs))
        return dict(values=kwargs, calendar_list=self.accessor.get_calendar_list())

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.calendar.new")
    def new(self, **kwargs):
        LOG.info("new, kw = " + pformat(kwargs))
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(values=kwargs, form_errors=form_errors,
                    week_hours_list=self.accessor.get_week_hours_list())
