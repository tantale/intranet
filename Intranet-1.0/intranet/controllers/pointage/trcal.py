# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.trcal
:date: 2013-08-29
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import calendar
import datetime
import json
import logging

import pylons
from formencode.validators import Int, Number
from sqlalchemy.sql.expression import or_, and_, desc
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate, without_trailing_slash
from tg.flash import flash

from intranet.accessors.pointage.cal_event import CalEventAccessor
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.pointage.order import OrderAccessor
from intranet.accessors.pointage.order_phase import OrderPhaseAccessor
from intranet.controllers.session_obj.curr_user import CurrUserController
from intranet.controllers.session_obj.full_calendar import FullCalendarController
from intranet.controllers.session_obj.layout import LayoutController
from intranet.model.pointage.cal_event import CalEvent
from intranet.model.pointage.order import Order
from intranet.validators.iso_date_converter import IsoDatetimeConverter

LOG = logging.getLogger(__name__)


def add_months(start_date, months):
    month = start_date.month - 1 + months
    year = start_date.year + month / 12
    month = month % 12 + 1
    day = min(start_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


# noinspection PyComparisonWithNone
def overlap_cond(ref_start, ref_end, field_start, field_end):
    """
    Construct a sqlalchemy's predicate to check if two date intervals overlap.

    :param ref_start: reference interval start date

    :param ref_end: reference interval end date

    :param field_start: field interval start date

    :param field_end: field interval end date, or None for eternity

    :return: ref_start <= field_start < ref_end or
             field_start <= ref_start < field_end
    """
    return or_(and_(field_start >= ref_start,
                    field_start < ref_end),
               and_(field_start <= ref_start,
                    or_(field_end == None, field_end > ref_start)))


def get_event_duration(event):
    delta = event.event_end - event.event_start
    return delta.seconds / 3600.0


def get_ctrl_status(duration_total, worked_hours):
    if duration_total == 0:
        message = u"Aucun pointage pour cette semaine."
        status = "info"
        icon = "ui-icon-info"
    elif duration_total > worked_hours:
        msg_fmt = u"Le pointage de la semaine dépasse le temps " \
                  u"de travail de {hours} h/sem. " \
                  u"il y a un excédant de {exceeding} h."
        message = msg_fmt.format(hours=worked_hours,
                                 exceeding=duration_total - worked_hours)
        status = "warning"
        icon = "ui-icon-alert"
    elif duration_total < worked_hours:
        msg_fmt = u"Le pointage de la semaine n’atteint pas le temps " \
                  u"de travail de {hours} h/sem. " \
                  u"il y a un déficit de {missing} h."
        message = msg_fmt.format(hours=worked_hours,
                                 missing=worked_hours - duration_total)
        status = "error"
        icon = "ui-icon-alert"
    else:
        message = u"Le pointage de la semaine est correct."
        status = "ok"
        icon = "ui-icon-check"
    return dict(message=message, status=status, icon=icon)


class CalendarController(RestController):
    """
    Calendar controller.

    .. versionchanged:: 1.4.0
        Add layout controller to memorize the position of the left frame.
        Add full_calendar controller to memorize the date and selected view.
        Add curr_user controller to memorize the current user.
    """
    layout = LayoutController("trcal")
    full_calendar = FullCalendarController("trcal")
    curr_user = CurrUserController("pointage")

    def __init__(self, main_menu):
        self.main_menu = main_menu
        self.cal_event_accessor = CalEventAccessor()
        self.order_accessor = OrderAccessor()
        self.order_phase_accessor = OrderPhaseAccessor()
        self.employee_accessor = EmployeeAccessor()

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('intranet.templates.pointage.trcal.index')
    def index(self):
        """
        Display the index page.
        """
        LOG.info("CalendarController.index")
        return dict(main_menu=self.main_menu)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.trcal.order_get_all')
    def order_get_all(self, cal_start, cal_end, keyword=None, uid=None):
        """
        Display all orders for the given time interval.

        GET /pointage/trcal/order_get_all
        GET /pointage/trcal/order_get_all.json
        GET /admin/trcal/order_get_all.json?uid=&
                                            keyword=&
                                            cal_start=1388358000&
                                            cal_end=1391986800

        :param cal_start: start date/time of the calendar interval (timestamps)

        :param cal_end: end date/time of the calendar interval (timestamps)

        :param keyword: current keyword from the search form.

        :param uid: Active order's UID if any
        """
        LOG.info("order_get_all")
        LOG.debug("- cal_start: {!r}".format(cal_start))
        LOG.debug("- cal_end:   {!r}".format(cal_end))
        LOG.debug("- keyword:   {!r}".format(keyword))
        LOG.debug("- uid:       {!r}".format(uid))

        # -- date interval from the calendar's timestamps
        start_date = datetime.datetime.utcfromtimestamp(float(cal_start))
        end_date = datetime.datetime.utcfromtimestamp(float(cal_end))
        LOG.debug(("date interval from the calendar's timestamps: "
                   "[{start_date} ; {end_date}]")
                  .format(start_date=start_date,
                          end_date=end_date))

        # -- filter the order list/keyword currently open
        filter_cond = overlap_cond(start_date, end_date,
                                   Order.creation_date, Order.close_date)
        if keyword:
            filter_cond = and_(filter_cond,
                               Order.order_ref.like('%' + keyword + '%'))
        order_by_cond = desc(Order.creation_date)
        order_list = self.order_accessor.get_order_list(filter_cond, order_by_cond)

        # -- active_index of the order by uid
        active_index = False
        if uid:
            uid = int(uid)
            for index, order in enumerate(order_list):
                if order.uid == uid:
                    active_index = index
                    break
        return dict(order_list=order_list, keyword=keyword,
                    active_index=active_index)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose()
    def get_one(self,
                uid=None,
                employee_uid=None,
                order_phase_uid=None,
                event_start=None):
        """
        Display one record.

        GET /pointage/trcal/1

        :param uid: UID of the calendar event to display.
        :param employee_uid: UID of the employee
        :param order_phase_uid: UID of the OrderPhase
        :param event_start: Start date and time of the event (ISO 8601 string).
        """
        LOG.info("CalendarController.get_one")
        LOG.debug("- uid:             {!r}".format(uid))
        LOG.debug("- employee_uid:    {!r}".format(employee_uid))
        LOG.debug("- order_phase_uid: {!r}".format(order_phase_uid))
        LOG.debug("- event_start:     {!r}".format(event_start))

        if uid:
            cal_event = self.cal_event_accessor.get_cal_event(uid)
        else:
            employee_uid = int(employee_uid)
            order_phase_uid = int(order_phase_uid)
            event_start = datetime.datetime.strptime(event_start, "%Y-%m-%d %H:%M:%S")  # @IgnorePep8
            filter_cond = and_(CalEvent.employee_uid == employee_uid,
                               CalEvent.order_phase_uid == order_phase_uid,
                               CalEvent.event_start == event_start)
            cal_event_list = self.cal_event_accessor.get_cal_event_list(filter_cond)
            cal_event = cal_event_list[0]
        return json.dumps(cal_event.event_obj())

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.trcal.employee_get_all')
    def employee_get_all(self, cal_start, cal_end, cal_curr, employee_uid):
        """
        Display all employees for the given time interval.

        GET /admin/trcal/employee_get_all.json?cal_start=1388530800&
                                               cal_end=1391209200&
                                               cal_curr=1390655265

        :param cal_start: start date/time of the calendar interval (timestamps)

        :param cal_end: end date/time of the calendar interval (timestamps)

        :param cal_curr: current date/time of the calendar (timestamps)

        :param employee_uid: Current employee uid's UID
        """
        LOG.info("employee_get_all")
        LOG.debug("- cal_start:    {!r}".format(cal_start))
        LOG.debug("- cal_end:      {!r}".format(cal_end))
        LOG.debug("- cal_curr:     {!r}".format(cal_curr))
        LOG.debug("- employee_uid: {!r}".format(employee_uid))

        # -- date interval from the calendar's timestamps
        start_date = datetime.datetime.utcfromtimestamp(float(cal_start))
        end_date = datetime.datetime.utcfromtimestamp(float(cal_end))
        LOG.debug(("date interval from the calendar's timestamps: "
                   "[{start_date} ; {end_date}]")
                  .format(start_date=start_date,
                          end_date=end_date))

        # -- employees currently working
        employee_list = self.employee_accessor.get_active_employees(start_date, end_date)

        # -- current employee, if any
        employee_uid = int(employee_uid) if employee_uid else 0
        if employee_uid:
            employee = self.employee_accessor.get_employee(employee_uid)
            if employee not in employee_list:
                employee = None
                err_msg = u"Aucun employée n'est en activité."
                LOG.warning(err_msg)
                self.curr_user.put(uid=0)
            else:
                err_msg = (u"Employé {name} sélectionné."
                           .format(name=employee.employee_name))
                LOG.info(err_msg)
                self.curr_user.put(uid=employee.uid)
        elif len(employee_list):
            curr_uid = self.curr_user.get_all()["uid"]
            for employee in employee_list:
                if employee.uid == curr_uid:
                    break
            else:
                employee = employee_list[0]
                self.curr_user.put(uid=employee.uid)
            err_msg = (u"Employé {name} trouvé."
                       .format(name=employee.employee_name))
            LOG.info(err_msg)
        else:
            employee = None
            err_msg = u"Aucun employée n'est en activité."
            LOG.warning(err_msg)
            self.curr_user.put(uid=0)

        return dict(cal_start=cal_start,
                    cal_end=cal_end,
                    cal_curr=cal_curr,
                    employee=employee,
                    employee_list=employee_list)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.trcal.get_all')
    def get_all(self, cal_start, cal_end, employee_uid=None):
        """
        Display all employees for the given time interval.

        GET /admin/trcal/get_all.json?cal_start=1388530800&
                                      cal_end=1391209200&

        :param cal_start: start date/time of the calendar interval (timestamps)

        :param cal_end: end date/time of the calendar interval (timestamps)

        :param employee_uid: Current employee uid's UID
        """
        LOG.info("get_all")
        LOG.debug("- cal_start:    {!r}".format(cal_start))
        LOG.debug("- cal_end:      {!r}".format(cal_end))
        LOG.debug("- employee_uid: {!r}".format(employee_uid))

        # -- date interval from the calendar's timestamps
        start_date = datetime.datetime.utcfromtimestamp(float(cal_start))
        end_date = datetime.datetime.utcfromtimestamp(float(cal_end))
        LOG.debug(("date interval from the calendar's timestamps: "
                   "[{start_date} ; {end_date}]")
                  .format(start_date=start_date,
                          end_date=end_date))

        # -- employees currently working
        employee_list = self.employee_accessor.get_active_employees(start_date, end_date)

        # -- current employee, if any
        employee_uid = int(employee_uid) if employee_uid else 0
        if employee_uid:
            employee = self.employee_accessor.get_employee(employee_uid)
            if employee not in employee_list:
                employee = None
                err_msg = u"Aucun employée n'est en activité."
                LOG.warning(err_msg)
                self.curr_user.put(uid=0)
            else:
                err_msg = (u"Employé {name} sélectionné."
                           .format(name=employee.employee_name))
                LOG.info(err_msg)
                self.curr_user.put(uid=employee.uid)
        elif len(employee_list):
            curr_uid = self.curr_user.get_all()["uid"]
            for employee in employee_list:
                if employee.uid == curr_uid:
                    break
            else:
                employee = employee_list[0]
                self.curr_user.put(uid=employee.uid)
            err_msg = (u"Employé {name} trouvé."
                       .format(name=employee.employee_name))
            LOG.info(err_msg)
        else:
            employee = None
            err_msg = u"Aucun employée n'est en activité."
            LOG.warning(err_msg)
            self.curr_user.put(uid=0)

        return dict(cal_start=cal_start,
                    cal_end=cal_end,
                    employee=employee,
                    employee_list=employee_list)

    # noinspection PyUnusedLocal
    @expose()
    def events(self, employee_uid, start, end, **kw):
        """
        Generate the events list as a JSON object.

        GET /pointage/trcal/events?employee_uid=&start_date=&end_date=
        @see: http://arshaw.com/fullcalendar/docs/event_data/events_json_feed/

        :param employee_uid: Current employee uid's UID
        :param start: Start date (UTC timestamp).
        :param end: End date (UTC timestamp).
        :param kw: extra parameters (not used).
        """
        LOG.info("CalendarController.events")
        LOG.debug("- employee_uid: {!r}".format(employee_uid))
        LOG.debug("- start:        {!r}".format(start))
        LOG.debug("- end:          {!r}".format(end))

        # -- date interval from the calendar's timestamps
        start_date = datetime.datetime.utcfromtimestamp(float(start))
        end_date = datetime.datetime.utcfromtimestamp(float(end))
        LOG.debug(("date interval from the calendar's timestamps: "
                   "[{start_date} ; {end_date}]")
                  .format(start_date=start_date,
                          end_date=end_date))

        # -- current employee
        employee = self.employee_accessor.get_employee(employee_uid)

        # -- current events of the current employee
        cal_overlap_cond = overlap_cond(start_date, end_date,
                                        CalEvent.event_start,
                                        CalEvent.event_end)
        cal_filter_cond = and_(CalEvent.employee == employee,
                               cal_overlap_cond)
        cal_order_by_cond = CalEvent.event_start
        cal_event_list = self.cal_event_accessor.get_cal_event_list(cal_filter_cond,
                                                                    cal_order_by_cond)

        return json.dumps([cal_event.event_obj()
                           for cal_event in cal_event_list])

    @expose()
    def event_resize(self, uid, day_delta, minute_delta):
        LOG.info("CalendarController.event_resize")
        LOG.debug("- uid:          {!r}".format(uid))
        LOG.debug("- day_delta:    {!r}".format(day_delta))
        LOG.debug("- minute_delta: {!r}".format(minute_delta))
        day_delta = int(day_delta)
        minute_delta = int(minute_delta)
        if day_delta:
            self.cal_event_accessor.divide_event(uid, day_delta)
        else:
            delta = datetime.timedelta(minutes=minute_delta)
            self.cal_event_accessor.increase_duration(uid, delta)

    @expose()
    def event_drop(self, uid, day_delta, minute_delta):
        LOG.info("CalendarController.event_drop")
        LOG.debug("- uid:          {!r}".format(uid))
        LOG.debug("- day_delta:    {!r}".format(day_delta))
        LOG.debug("- minute_delta: {!r}".format(minute_delta))
        day_delta = int(day_delta)
        minute_delta = int(minute_delta)
        delta = datetime.timedelta(days=day_delta,
                                   minutes=minute_delta)
        self.cal_event_accessor.move_datetime(uid, delta)

    @expose('intranet.templates.pointage.trcal.new')
    def new(self, employee_uid, order_phase_uid, tz_offset, **kw):
        """
        Display a page to prompt the User for resource creation:

        GET /pointage/trcal/new?employee_uid=&order_phase_uid=

        :param employee_uid: Current employee uid's UID
        :param order_phase_uid: Current order phase uid's UID
        :param tz_offset: Timezone offset from UTC in minutes (tz_offset = utc_date - local_date).
        """
        LOG.info("CalendarController.new")
        LOG.debug("- employee_uid:     {!r}".format(employee_uid))
        LOG.debug("- order_phase_uid:  {!r}".format(order_phase_uid))
        LOG.debug("- tz_offset:        {!r}".format(tz_offset))

        if 'date' in kw and 'allDay' in kw:
            # -- [A]: receive parameters from open_new_event_dialog in get_all
            # :param date: JavaScript date in ISO 8601 format (UTC date/time)
            # :param allDay: JavaScript boolean value: "true" or "false"
            LOG.debug("- date:             {!r}".format(kw.get('date')))
            LOG.debug("- allDay:           {!r}".format(kw.get('allDay')))
            iso_fmt = "%Y-%m-%dT%H:%M:%S.000Z"  # ignore trailing milliseconds
            datetime_utc = datetime.datetime.strptime(kw.pop('date'), iso_fmt)
            all_day = kw.pop('allDay') == 'true'
            tz_delta = datetime.timedelta(minutes=int(tz_offset))
            if all_day:
                # -- find the best interval in available work hours
                local_datetime = datetime_utc - tz_delta
                local_day = local_datetime.date()
                start_utc, end_utc = self.cal_event_accessor.get_event_interval(employee_uid,
                                                                                local_day,
                                                                                tz_delta)
                event_start = start_utc - tz_delta
                delta = end_utc - start_utc
                kw['event_start'] = event_start.isoformat()
                kw['event_duration'] = delta.seconds / 3600.0
                kw['comment'] = None
            else:
                # -- find an optimized duration in available work hours
                local_datetime = datetime_utc - tz_delta
                local_day = local_datetime.date()
                local_time = local_datetime.time()
                delta = self.cal_event_accessor.get_event_duration(employee_uid,
                                                                   local_day,
                                                                   tz_delta,
                                                                   local_time)
                kw['event_start'] = local_datetime.isoformat()
                kw['event_duration'] = delta.seconds / 3600.0
                kw['comment'] = None

        elif 'event_start' in kw and 'event_duration' in kw:
            # -- [B]: receive parameters from post() method for error handling
            # :param event_start: date in ISO 8601 format (local date/time)
            # :param event_duration: duration (in hour number)
            # :param comment: optional comment (200 characters)
            LOG.debug("- event_start:      {!r}".format(kw.get('event_start')))
            LOG.debug("- event_duration:   {!r}".format(kw.get('event_duration')))  # @IgnorePep8
            LOG.debug("- comment:          {!r}".format(kw.get('comment')))

        else:
            raise NotImplementedError("Unknown arguments: {!r}".format(kw))

        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        LOG.debug("form_errors: {}".format(form_errors))
        if form_errors:
            err_msg = u"Le formulaire comporte des champs invalides"
            flash(err_msg, status="error")
        employee = self.employee_accessor.get_employee(employee_uid)
        order_phase = self.order_phase_accessor.get_order_phase(order_phase_uid)
        return dict(tz_offset=tz_offset,
                    employee=employee, order_phase=order_phase,
                    values=kw, form_errors=form_errors)

    # noinspection PyUnusedLocal
    @validate({'employee_uid': Int(min=0, not_empty=True),
               'order_phase_uid': Int(min=0, not_empty=True),
               'tz_offset': Int(min=-1200, max=1200, not_empty=True),
               'event_start': IsoDatetimeConverter(),
               'event_duration': Number(min=0.25, max=12, not_empty=True)},
              error_handler=new)
    @expose()
    def post(self, employee_uid, order_phase_uid, tz_offset,
             event_start, event_duration, comment, **kw):
        """

        Create a new record.

        POST /pointage/trcal/

        :param employee_uid: Current employee uid's UID
        :param order_phase_uid: Current order phase uid's UID
        :param tz_offset: Timezone offset from UTC in minutes (tz_offset = utc_date - local_date).
        :param event_start: Start date of the event (ISO 8601 string).
        :param event_duration: Event duration in hours.
        :param comment: Event comment.
        :param kw: extra parameters (not used).
        """
        LOG.info("CalendarController.post")
        LOG.debug("- employee_uid:     {!r}".format(employee_uid))
        LOG.debug("- order_phase_uid:  {!r}".format(order_phase_uid))
        LOG.debug("- tz_offset:        {!r}".format(tz_offset))
        LOG.debug("- event_start:      {!r}".format(event_start))
        LOG.debug("- event_duration:   {!r}".format(event_duration))
        LOG.debug("- comment:          {!r}".format(comment))

        # -- convert parameters
        tz_delta = datetime.timedelta(minutes=tz_offset)
        event_start_utc = event_start + tz_delta
        delta = datetime.timedelta(hours=float(event_duration))
        event_end_utc = event_start_utc + delta
        LOG.debug("- event_start_utc:  {!r}".format(event_start_utc))
        LOG.debug("- event_end_utc:    {!r}".format(event_end_utc))

        # -- check overlapping dates in other events of the current employee
        employee = self.employee_accessor.get_employee(employee_uid)
        cal_overlap_cond = overlap_cond(event_start_utc, event_end_utc,
                                        CalEvent.event_start,
                                        CalEvent.event_end)
        cal_filter_cond = and_(CalEvent.employee == employee,
                               cal_overlap_cond)
        cal_order_by_cond = CalEvent.event_start
        cal_event_list = self.cal_event_accessor.get_cal_event_list(cal_filter_cond,
                                                                    cal_order_by_cond)
        if cal_event_list:
            err_msg = (u"Ce pointage intercepte un pointage existant. "
                       u"Veuillez changer la date/heure ou ajuster la durée.")
            flash(err_msg, status="error")
            redirect('./new',
                     employee_uid=employee_uid,
                     order_phase_uid=order_phase_uid,
                     tz_offset=tz_offset,
                     event_start=event_start.isoformat(),
                     event_duration=event_duration,
                     comment=comment)

        # -- insert event in database
        self.cal_event_accessor.insert_cal_event(employee_uid, order_phase_uid,
                                                 event_start_utc,
                                                 event_end_utc, comment)

        # -- return the newly created event
        redirect('./get_one',
                 employee_uid=employee_uid,
                 order_phase_uid=order_phase_uid,
                 event_start=event_start_utc)

    @expose('intranet.templates.pointage.trcal.edit')
    def edit(self, uid, tz_offset, **kw):
        """
        Display a page to prompt the User for resource modification.

        GET /pointage/trcal/1/?uid

        :param uid: UID of the CalEvent to update
        :param tz_offset: Timezone offset from UTC in minutes (tz_offset = utc_date - local_date).
        """
        LOG.info("CalendarController.edit")
        LOG.debug("- uid:              {!r}".format(uid))
        LOG.debug("- tz_offset:        {!r}".format(tz_offset))

        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        cal_event = self.cal_event_accessor.get_cal_event(uid)
        tz_delta = datetime.timedelta(minutes=int(tz_offset))
        event_start = cal_event.event_start - tz_delta
        delta = cal_event.event_end - cal_event.event_start
        event_duration = delta.seconds / 3600.0
        values = dict(uid=cal_event.uid,
                      event_start=event_start.isoformat(),
                      event_duration=event_duration,
                      comment=cal_event.comment)
        values.update(kw)
        LOG.debug("- values:           {!r}".format(values))
        return dict(tz_offset=tz_offset,
                    values=values,
                    employee=cal_event.employee,
                    order_phase=cal_event.order_phase,
                    form_errors=form_errors)

    # noinspection PyUnusedLocal
    @validate({'uid': Int(min=0, not_empty=True),
               'tz_offset': Int(min=-1200, max=1200, not_empty=True),
               'event_start': IsoDatetimeConverter(),
               'event_duration': Number(min=0.25, max=12, not_empty=True)},
              error_handler=edit)
    @expose()
    def put(self, uid, tz_offset, event_start, event_duration, comment, **kw):
        """
        Update an existing record.

        POST /pointage/trcal/1?_method=PUT
        PUT /pointage/trcal/1

        :param uid: UID of the CalEvent to update
        :param tz_offset: Timezone offset from UTC in minutes (tz_offset = utc_date - local_date).
        :param event_start: Start date of the event (ISO 8601 string).
        :param event_duration: Event duration in hours.
        :param comment: Event comment.
        :param kw: extra parameters (not used)
        """
        LOG.info("CalendarController.put")
        LOG.debug("- uid:              {!r}".format(uid))
        LOG.debug("- tz_offset:        {!r}".format(tz_offset))
        LOG.debug("- event_start:      {!r}".format(event_start))
        LOG.debug("- event_duration:   {!r}".format(event_duration))
        LOG.debug("- comment:          {!r}".format(comment))

        # -- convert parameters
        tz_delta = datetime.timedelta(minutes=tz_offset)
        event_start_utc = event_start + tz_delta
        delta = datetime.timedelta(hours=float(event_duration))
        event_end_utc = event_start_utc + delta
        LOG.debug("- event_start_utc:  {!r}".format(event_start_utc))
        LOG.debug("- event_end_utc:    {!r}".format(event_end_utc))

        # -- update the event's duration and comment
        self.cal_event_accessor.update_cal_event(uid,
                                                 event_start=event_start_utc,
                                                 event_end=event_end_utc,
                                                 comment=comment)

        # -- return the updated event
        redirect('./get_one', uid=uid)

    @expose()
    def post_delete(self, uid):
        """
        Delete an existing record.

        POST /pointage/trcal/1?_method=DELETE
        DELETE /pointage/trcal/1

        :param uid: UID of the CalEvent to delete.
        """
        LOG.info("CalendarController.post_delete")
        LOG.debug("- uid: {!r}".format(uid))
        self.cal_event_accessor.delete_cal_event(uid)
        # -- return an event object with it's id only
        return json.dumps(dict(id='cal_event_{uid}'.format(uid=uid)))

    @expose('json')
    @expose('intranet.templates.pointage.trcal.ctrl_rec_times')
    def ctrl_rec_times(self, employee_uid, week_start, week_end, tz_offset, display_messages=False):
        """
        Control recorded/tracked times.

        :param employee_uid: UID of the current employee.
        :param week_start: Start date (UTC timestamp).
        :param week_end: End date (UTC timestamp).
        :param tz_offset: Timezone offset from UTC in minutes (tz_offset = utc_date - local_date).
        :param display_messages:
        """
        LOG.info("CalendarController.ctrl_rec_times")
        LOG.debug("- employee_uid: {!r}".format(employee_uid))
        LOG.debug("- week_start:   {!r}".format(week_start))
        LOG.debug("- week_end:     {!r}".format(week_end))
        LOG.debug("- tz_offset:    {!r}".format(tz_offset))

        # -- convert tz_offset parameter
        tz_offset = int(tz_offset)
        tz_delta = datetime.timedelta(minutes=tz_offset)

        # -- date interval from the calendar's timestamps (UTC dates)
        start_date = datetime.datetime.utcfromtimestamp(float(week_start))
        end_date = datetime.datetime.utcfromtimestamp(float(week_end))
        LOG.debug(("date interval from the calendar's timestamps: "
                   "[{start_date} ; {end_date}]")
                  .format(start_date=start_date,
                          end_date=end_date))

        # -- current employee
        employee = self.employee_accessor.get_employee(employee_uid)

        # -- current events of the current employee
        cal_overlap_cond = overlap_cond(start_date, end_date,
                                        CalEvent.event_start,
                                        CalEvent.event_end)
        cal_filter_cond = and_(CalEvent.employee == employee,
                               cal_overlap_cond)
        cal_order_by_cond = CalEvent.event_start
        cal_event_list = self.cal_event_accessor.get_cal_event_list(cal_filter_cond,
                                                                    cal_order_by_cond)

        # -- count events duration by day and week
        delta = end_date - start_date
        weeks = int(delta.days / 7)

        week_list = []
        for week in xrange(weeks):
            day_list = []
            for day in xrange(7):
                day_start = start_date + datetime.timedelta(days=week * 7 + day)  # @IgnorePep8
                day_end = day_start + datetime.timedelta(days=1)
                event_day_list = [event for event in cal_event_list
                                  if ((day_start <= event.event_start < day_end) or
                                      (event.event_start <= day_start < event.event_end))]
                duration_sum = sum([get_event_duration(event)
                                    for event in event_day_list])
                day_list.append(duration_sum)

            # -- week_date converted in local time
            week_date = start_date + datetime.timedelta(days=week * 7) - tz_delta
            duration_total = sum(day_list)
            week_dict = dict(week_number=week_date.isocalendar()[1],
                             day_list=day_list,
                             duration_total=duration_total)
            week_dict.update(get_ctrl_status(duration_total,
                                             employee.worked_hours))
            week_list.append(week_dict)

        return dict(employee_uid=employee_uid,
                    employee_name=employee.employee_name,
                    worked_hours=employee.worked_hours,
                    week_start=week_start,
                    week_end=week_end,
                    tz_offset=tz_offset,
                    display_messages=display_messages,
                    week_list=week_list)

    @expose('intranet.templates.pointage.trcal.print_rec_times')
    def print_rec_times(self, employee_uid, week_start, week_end, tz_offset):
        return self.ctrl_rec_times(employee_uid, week_start, week_end, tz_offset, display_messages=True)
