# -*- coding: utf-8 -*-
import json
import logging
import pprint

import pylons
import sqlalchemy.exc
import transaction
import webob.exc
from formencode import All
from formencode.validators import NotEmpty, MaxLength
from pylons.i18n import ugettext as _
from tg import expose, flash, validate, redirect
from tg.controllers import RestController
from tg.decorators import with_trailing_slash, without_trailing_slash
from tg.validation import TGValidationError

from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.model import DayPeriod

LOG = logging.getLogger(__name__)


# noinspection PyAbstractClass
class DayPeriodController(RestController):
    # noinspection PyUnusedLocal
    def _before(self, *args, **kw):
        self.accessor = DayPeriodAccessor()
        url = kw["url"]
        parts = url.split("/")
        # Is it: /admin/planning/week_hours/day_periods
        #    or: /admin/planning/week_hours/{week_hours_uid}/day_periods
        week_hours = parts.index("week_hours")
        day_periods = parts.index("day_periods")
        self.week_hours_uid = None if week_hours + 1 == day_periods else int(parts[week_hours + 1])

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.week_hours.day_period.get_one")
    def get_one(self, uid):
        LOG.info(u"get_one: " + pprint.pformat(locals()))
        day_period = self.accessor.get_day_period(uid)
        return dict(week_hours_uid=self.week_hours_uid, day_period=day_period)

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.week_hours.day_period.get_one")
    def get_by_label(self, label):
        LOG.info(u"get_by_label: " + pprint.pformat(locals()))
        day_period = self.accessor.get_by_label(self.week_hours_uid, label)
        return dict(week_hours_uid=self.week_hours_uid, day_period=day_period)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("json")
    def get_all(self):
        if self.week_hours_uid:
            day_period_list = self.accessor.get_day_period_list(DayPeriod.week_hours_uid == self.week_hours_uid)
        else:
            day_period_list = self.accessor.get_day_period_list()
        return dict(week_hours_uid=self.week_hours_uid, day_period_list=day_period_list)

    # /admin/planning/week_hours/day_periods/new
    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.week_hours.day_period.new")
    def new(self, **kwargs):
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        LOG.info(u"new: " + pprint.pformat(locals()))
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(week_hours_uid=self.week_hours_uid, values=kwargs, form_errors=form_errors)

    @validate({'label': All(NotEmpty(), MaxLength(32)),
               'description': MaxLength(200)},
              error_handler=new)
    @expose()
    def post(self, label, description=None, **kwargs):
        LOG.info(u"post: " + pprint.pformat(locals()))
        try:
            self.accessor.insert_day_period(self.week_hours_uid, label, description)
        except sqlalchemy.exc.IntegrityError as exc:
            transaction.abort()
            LOG.warning(exc)
            if "constraint failed: DayPeriod.week_hours_uid, DayPeriod.label" in exc.message:
                msg_fmt = _(u"Le libellé doit être unique")
            else:
                msg_fmt = _(u"Erreur d’intégrité : {exc}")
            err_msg = msg_fmt.format(exc=exc)
            raise TGValidationError(err_msg,
                                    value=dict(label=label, description=description),
                                    error_dict=dict(label=err_msg))
        redirect('./get_by_label', label=label)

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.week_hours.day_period.get_delete")
    def get_delete(self, uid=None):
        LOG.info(u"get_delete: " + pprint.pformat(locals()))
        day_period = self.accessor.get_day_period(uid)
        return dict(week_hours_uid=self.week_hours_uid, day_period=day_period)

    @expose()
    def post_delete(self, uid):
        """
        Delete an existing day_period.

        :param uid: UID of the day_period to delete.
        """
        LOG.info(u"post_delete: " + pprint.pformat(locals()))
        self.accessor.delete_day_period(uid)
        # return dict(id='day_period_{uid}'.format(uid=uid))

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
            self.accessor.update_day_period(uid, **{field: value})
        except sqlalchemy.exc.IntegrityError as exc:
            transaction.abort()
            if "constraint failed: DayPeriod.week_hours_uid, DayPeriod.label" in exc.message:
                msg_fmt = _(u"Le libellé doit être unique")
            else:
                msg_fmt = _(u"Erreur d’intégrité : {exc}")
            err_msg = msg_fmt.format(exc=exc)
            raise JsonBadRequest(dict(status=u'error', msg=err_msg))
        return dict(status=u'updated')


class JsonBadRequest(webob.exc.HTTPBadRequest):
    def __init__(self, obj):
        super(JsonBadRequest, self).__init__(body=json.dumps(obj), content_type="application/json")
