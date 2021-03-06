# -*- coding: utf-8 -*-
import datetime
import json
import logging
import pprint

import pylons
import sqlalchemy.exc
import transaction
from formencode import All
from formencode.validators import Int
from formencode.validators import MaxLength
from formencode.validators import NotEmpty
from formencode.validators import StringBool
from pylons.i18n import ugettext as _
from tg import expose
from tg import flash
from tg import redirect
from tg import validate
from tg.controllers import RestController
from tg.decorators import with_trailing_slash
from tg.decorators import without_trailing_slash

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.planning_event import PlanningEventAccessor
from intranet.controllers.session_obj.calendar_selection import CalendarSelectionController
from intranet.model import Calendar
from intranet.validators.iso_date_converter import IsoDatetimeConverter

LOG = logging.getLogger(__name__)


# noinspection PyAbstractClass
class PlanningEventController(RestController):
    """
    Planning event.

    ===========  =====================================================  ==============================
    Method       Description                                            Example Method(s) / URL(s)
    ===========  =====================================================  ==============================
    get_one      Display the data of one record                         GET /events/1
    get_all      Display the table widget and its data                  GET /events/
    new          Display new_form                                       GET /events/new
    post         Create a new record                                    POST /events/
    edit         Display edit_form and the containing record’s data     GET /events/1/edit
    put          Update an existing record                              POST /events/1?_method=PUT
                                                                        PUT /events/1
    get_delete   Delete Confirmation page                               Get /events/1/delete
    post_delete  Delete an existing record                              POST /events/1?_method=DELETE
                                                                        DELETE /events/1
    ===========  =====================================================  ==============================
    """
    calendar_selections = CalendarSelectionController("planning")

    # noinspection PyUnusedLocal
    def _before(self, *args, **kw):
        self.accessor = PlanningEventAccessor()
        self.calendar_accessor = CalendarAccessor()
        url = kw["url"]
        parts = url.split("/")
        # Is it: /admin/planning/sources/1/events
        #    or: /admin/planning/sources/events
        sources_index = parts.index("sources")
        events_index = parts.index("events")
        self.calendar_uid = None if sources_index + 1 == events_index else int(parts[sources_index + 1])

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose()
    def get_one(self, uid):
        event = self.accessor.get_planning_event(uid)
        return json.dumps(event.event_obj())

    # noinspection PyArgumentList
    @with_trailing_slash
    @validate({'start': Int(min=0),
               'end': Int(min=0)})
    @expose()
    def get_all(self, start, end, **kwargs):
        """
        Récupère le calendrier de l’utilisateur.
        Recherche tous les événements dont la date de début ou de fin se trouve dans l'intervalle [start; end[.

        Example:

            /admin/planning/sources/7/events?start=1474840800&end=1478473200&_=1479716150036

        Arguments::

            start=1472421600, end=1476050400, kwargs={'_': u'1474187468622'}
            start=1473976800, end=1474063200, kwargs={'_': u'1474187525738'}

        .. versionchanged:: 2.2.0

        :type start: int
        :param start: Start date of the calendar view (timestamp).
        :type end: int
        :param end: End date of the calendar view (+ 1 day: excluded from interval).
        :param kwargs: Contains the "no cache value".
        """
        LOG.info("get_all: start={start}, end={end}, kwargs={kwargs}".format(start=pprint.pformat(start),
                                                                             end=pprint.pformat(end),
                                                                             kwargs=pprint.pformat(kwargs)))

        # Il faut calculer les dates au format datetime pour la requête en bdd
        start_date = datetime.datetime.fromtimestamp(start)
        end_date = datetime.datetime.fromtimestamp(end)

        # Les dates sont des dates locales.
        # Il faut les convertir en date UTC pour les comparer avec les dates des événements.
        tz_offset = int(kwargs['tz_offset'])
        tz_delta = datetime.timedelta(minutes=int(tz_offset))
        start_utc = start_date + tz_delta
        end_utc = end_date + tz_delta

        #: Get all planning events in the calendar interval
        events = self.accessor.search_planning_events(self.calendar_uid, start_utc, end_utc)

        # Pour le plugin fullcalendar, on utilise des objets json
        result = [event.event_obj() for event in events]
        return json.dumps(result)

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.event.new")
    def new(self, tz_offset, **kwargs):
        LOG.info("new, kw = " + pprint.pformat(kwargs))
        # -- Convert UTC dates to local time to fill the form
        iso_fmt = "%Y-%m-%dT%H:%M:%S.000Z"  # ignore trailing milliseconds
        for key in ("event_start", "event_end"):
            date_str = kwargs.get(key)
            if date_str and date_str.endswith("Z"):
                date_utc = datetime.datetime.strptime(date_str, iso_fmt)
                tz_delta = datetime.timedelta(minutes=int(tz_offset))
                date_local = date_utc - tz_delta
                kwargs[key] = date_local.isoformat()
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        selections = self.calendar_selections.get_all()["selections"]
        if selections:
            predicate = Calendar.uid.in_(selections)
            calendar_list = self.calendar_accessor.get_calendar_list(predicate)
        else:
            # The list is empty if there is no selection.
            calendar_list = []
        return dict(tz_offset=tz_offset, values=kwargs, form_errors=form_errors,
                    calendar_list=calendar_list)

    @validate({'tz_offset': Int(min=-720, max=720),
               'calendar_uid': Int(min=0),
               'label': All(NotEmpty(), MaxLength(32)),
               'description': MaxLength(200),
               'event_start': IsoDatetimeConverter(not_empty=True),
               'event_end': IsoDatetimeConverter(not_empty=True),
               'editable': StringBool(if_empty=False),
               'all_day': StringBool(if_empty=False),
               'location': MaxLength(200),
               'private': StringBool(if_empty=False)},
              error_handler=new)
    @expose()
    def post(self, tz_offset, calendar_uid,
             label, description, event_start, event_end, editable=True, all_day=False,
             location=None, private=False,
             **kwargs):
        """
        locals = {'all_day': None,
                  'calendar_uid': 1,
                  'description': u'jhdfsjkhfsd',
                  'editable': True,
                  'event_end': datetime.datetime(2015, 10, 16, 12, 30),
                  'event_start': datetime.datetime(2015, 10, 15, 12, 30),
                  'label': u'Toto',
                  'location': u'ici',
                  'private': True,
                  'tz_offset': -120}
        """
        LOG.info("post, locals={0}".format(pprint.pformat(locals())))
        # -- Compute the UTC dates
        tz_delta = datetime.timedelta(minutes=tz_offset)
        event_start_utc = event_start + tz_delta
        event_end_utc = event_end + tz_delta
        try:
            self.accessor.insert_planning_event(calendar_uid,
                                                label,
                                                description,
                                                event_start_utc,
                                                event_end_utc,
                                                editable=editable,
                                                all_day=all_day,
                                                location=location,
                                                private=private)
        except sqlalchemy.exc.IntegrityError as exc:
            transaction.abort()
            LOG.warning(exc)
            # -- try to have a better error message
            if "start_before_end_check" in exc.message:
                msg_fmt = _(u"Les dates et heures ne sont pas cohérentes\u00a0: "
                            u"l'heure et la date de début doivent être antérieures à celles de fin.")
            elif "UNIQUE constraint failed: " \
                 "PlanningEvent.calendar_uid, PlanningEvent.event_start, PlanningEvent.event_end" in exc.message:
                msg_fmt = _(u"Les dates et heures sont déjà utilisées pour un autre événement.")
            else:
                msg_fmt = _(u"Erreur d’intégrité : {exc}")
            err_msg = msg_fmt.format(exc=exc)
            flash(err_msg, status="error")
            iso_fmt = "%Y-%m-%dT%H:%M:%S.000Z"  # ignore trailing milliseconds
            redirect('./new',
                     tz_offset=tz_offset,
                     calendar_uid=calendar_uid,
                     label=label,
                     description=description,
                     event_start=event_start_utc.strftime(iso_fmt),
                     event_end=event_end_utc.strftime(iso_fmt),
                     editable=unicode(editable).lower(),
                     all_day=unicode(all_day).lower(),
                     location=location,
                     private=unicode(private).lower())
        # -- Return a JSON object
        result = self.accessor.get_event_by_dates(calendar_uid, event_start_utc, event_end_utc)
        return json.dumps(result.event_obj())

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.event.edit")
    def edit(self, uid, tz_offset=None, **kwargs):
        if LOG.isEnabledFor(logging.INFO):
            msg_fmt = "edit: uid={uid}, tz_offset={tz_offset}, kwargs={kwargs}"
            LOG.info(msg_fmt.format(uid=pprint.pformat(uid),
                                    tz_offset=pprint.pformat(tz_offset),
                                    kwargs=pprint.pformat(kwargs)))
        tz_offset = tz_offset or 0
        event = self.accessor.get_planning_event(uid)
        # -- Convert UTC dates to local time to fill the form
        tz_delta = datetime.timedelta(minutes=int(tz_offset))
        event_start = event.event_start - tz_delta
        event_end = event.event_end - tz_delta
        values = dict(uid=event.uid,
                      tz_offset=tz_offset,
                      calendar_uid=event.calendar_uid,
                      label=event.label,
                      description=event.description,
                      event_start=event_start.isoformat(),
                      event_end=event_end.isoformat(),
                      editable=unicode(event.editable).lower(),
                      all_day=unicode(event.all_day).lower(),
                      location=event.location,
                      private=unicode(event.private).lower())
        values.update(kwargs)
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = _(u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(tz_offset=tz_offset,
                    assignation=event.assignation,
                    values=values,
                    form_errors=form_errors,
                    calendar_list=self.calendar_accessor.get_calendar_list())

    @validate({'uid': Int(min=0, not_empty=True),
               'calendar_uid': Int(min=0),
               'tz_offset': Int(min=-720, max=720),
               'label': All(NotEmpty(), MaxLength(32)),
               'description': MaxLength(200),
               'event_start': IsoDatetimeConverter(not_empty=True),
               'event_end': IsoDatetimeConverter(not_empty=True),
               'editable': StringBool(if_empty=False),
               'all_day': StringBool(if_empty=False),
               'location': MaxLength(200),
               'private': StringBool(if_empty=False)},
              error_handler=edit)
    @expose()
    def put(self, uid, calendar_uid, tz_offset, label, event_start, event_end,
            description=u"", editable=True, all_day=False,
            location=None, private=False,
            **kwargs):
        LOG.info("put, locals={0}".format(pprint.pformat(locals())))
        # -- Compute the UTC dates
        tz_delta = datetime.timedelta(minutes=tz_offset)
        event_start_utc = event_start + tz_delta
        event_end_utc = event_end + tz_delta
        try:
            self.accessor.update_planning_event(uid,
                                                calendar_uid=calendar_uid,
                                                label=label,
                                                description=description,
                                                event_start=event_start_utc,
                                                event_end=event_end_utc,
                                                editable=editable,
                                                all_day=all_day,
                                                location=location,
                                                private=private)
        except sqlalchemy.exc.IntegrityError as exc:
            transaction.abort()
            LOG.warning(exc)
            # -- try to have a better error message
            if "start_before_end_check" in exc.message:
                msg_fmt = _(u"Les dates et heures ne sont pas cohérentes\u00a0: "
                            u"l'heure et la date de début doivent être antérieures à celles de fin.")
            elif "UNIQUE constraint failed: " \
                 "PlanningEvent.calendar_uid, PlanningEvent.event_start, PlanningEvent.event_end" in exc.message:
                msg_fmt = _(u"Les dates et heures sont déjà utilisées pour un autre événement.")
            else:
                msg_fmt = _(u"Erreur d’intégrité : {exc}")
            err_msg = msg_fmt.format(exc=exc)
            flash(err_msg, status="error")
            redirect('./edit',
                     uid=uid,
                     tz_offset=tz_offset,
                     calendar_uid=calendar_uid,
                     label=label,
                     description=description,
                     event_start=event_start.isoformat(),
                     event_end=event_end.isoformat(),
                     editable=unicode(editable).lower(),
                     all_day=unicode(all_day).lower(),
                     location=location,
                     private=unicode(private).lower())
        # -- Return a JSON object
        result = self.accessor.get_event_by_dates(calendar_uid, event_start_utc, event_end_utc)
        return json.dumps(result.event_obj())

    @expose()
    def post_delete(self, uid):
        """
        Delete an existing event.

        :param uid: UID of the event to delete.
        """
        self.accessor.delete_planning_event(uid)
        # -- return an event object with it's id only
        return json.dumps(dict(id='planning_event_{uid}'.format(uid=uid)))

    @expose()
    def event_drop(self, uid, day_delta, minute_delta, all_day):
        LOG.info("event_drop, locals={0}".format(pprint.pformat(locals())))
        day_delta = int(day_delta)
        minute_delta = int(minute_delta)
        all_day = unicode(all_day).lower() in ("true", "yes", "on", "1")
        delta = datetime.timedelta(days=day_delta, minutes=minute_delta)
        self.accessor.move_datetime(uid, delta, all_day=all_day)

    @expose()
    def event_resize(self, uid, day_delta, minute_delta):
        LOG.info("event_resize, locals={0}".format(pprint.pformat(locals())))
        day_delta = int(day_delta)
        minute_delta = int(minute_delta)
        delta = datetime.timedelta(days=day_delta, minutes=minute_delta)
        self.accessor.increase_duration(uid, delta)
