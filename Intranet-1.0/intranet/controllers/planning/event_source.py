# -*- coding: utf-8 -*-
import json
import logging
import pprint
import datetime

from formencode.compound import All
from formencode.validators import NotEmpty, Int, MaxLength, StringBool
import pylons
from pylons.i18n import ugettext as _
from tg import expose, flash
from tg.controllers import RestController
from tg.decorators import with_trailing_slash, without_trailing_slash, validate
from tg.controllers.util import redirect
import sqlalchemy.exc
import transaction

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.planning_event import PlanningEventAccessor
from intranet.validators.iso_date_converter import IsoDatetimeConverter

LOG = logging.getLogger(__name__)


# noinspection PyAbstractClass
class PlanningEventController(RestController):
    def _before(self, *args, **kw):
        self.accessor = PlanningEventAccessor()
        self.calendar_accessor = CalendarAccessor()
        url = kw["url"]
        parts = url.split("/")
        # Is it: /admin/planning/sources/1/events
        #    or: /admin/planning/sources/events
        sources_index = parts.index("sources")
        events_index = parts.index("events")
        self.uid = None if sources_index + 1 == events_index else int(parts[sources_index + 1])

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose()
    def get_all(self, start, end, **kwargs):
        LOG.info("get_all: start={start}, end={end}, kwargs={kwargs}".format(start=pprint.pformat(start),
                                                                             end=pprint.pformat(end),
                                                                             kwargs=pprint.pformat(kwargs)))
        calendar = self.calendar_accessor.get_calendar(self.uid)
        result = [event.event_obj() for event in calendar.planning_event_list]
        return json.dumps(result)

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose("intranet.templates.planning.event.new")
    def new(self, tz_offset, **kwargs):
        LOG.info("new, kw = " + pprint.pformat(kwargs))
        # -- Convert UTC date to local time to fill the form
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
        return dict(tz_offset=tz_offset, values=kwargs, form_errors=form_errors,
                    calendar_list=self.calendar_accessor.get_calendar_list())

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
        LOG.info("post, kwargs={0}".format(pprint.pformat(kwargs)))
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


# noinspection PyAbstractClass
class EventSourceController(RestController):
    events = PlanningEventController()

    def _before(self, *args, **kw):
        self.accessor = CalendarAccessor()

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('intranet.templates.planning.event_source')
    def get_all(self):
        # -- find all and filter
        calendar_list = self.accessor.get_calendar_list()
        event_source_list = [calendar.event_source_obj() for calendar in calendar_list]
        for event_source in event_source_list:
            event_source["url"] = "./sources/{id}/events".format(id=event_source["id"])
        return dict(eventSources=json.dumps(event_source_list, indent=True))

    @expose('json')
    def get_one(self, uid):
        calendar = self.accessor.get_calendar(uid)
        event_source = calendar.event_source_obj()
        event_source["url"] = "./sources/{id}/events".format(id=event_source["id"])
        return event_source
