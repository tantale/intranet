# -*- coding: utf-8 -*-
"""
FullCalendar
============

Date: 2015-05-31

Author: Laurent LAPORTE <tantale.solutions@gmail.com>
"""
from __future__ import unicode_literals
import logging
import datetime

from tg import session
from tg.controllers.restcontroller import RestController
from tg.decorators import expose

from intranet.controllers.session_obj.casting import as_unicode, as_int, as_dict

LOG = logging.getLogger(__name__)


class FullCalendarController(RestController):
    """
    Default properties for FullCalendar, see: http://fullcalendar.io/docs1/

    .. versionadded:: 1.4.0
    """
    CONFIG = dict(
        theme=True,
        editable=True,
        eventStartEditable=True,
        eventDurationEditable=True,
        firstDay=1,
        firstHour=8,
        weekends=True,
        snapMinutes=15,
        slotEventOverlap=True,
        ignoreTimezone=False,
        header={'left': 'month,agendaWeek,agendaDay',
                'center': 'title',
                'right': 'today prev,next'},
        allDayText='Toute la journ\u00e9e',
        axisFormat='H:mm',
        timeFormat={"agenda": 'H:mm{ - H:mm}',
                    '': 'H(:mm)'},
        columnFormat={"month": 'ddd',
                      "week": 'ddd d/M',
                      "day": 'dddd d/M'
                      },
        titleFormat={"month": 'MMMM yyyy',
                     "week": "d[ MMM][ yyyy]{ '&#8212;' d MMM yyyy}",
                     "day": 'dddd d MMM yyyy'
                     },
        monthNames=['Janvier', 'F\u00e9vrier', 'Mars', 'Avril', 'Mai', 'Juin',
                    'Juillet', 'Ao\u00fbt', 'Septembre', 'Octobre', 'Novembre', 'D\u00e9cembre'],
        monthNamesShort=['Jan.', 'F\u00e9v.', 'Mar.', 'Avr.', 'Mai', 'Juin',
                         'Juil.', 'Ao\u00fbt', 'Sept.', 'Oct.', 'Nov.', 'D\u00e9c.'],
        dayNames=['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
        dayNamesShort=['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
        buttonText={"prev": "<span class='fc-text-arrow'>&lsaquo;</span>",
                    "next": "<span class='fc-text-arrow'>&rsaquo;</span>",
                    "prevYear": "<span class='fc-text-arrow'>&laquo;</span>",
                    "nextYear": "<span class='fc-text-arrow'>&raquo;</span>",
                    "today": 'Aujoud\u2019hui',
                    "month": 'mois',
                    "week": 'semaine',
                    "day": 'jour'
                    })

    DEFAULT_PROPERTIES = dict(
        defaultView='month',  # basicWeek, basicDay, agendaWeek, agendaDay
        year=None,
        month=None,
        date=None)

    CAST_MAPPING = dict(
        defaultView=as_unicode,
        year=as_int,
        month=as_int,
        date=as_int)

    def __init__(self, module):
        self.session_var = module + ".full_calendar"

    @property
    def properties(self):
        if self.session_var not in session:
            session[self.session_var] = dict(self.DEFAULT_PROPERTIES)
            session.save()
            LOG.debug("init session[{key}] = {val!r}".format(key=self.session_var, val=session[self.session_var]))
        LOG.debug("get session[{key}] = {val!r}".format(key=self.session_var, val=session[self.session_var]))
        return session[self.session_var]

    @properties.setter
    def properties(self, properties):
        # use: http://127.0.0.1:8080/environ.html to display the cookie session
        session[self.session_var] = properties
        session.save()
        LOG.debug("set session[{key}] = {val!r}".format(key=self.session_var, val=session[self.session_var]))

    @expose('json')
    def get_all(self, timestamp=None):
        timestamp = timestamp and float(timestamp)
        properties = self.properties
        if any(properties.get(k) is None for k in ("year", "month", "date")):
            curr_date = datetime.datetime.utcfromtimestamp(timestamp) if timestamp else datetime.datetime.utcnow()
            properties["year"] = curr_date.year
            properties["month"] = curr_date.month - 1  # in JavaScript: 0 <= month <= 11
            properties["date"] = curr_date.day  # JavaScript date == Python day
        return dict(self.CONFIG, **properties)

    @expose()
    def put(self, **kwargs):
        # with a getter/setter we can't update directly
        casted_kwargs = as_dict(self.CAST_MAPPING, kwargs)
        self.properties = dict(self.properties, **casted_kwargs)

    @expose('json')
    def get_one(self, key):
        """
        Get a property value.

        eg.: http://127.0.0.1:8080/admin/trcal/full_calendar/isodate

        :type key: unicode
        :param key: Name of the property.
        :return: dict(key, value)
        """
        # for debug
        properties = self.properties
        if key == "isodate":
            fmt = "{year:04d}-{month:02d}-{date:02d}"
            return dict(isodate=fmt.format(year=properties["year"],
                                           month=properties["month"] + 1,  # in JavaScript: 0 <= month <= 11
                                           date=properties["date"]))
        return {key: properties[key]}
