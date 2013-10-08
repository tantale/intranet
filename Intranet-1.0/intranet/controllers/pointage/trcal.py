# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.trcal
:date: 2013-08-29
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from formencode.validators import NotEmpty, Int
from intranet.accessors.cal_event import CalEventAccessor
from intranet.accessors.order import OrderAccessor
from intranet.model.pointage.cal_event import CalEvent
from intranet.model.pointage.employee import Employee
from intranet.model.pointage.order import Order
from intranet.validators.iso_date_converter import IsoDateConverter, \
    IsoDatetimeConverter
from sqlalchemy.sql.expression import or_, and_
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate
from tg.flash import flash
import calendar
import datetime
import logging
import pylons
import math
import json

LOG = logging.getLogger(__name__)


def month_start(date):
    return date.replace(day=1)


def add_months(start_date, months):
    month = start_date.month - 1 + months
    year = start_date.year + month / 12
    month = month % 12 + 1
    day = min(start_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def overlap_cond(ref_start, ref_end, field_start, field_end):
    """
    Construct a sqlalchemy's predicate to check if two date intervals overlap.

    :param ref_start: reference insterval's start date

    :param ref_end: reference insterval's end date

    :param field_start: field insterval's start date

    :param field_end: field insterval's end date, or None for eternity

    :return: ref_start <= field_start < ref_end or
             field_start <= ref_start < field_end
    """
    return or_(and_(field_start >= ref_start,
                    field_start < ref_end),
               and_(field_start <= ref_start,
                    or_(field_end == None, field_end > ref_start)))


class CalendarController(RestController):
    """
    Calendar controller.
    """

    @with_trailing_slash
    @expose('intranet.templates.pointage.trcal.index')
    def index(self):
        """
        Display the index page.
        """
        return dict()

    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.trcal.order_get_all')
    def order_get_all(self, cal_date=None, keyword=None, uid=None):
        """
        Display all records in a resource.

        GET /pointage/trcal/order_get_all
        GET /pointage/trcal/order_get_all.json

        :param uid: Active order's UID if any
        """
        LOG.info("order_get_all")
        accessor = OrderAccessor()

        # -- date interval from the calendar's date
        cal_date = cal_date or datetime.date.today()
        start_date = month_start(cal_date)
        end_date = add_months(start_date, 1)
        LOG.debug("[{start_date} ; {end_date}]"
                  .format(start_date=start_date,
                          end_date=end_date))

        # -- filter the order list/keyword currently open
        filter_cond = overlap_cond(start_date, end_date,
                                   Order.creation_date, Order.close_date)
        if keyword:
            filter_cond = and_(filter_cond,
                               Order.order_ref.like('%' + keyword + '%'))
        order_by_cond = Order.order_ref
        order_list = accessor.get_order_list(filter_cond, order_by_cond)

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

    @with_trailing_slash
    @expose('json')
    def get_one(self, uid):
        """
        Display one record.

        GET /pointage/trcal/1

        :param uid: UID of the calendar event to display.
        """
        accessor = CalEventAccessor()
        cal_event = accessor.get_cal_event(uid)
        return dict(cal_event=cal_event)

    @with_trailing_slash
    @validate({'cal_date': IsoDateConverter(not_empty=False)})
    @expose('json')
    @expose('intranet.templates.pointage.trcal.get_all')
    def get_all(self, cal_date=None, employee_uid=None):
        """
        Display all records in a resource.

        GET /pointage/trcal/?employee_uid=&cal_date=&date_end=

        :param employee_uid: Current employee uid's UID
        """
        LOG.info("get_all")
        accessor = CalEventAccessor()

        # -- time zone offset for UTC date/time calculation
        utcnow = datetime.datetime.utcnow()
        now = datetime.datetime.now()
        timegm = calendar.timegm(utcnow.utctimetuple())
        utctimegm = calendar.timegm(now.timetuple())
        time_zone_offset = int(math.ceil((timegm - utctimegm) / 36.0))

        # -- date interval from the calendar's date
        cal_date = cal_date or datetime.date.today()
        start_date = month_start(cal_date)
        end_date = add_months(start_date, 1)
        LOG.debug("[{start_date} ; {end_date}]"
                  .format(start_date=start_date,
                          end_date=end_date))

        # -- employees currently working
        filter_cond = overlap_cond(start_date, end_date,
                                   Employee.entry_date, Employee.exit_date)
        order_by_cond = Employee.employee_name
        employee_list = accessor.get_employee_list(filter_cond,
                                                   order_by_cond)

        # -- current employee, if any
        if employee_uid:
            employee = accessor.get_employee(employee_uid)
            err_msg = (u"Employé {name} à la date du {date:%d/%m/%Y}"
                       .format(name=employee.employee_name,
                               date=cal_date))
            LOG.info(err_msg)
        elif len(employee_list):
            employee = employee_list[0]
            err_msg = (u"Employé {name} à la date du {date:%d/%m/%Y}"
                       .format(name=employee.employee_name,
                               date=cal_date))
            LOG.info(err_msg)
        else:
            employee = None
            err_msg = (u"Aucun employée n'est en activité à la date du {date:%d/%m/%Y}"  # @IgnorePep8
                       .format(date=cal_date))
            LOG.warning(err_msg)

        return dict(time_zone_offset=time_zone_offset,
                    cal_date=cal_date,
                    start_date=start_date,
                    end_date=end_date,
                    employee=employee,
                    employee_list=employee_list)

    @expose()
    def events(self, employee_uid, start, end, **kw):
        """
        Generate the events list as a JSON object.

        GET /pointage/trcal/events?employee_uid=&start_date=&end_date=
        @see: http://arshaw.com/fullcalendar/docs/event_data/events_json_feed/

        :param employee_uid: Current employee uid's UID
        """
        LOG.info("CalendarController.events")
        LOG.debug("- employee_uid: {!r}".format(employee_uid))
        LOG.debug("- start:        {!r}".format(start))
        LOG.debug("- end:          {!r}".format(end))

        # -- date interval from the calendar's timestamps
        start_date = datetime.datetime.utcfromtimestamp(float(start))
        end_date = datetime.datetime.utcfromtimestamp(float(end))
        LOG.debug("date interval from the calendar's timestamps: [{start_date} ; {end_date}]"
                  .format(start_date=start_date,
                          end_date=end_date))

        # -- current employee
        accessor = CalEventAccessor()
        employee = accessor.get_employee(employee_uid)

        # -- current events of the current employee
        cal_overlap_cond = overlap_cond(start_date, end_date,
                                        CalEvent.event_start,
                                        CalEvent.event_end)
        cal_filter_cond = and_(CalEvent.employee == employee,
                               cal_overlap_cond)
        cal_order_by_cond = CalEvent.event_start
        cal_event_list = accessor.get_cal_event_list(cal_filter_cond,
                                                     cal_order_by_cond)

        return json.dumps([cal_event.event_obj()
                           for cal_event in cal_event_list])

    @expose('intranet.templates.pointage.trcal.new')
    def new(self, employee_uid, order_phase_uid, time_zone_offset, **kw):
        """
        Display a page to prompt the User for resource creation:

        GET /pointage/trcal/new?employee_uid=&order_phase_uid=

        :param employee_uid: Current employee uid's UID

        :param order_phase_uid: Current order phase uid's UID
        """
        LOG.info("new")
        #    # -- compute default parameters
        #    if 'event_start' not in kw:
        #        event_start = datetime.datetime.now().replace(second=0,
        #                                                      microsecond=0)
        #        kw['event_start'] = event_start.isoformat()
        accessor = CalEventAccessor()
        employee = accessor.get_employee(employee_uid)
        order_phase = accessor.get_order_phase(order_phase_uid)
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        LOG.debug("form_errors: {}".format(form_errors))
        if form_errors:
            err_msg = (u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(time_zone_offset=time_zone_offset,
                    employee=employee, order_phase=order_phase,
                    values=kw, form_errors=form_errors)

    @validate({'employee_uid': Int(min=0, not_empty=True),
               'order_phase_uid': Int(min=0, not_empty=True),
               'time_zone_offset': Int(min=-1200, max=1200, not_empty=True),
               'title': NotEmpty,
               'event_start': IsoDatetimeConverter,
               'event_duration': Int(min=1, max=999, not_empty=True)},
              error_handler=new)
    @expose('json')
    def post(self, employee_uid, order_phase_uid, time_zone_offset,
             title, event_start, event_duration, comment, **kwagrs):
        """
        Create a new record.

        POST /pointage/trcal/

        :param employee_uid: Current employee uid's UID

        :param order_phase_uid: Current order phase uid's UID
        """
        LOG.info("CalendarController.post")
        LOG.debug("- employee_uid:     {!r}".format(employee_uid))
        LOG.debug("- order_phase_uid:  {!r}".format(order_phase_uid))
        LOG.debug("- time_zone_offset: {!r}".format(time_zone_offset))
        LOG.debug("- title:            {!r}".format(title))
        LOG.debug("- event_start:      {!r}".format(event_start))
        LOG.debug("- event_duration:   {!r}".format(event_duration))
        LOG.debug("- comment:          {!r}".format(comment))

        # -- convert parameters
        event_start_utc = event_start + datetime.timedelta(minutes=time_zone_offset)  # @IgnorePep8
        event_end_utc = event_start_utc + datetime.timedelta(hours=float(event_duration) / 100)  # @IgnorePep8
        LOG.debug("- event_start_utc:  {!r}".format(event_start_utc))
        LOG.debug("- event_end_utc:    {!r}".format(event_end_utc))

        # -- insert event in database
        accessor = CalEventAccessor()
        cal_event = accessor.insert_cal_event(employee_uid, order_phase_uid,
                                              title, event_start_utc,
                                              event_end_utc, comment)
        return dict(cal_event=cal_event.event_obj())

    @expose('intranet.templates.pointage.trcal.edit')
    def edit(self, employee_uid, order_phase_uid, uid, **kw):
        """
        Display a page to prompt the User for resource modification.

        GET /pointage/trcal/1/?order_uid

        :param employee_uid: Current employee uid's UID

        :param order_phase_uid: Current order phase uid's UID

        :param uid: UID of the CalEvent to update
        """
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        accessor = CalEventAccessor()
        cal_event = accessor.get_cal_event(uid)
        values = dict(uid=cal_event.uid,
                      title=cal_event.title)
        values.update(kw)
        return dict(employee_uid=employee_uid, order_phase_uid=order_phase_uid,
                    values=values,
                    form_errors=form_errors)

    @validate({'title': NotEmpty}, error_handler=edit)
    @expose()
    def put(self, employee_uid, order_phase_uid, uid, title, **kw):
        """
        Update an existing record.

        POST /pointage/trcal/1?_method=PUT
        PUT /pointage/trcal/1

        :param employee_uid: Current employee uid's UID

        :param order_phase_uid: Current order phase uid's UID

        :param uid: UID of the CalEvent to update

        :param title: the order phase's title (not null)
        """
        accessor = CalEventAccessor()
        accessor.update_cal_event(uid, title=title)
        msg_fmt = (u"La phase de commande « {title} » est modifiée.")
        flash(msg_fmt.format(title=title), status="ok")
        redirect('./{uid}/edit'.format(uid=uid))

    @expose('intranet.templates.pointage.trcal.get_delete')
    def get_delete(self, uid):
        """
        Display a delete Confirmation page.

        GET /pointage/trcal/1/delete

        :param uid: UID of the CalEvent to delete.
        """
        accessor = CalEventAccessor()
        cal_event = accessor.get_cal_event(uid)
        return dict(cal_event=cal_event)

    @expose('intranet.templates.pointage.trcal.get_delete')
    def post_delete(self, uid):
        """
        Delete an existing record.

        POST /pointage/trcal/1?_method=DELETE
        DELETE /pointage/trcal/1

        :param uid: UID of the CalEvent to delete.
        """
        accessor = CalEventAccessor()
        old_cal_event = accessor.delete_cal_event(uid)
        msg_fmt = (u"La phase de commande « {title} » est supprimée.")
        flash(msg_fmt.format(title=old_cal_event.title), status="ok")
        return dict(cal_event=None)
