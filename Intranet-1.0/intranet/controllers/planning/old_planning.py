# -*- coding: utf-8 -*-
"""
Planning: Event calendar
========================

Date: 2015-05-30

Author: Laurent LAPORTE <tantale.solutions@gmail.com>

.. versionadded:: 1.4.0
    Prepare next release for "planning" topic.
"""
import json
import logging
import collections
import datetime
import time

from tg.i18n import ugettext as _
from tg.controllers.restcontroller import RestController
from tg.decorators import expose, without_trailing_slash, with_trailing_slash, request

from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.controllers.session_obj.full_calendar import FullCalendarController
from intranet.controllers.session_obj.layout import LayoutController
from intranet.controllers.session_obj.users_selection import UsersSelectionController

LOG = logging.getLogger(__name__)


class ResourcesController(RestController):
    users_selections = UsersSelectionController("planning")

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('intranet.templates.pointage.planning.resources')
    def get_all(self):
        # -- find all
        accessor = EmployeeAccessor()
        employee_list = accessor.get_employee_list()

        # -- add selection flag
        selections = self.users_selections.get_all()["selections"]
        for employee in employee_list:
            employee.checked = employee.uid in selections

        # -- Group resources
        group_dict = collections.OrderedDict()
        group_dict[_(u"Employés actifs")] = filter(lambda x: x.exit_date is None, employee_list)
        group_dict[_(u"Hors effectifs")] = filter(lambda x: x.exit_date is not None, employee_list)

        return dict(title_msg=_(u"Employés"),
                    empty_msg=_(u"Aucun employé"),
                    group_dict=group_dict)

    @expose()
    def put(self, uid, checked):
        return self.users_selections.put(uid, checked)


class EventsController(RestController):
    def _before(self, *args, **kw):
        self.user_uid = int(request.url.split('/')[-3])

    @expose()
    def get_all(self, start, end, **kwargs):
        """
        Get the events of the given user.

        http://fullcalendar.io/docs1/event_data/Event_Object/
        """
        import pkg_resources
        import os
        import io

        intranet_path = os.path.dirname(pkg_resources.resource_filename("intranet", "__init__.py"))
        demo_dir = os.path.join(os.path.dirname(intranet_path), "data")
        if not os.path.isdir(demo_dir):
            os.mkdir(demo_dir)
        demo_path = os.path.join(demo_dir, "demo.json")
        if os.path.isfile(demo_path):
            with io.open(demo_path, "r", encoding="utf-8") as fd:
                demo = json.loads(fd.read())
        else:
            demo = dict()

        LOG.debug(u"==> Recherche du calendrier pour le user : {0:d}".format(self.user_uid))
        record_list = demo.get(unicode(self.user_uid), [])

        event_list = [dict(id=record["id"],
                           title=record["title"],
                           allDay=record["allDay"],
                           start=datetime.datetime.strptime(record["start"], "%Y-%m-%dT%H:%M:%S"),
                           end=datetime.datetime.strptime(record["end"], "%Y-%m-%dT%H:%M:%S"))
                      for record in record_list]

        start_date = datetime.datetime.fromtimestamp(int(start))
        end_date = datetime.datetime.fromtimestamp(int(end))

        event_list = filter(lambda x: start_date <= x["end"] and x["start"] <= end_date, event_list)

        timestamp = lambda d: time.mktime((d.year, d.month, d.day,
                                           d.hour, d.minute, d.second,
                                           -1, -1, -1)) + d.microsecond / 1e6
        start_timestamp = timestamp(start_date)
        end_timestamp = timestamp(end_date)

        if not event_list:
            import random

            for count in xrange(random.randint(20, 30)):
                start_event = datetime.datetime.fromtimestamp(random.randint(start_timestamp, end_timestamp))
                end_event = start_event + datetime.timedelta(days=random.random() * 5)
                event = dict(id="event_{user}_{count}".format(user=self.user_uid, count=count),
                             title=random.choice([u"Fabrication meuble bureau",
                                                  u"Fabrication lit",
                                                  u"Fabrication meuble salle de bain",
                                                  u"Fabrication chaises",
                                                  u"Fabrication table",
                                                  u"Fabrication Escalier",
                                                  u"Fabrication étagères",
                                                  u"Finition meuble bureau",
                                                  u"Finition lit",
                                                  u"Finition meuble salle de bain",
                                                  u"Finition chaises",
                                                  u"Finition table",
                                                  u"Finition Escalier",
                                                  u"Finition étagères",
                                                  u"Pose meuble bureau",
                                                  u"Pose lit",
                                                  u"Pose meuble salle de bain",
                                                  u"Pose chaises",
                                                  u"Pose table",
                                                  u"Pose Escalier",
                                                  u"Pose étagères",
                                                  u"Divers atelier",
                                                  u"Absence"]),
                             allDay=False,
                             start=start_event,
                             end=end_event)
                event_list.append(event)

        event_list = [dict(id=event["id"],
                           title=event["title"],
                           allDay=event["allDay"],
                           start=event["start"].isoformat(),
                           end=event["end"].isoformat())
                      for event in event_list]

        LOG.info(event_list)
        # dump a string to avoid JsonEncodeError
        return json.dumps(event_list, indent=True)


class UsersController(RestController):
    events = EventsController()

    @expose('json')
    def get_all(self):
        return dict(title="all users")

    @expose('json')
    def get_one(self, uid):
        uid = int(uid)
        return dict(title="user {uid}".format(uid=uid))


ONE_THIRD = 1.0 / 3.0
ONE_SIXTH = 1.0 / 6.0
TWO_THIRD = 2.0 / 3.0


def hls_to_rgb(h, l, s):
    if s == 0.0:
        return l, l, l
    if l <= 0.5:
        m2 = l * (1.0 + s)
    else:
        m2 = l + s - (l * s)
    m1 = 2.0 * l - m2
    return _v(m1, m2, h + ONE_THIRD), _v(m1, m2, h), _v(m1, m2, h - ONE_THIRD)


def _v(m1, m2, hue):
    hue %= 1.0
    if hue < ONE_SIXTH:
        return m1 + (m2 - m1) * hue * 6.0
    if hue < 0.5:
        return m2
    if hue < TWO_THIRD:
        return m1 + (m2 - m1) * (TWO_THIRD - hue) * 6.0
    return m1


class CalendarController(RestController):
    users_selections = UsersSelectionController("planning")
    users = UsersController()

    def get_event_source(self, uid):
        """
        Return the event source of a given user.

        {
            url: '/myfeed.php', // use the `url` property
            color: 'yellow',    // an option!
            textColor: 'black'  // an option!
        }
        """
        uid = int(uid)
        h, l, s = 1.0 * (uid % 10) / 10, .5, 0.5
        red, green, blue = (int(256 * x) for x in hls_to_rgb(h, l, s))
        return dict(url="./calendar/users/{uid}/events/".format(uid=uid),
                    color="#{red:x}{green:x}{blue:x}".format(red=red, green=green, blue=blue))

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('intranet.templates.pointage.planning.calendar')
    def get_all(self):
        selections = self.users_selections.get_all()["selections"]
        event_source_list = [self.get_event_source(uid) for uid in selections]
        return dict(eventSources=json.dumps(event_source_list, indent=True))


class PlanningController(RestController):
    layout = LayoutController("planning")
    full_calendar = FullCalendarController("planning")
    resources = ResourcesController()
    calendar = CalendarController()

    def __init__(self, main_menu):
        self.main_menu = main_menu

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('intranet.templates.pointage.planning.index')
    def index(self, res=None):
        """
        Display the index page.
        """
        return dict(main_menu=self.main_menu)
