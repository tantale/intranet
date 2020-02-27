# -*- coding: utf-8 -*-
import datetime
import json
import logging
import pprint

import pylons
import sqlalchemy.exc
import transaction
import webob.exc
from formencode.validators import NotEmpty
from pylons.i18n import ugettext as _
from tg import expose, flash
from tg.controllers import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, without_trailing_slash, validate

from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.controllers.planning.day_period import DayPeriodController

LOG = logging.getLogger(__name__)


# noinspection PyAbstractClass
class WeekHoursController(RestController):
    # /admin/planning/week_hours/{week_hours_uid}/day_periods
    day_periods = DayPeriodController()

    # noinspection PyUnusedLocal
    def _before(self, *args, **kw):
        self.accessor = WeekHoursAccessor()
        self.hours_interval_accessor = HoursIntervalAccessor()

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.planning.week_hours.index")
    def index(self, **kwargs):
        LOG.info("index, kw = " + pprint.pformat(kwargs))
        return dict(values=kwargs)

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("json")
    def get_one(self, uid):
        LOG.info(u"get_one: " + pprint.pformat(locals()))
        return dict(week_hour=self.accessor.get_week_hours(uid))

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.planning.week_hours.get_all")
    def get_all(self):
        LOG.info("get_all")
        week_day_accessor = WeekDayAccessor()
        week_day_list = week_day_accessor.get_week_day_list()
        return dict(week_hours_list=self.accessor.get_week_hours_list(),
                    week_day_list=week_day_list)

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.week_hours.new")
    def new(self, **kwargs):
        LOG.info("new, kw = " + pprint.pformat(kwargs))
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(values=kwargs, form_errors=form_errors)

    @validate({'label': NotEmpty()},
              error_handler=new)
    @expose()
    def post(self, label, description, **kwargs):
        if LOG.isEnabledFor(logging.INFO):
            msg_fmt = u"post: label={label}, description={description}, kwargs={kwargs}"
            LOG.info(msg_fmt.format(label=pprint.pformat(label),
                                    description=pprint.pformat(description),
                                    kwargs=pprint.pformat(kwargs)))
        try:
            self.accessor.insert_week_hours(label, description)
        except sqlalchemy.exc.IntegrityError as exc:
            transaction.abort()
            LOG.warning(exc)
            if label:
                msg_fmt = _(u"Libellé du calendrier en doublon ! "
                            u"Le libellé « {label} » existe déjà.")
            else:
                msg_fmt = _(u"Libellé du calendrier vide !")
            err_msg = msg_fmt.format(label=label)
            flash(err_msg, status="error")
            redirect('./new',
                     label=label,
                     description=description)
        else:
            msg_fmt = _(u"La grille d’horaires « {label} » a été créée "
                        u"dans la base de données avec succès.")
            flash(msg_fmt.format(label=label), status="ok")
            redirect('./new')

    @expose('intranet.templates.planning.week_hours.get_delete')
    def get_delete(self, uid):
        LOG.info("get_delete, uid={0}".format(pprint.pformat(uid)))
        return dict(week_hours=self.accessor.get_week_hours(uid))

    @expose()
    def post_delete(self, uid):
        LOG.info("post_delete, uid={0}".format(pprint.pformat(uid)))
        old_week_hours = self.accessor.delete_week_hours(uid)
        msg_fmt = _(u"La grille d’horaires « {label} » a été supprimée "
                    u"de la base de données avec succès.")
        flash(msg_fmt.format(label=old_week_hours.label), status="ok")
        return dict()

    @expose('json')
    def edit_in_place(self, name, value, **kwargs):
        """
        Edit the label or the description of the WeekHours in-place

        :param name: Name of the field, eg.: "week_hours_2_description".
        :param value: "A text"
        :param kwargs: Not used, eg.: {'pk': 'unused'}.
        :return: The update status as a JSON object.
        """
        LOG.info(u"edit_in_place: " + pprint.pformat(locals()))
        # name: "week_hours_1_day_period_3_label"
        parts = name.split("_")
        uid, field = parts[-2:]
        if field == "label" and not value:
            msg_fmt = _(u"Le libellé ne doit pas être vide")
            err_msg = msg_fmt.format(label=value)
            raise JsonBadRequest(dict(status=u'error', msg=err_msg))
        try:
            self.accessor.update_week_hours(uid, **{field: value})
        except sqlalchemy.exc.IntegrityError as exc:
            transaction.abort()
            if "constraint failed: DayPeriod.week_hours_uid, DayPeriod.label" in exc.message:
                msg_fmt = _(u"Le libellé doit être unique")
            else:
                msg_fmt = _(u"Erreur d’intégrité : {exc}")
            err_msg = msg_fmt.format(exc=exc)
            raise JsonBadRequest(dict(status=u'error', msg=err_msg))
        return dict(status=u'updated')

    @expose('json')
    def edit_hours_interval(self, week_day_uid, day_period_uid, start_hour, end_hour):
        """
        Edit a hours interval

        :param week_day_uid: Hours interval composite UID.
        :param day_period_uid: Hours interval composite UID.
        :param start_hour: String representation of the start hour.
        :param end_hour: String representation of the end hour.
        :return: The update status as a JSON object.
        """
        LOG.info(u"edit_hours_interval: " + pprint.pformat(locals()))

        def get_time(date_string):
            for time_fmt in ("%H:%M:%S", "%H:%M"):
                try:
                    return datetime.datetime.strptime(date_string, time_fmt).time()
                except ValueError:
                    pass
            return None

        start_hour = get_time(start_hour)
        end_hour = get_time(end_hour)
        return self.hours_interval_accessor.edit_hours_interval(week_day_uid, day_period_uid, start_hour, end_hour)


class JsonBadRequest(webob.exc.HTTPBadRequest):
    def __init__(self, obj):
        super(JsonBadRequest, self).__init__(body=json.dumps(obj), content_type="application/json")
