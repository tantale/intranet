# -*- coding: utf-8 -*-
import logging
from pprint import pformat

import pylons
from pylons.i18n import ugettext as _
from tg import expose, flash

from tg.controllers import RestController

from tg.decorators import with_trailing_slash, without_trailing_slash

from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor

LOG = logging.getLogger(__name__)


class WeekHoursController(RestController):
    def _before(self, *args, **kw):
        self.accessor = WeekHoursAccessor()

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.planning.week_hours.index")
    def index(self, **kwargs):
        LOG.info("index, kw = " + pformat(kwargs))
        return dict(values=kwargs)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.planning.week_hours.get_one")
    def get_one(self, uid):
        LOG.info("get_one, uid = " + pformat(uid))
        week_hours = self.accessor.get_week_hours(uid)
        day_period_accessor = DayPeriodAccessor()
        day_period_list = day_period_accessor.get_day_period_list()
        week_day_accessor = WeekDayAccessor()
        week_day_list = week_day_accessor.get_week_day_list()
        hours_interval_accessor = HoursIntervalAccessor()
        hours_interval_table = hours_interval_accessor.get_hours_interval_table(uid)
        return dict(week_hours=week_hours,
                    day_period_list=day_period_list,
                    week_day_list=week_day_list,
                    hours_interval_table=hours_interval_table)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.planning.week_hours.get_all")
    def get_all(self, **kwargs):
        LOG.info("get_all, kw = " + pformat(kwargs))
        return dict(values=kwargs, week_hours_list=self.accessor.get_week_hours_list())

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.week_hours.new")
    def new(self, **kwargs):
        LOG.info("new, kw = " + pformat(kwargs))
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(values=kwargs, form_errors=form_errors)
