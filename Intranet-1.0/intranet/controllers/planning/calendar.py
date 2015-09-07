# -*- coding: utf-8 -*-
import logging
from pprint import pformat

from formencode.validators import NotEmpty, Int
import pylons
from pylons.i18n import ugettext as _
from tg import expose, flash
from tg.controllers import RestController
from tg.decorators import with_trailing_slash, without_trailing_slash, validate
from tg.controllers.util import redirect
import sqlalchemy.exc
import transaction

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
    @expose("json")
    def get_all(self):
        LOG.info("get_all")
        return dict(calendar_list=self.accessor.get_calendar_list())

    @expose('intranet.templates.planning.calendar.edit')
    def edit(self, uid, **kw):
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        calendar = self.accessor.get_calendar(uid)
        values = dict(uid=calendar.uid,
                      label=calendar.label,
                      description=calendar.description,
                      employee_uid=calendar.employee_uid,
                      week_hours_uid=calendar.week_hours_uid)
        values.update(kw)
        return dict(uid=uid,
                    values=values, form_errors=form_errors,
                    employee_list=self.accessor.get_employee_list(),
                    week_hours_list=self.accessor.get_week_hours_list())

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
                    employee_list=self.accessor.get_employee_list(),
                    week_hours_list=self.accessor.get_week_hours_list())

    @validate({'week_hours_uid': Int(min=0),
               'label': NotEmpty(),
               'employee_uid': Int(min=0)},
              error_handler=new)
    @expose()
    def post(self, week_hours_uid, label, description, employee_uid, **kw):
        LOG.info("post, kw={0}".format(pformat(kw)))
        try:
            label = label or None
            description = description or None
            week_hours_uid = int(week_hours_uid)
            employee_uid = int(employee_uid) if employee_uid else None
            self.accessor.insert_calendar(week_hours_uid, label, description, employee_uid=employee_uid)
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
                     week_hours_uid=week_hours_uid,
                     label=label,
                     description=description,
                     employee_uid=employee_uid)
        else:
            msg_fmt = _(u"Le calendrier « {label} » a été créé "
                        u"dans la base de données avec succès.")
            flash(msg_fmt.format(label=label), status="ok")
            redirect('./new')

    @expose('intranet.templates.planning.calendar.get_delete')
    def get_delete(self, uid):
        LOG.info("get_delete, uid={0}".format(pformat(uid)))
        return dict(calendar=self.accessor.get_calendar(uid))

    @expose()
    def post_delete(self, uid):
        LOG.info("post_delete, uid={0}".format(pformat(uid)))
        old_calendar = self.accessor.delete_calendar(uid)
        msg_fmt = _(u"Le calendrier « {label} » a été supprimé "
                    u"de la base de données avec succès.")
        flash(msg_fmt.format(label=old_calendar.label), status="ok")
        return dict()
