# -*- coding: utf-8 -*-
import logging
from pprint import pformat

from formencode.validators import NotEmpty, Int, String
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


# noinspection PyAbstractClass
class CalendarController(RestController):
    #: Default Event colors: intranet/public/css/fullcalendar.css:264
    BACKGROUND_COLOR = "#cc0000"
    BORDER_COLOR = "#cc0000"
    TEXT_COLOR = "#ffffff"

    # noinspection PyUnusedLocal
    def _before(self, *args, **kwargs):
        self.accessor = CalendarAccessor()

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose("intranet.templates.planning.calendar.index")
    def index(self, **kwargs):
        LOG.info("index, kwargs = " + pformat(kwargs))
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
        return dict(calendar_list=self.accessor.get_calendar_list(),
                    employee_list=self.accessor.get_employee_list(),
                    week_hours_list=self.accessor.get_week_hours_list(),
                    order_cat_groups=self.accessor.order_cat_accessor.get_order_cat_groups())

    # @expose('intranet.templates.planning.calendar.edit')
    # def edit(self, uid, **kwargs):
    #     form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
    #     calendar = self.accessor.get_calendar(uid)
    #     values = dict(uid=calendar.uid,
    #                   label=calendar.label,
    #                   description=calendar.description,
    #                   employee_uid=calendar.employee_uid,
    #                   week_hours_uid=calendar.week_hours_uid)
    #     values.update(kwargs)
    #     return dict(uid=uid,
    #                 values=values, form_errors=form_errors,
    #                 employee_list=self.accessor.get_employee_list(),
    #                 week_hours_list=self.accessor.get_week_hours_list())

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.calendar.new")
    def new(self, **kwargs):
        LOG.info("new, kwargs = " + pformat(kwargs))
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        kwargs.setdefault("background_color", self.BACKGROUND_COLOR)
        kwargs.setdefault("border_color", self.BORDER_COLOR)
        kwargs.setdefault("text_color", self.TEXT_COLOR)
        return dict(values=kwargs, form_errors=form_errors,
                    employee_list=self.accessor.get_employee_list(),
                    week_hours_list=self.accessor.get_week_hours_list(),
                    order_cat_groups=self.accessor.order_cat_accessor.get_order_cat_groups())

    @validate({'week_hours_uid': Int(min=0),
               'label': NotEmpty(),
               'employee_uid': Int(min=0),
               'background_color': String(len=7),
               'border_color': String(len=7),
               'text_color': String(len=7),
               'class_name': String(len=50)},
              error_handler=new)
    @expose()
    def post(self, week_hours_uid, label, description, employee_uid,
             background_color, border_color, text_color, class_name, **kwargs):
        LOG.info("post, kwargs={0}".format(pformat(kwargs)))
        try:
            self.accessor.insert_calendar(week_hours_uid, label, description,
                                          employee_uid=employee_uid,
                                          background_color=background_color,
                                          border_color=border_color,
                                          text_color=text_color,
                                          class_name=class_name)
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
                     employee_uid=employee_uid,
                     background_color=background_color,
                     border_color=border_color,
                     text_color=text_color,
                     class_name=class_name)
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

    # @expose()
    # def put(self, uid, week_hours_uid, label, description, employee_uid, **kwargs):
    #     LOG.info("put, kwargs={0}".format(pformat(kwargs)))
    #     label = label or None
    #     description = description or None
    #     week_hours_uid = int(week_hours_uid)
    #     employee_uid = int(employee_uid) if employee_uid else None
    #     self.accessor.update_calendar(uid,
    #                                   label=label,
    #                                   description=description,
    #                                   week_hours_uid=week_hours_uid,
    #                                   employee_uid=employee_uid)

    @expose('json')
    def edit_in_place(self, name, value, **kwargs):
        """
        edit_label, kwargs={'name': u'calendar_4_label', 'pk': u'unused', 'value': u'gfggfdf'}

        :param kwargs:
        :return:
        """
        LOG.info("edit_in_place, name={name}, value={value}, kwargs={kwargs}".format(name=name,
                                                                                     value=pformat(value),
                                                                                     kwargs=pformat(kwargs)))
        uid, field = name.split("_", 2)[1:]
        try:
            self.accessor.update_calendar(uid, **{field: value})
        except sqlalchemy.exc.IntegrityError:
            transaction.abort()
            assert field == "label"
            if value:
                msg_fmt = _(u"Libellé du calendrier en doublon ! "
                            u"Le libellé « {label} » existe déjà.")
            else:
                msg_fmt = _(u"Libellé du calendrier vide !")
            err_msg = msg_fmt.format(label=value)
            return dict(status='error', msg=err_msg)
        return dict(status='updated')
