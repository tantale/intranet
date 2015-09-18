# -*- coding: utf-8 -*-
import logging
import pprint

from formencode.validators import NotEmpty
import pylons
from pylons.i18n import ugettext as _
from tg import expose, flash
from tg.controllers import RestController
from tg.decorators import with_trailing_slash, without_trailing_slash, validate
from tg.controllers.util import redirect
import sqlalchemy.exc
import transaction

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
        LOG.info("index, kw = " + pprint.pformat(kwargs))
        return dict(values=kwargs)

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
