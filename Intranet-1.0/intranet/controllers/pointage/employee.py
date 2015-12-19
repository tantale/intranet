# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.employee
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import logging
import pprint

import pylons
import sqlalchemy.exc
from formencode.validators import NotEmpty, Number, String
from sqlalchemy.sql.expression import or_
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate, without_trailing_slash
from tg.flash import flash

from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.controllers.session_obj.layout import LayoutController
from intranet.model.planning.calendar import Calendar
from intranet.model.pointage.employee import Employee
from intranet.validators.date_interval import check_date_interval
from intranet.validators.iso_date_converter import IsoDateConverter

LOG = logging.getLogger(__name__)


# noinspection PyAbstractClass
class EmployeeController(RestController):
    """
    Create / Modify / Remove Employees

    .. versionchanged:: 1.4.0
        Add layout controller to memorize the position of the left frame.
    """
    layout = LayoutController("employee")

    def __init__(self, main_menu):
        self.main_menu = main_menu

    # noinspection PyUnusedLocal
    def _before(self, *args, **kwargs):
        self.accessor = EmployeeAccessor()
        self.calendar_accessor = self.accessor.calendar_accessor

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('intranet.templates.pointage.employee.index')
    def index(self, uid=None, keyword=None):
        """
        Display the index page.

        :param uid: Employee UID
        :param keyword: Search keyword
        :return: Mako template parameters
        """
        return dict(main_menu=self.main_menu, uid=uid, keyword=keyword)

    # noinspection PyArgumentList
    @without_trailing_slash
    @expose('json')
    def get_one(self, uid):
        """
        Display one employee.

        GET /pointage/employee/1
        GET /pointage/employee/1.json
        GET /pointage/employee/get_one?uid=1
        GET /pointage/employee/get_one.json?uid=1

        :param uid: UID of the employee to display.
        """
        employee = self.accessor.get_employee(uid)
        # noinspection PyComparisonWithNone
        predicate = or_(Calendar.employee_uid == employee.uid, Calendar.employee_uid == None)
        calendar_list = self.calendar_accessor.get_calendar_list(filter_cond=predicate)
        return dict(employee=employee, calendar_list=calendar_list)

    # noinspection PyArgumentList
    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.employee.get_all')
    def get_all(self, uid=None, keyword=None):
        """
        Display all records in a resource.

        GET /pointage/employee/
        GET /pointage/employee.json
        GET /pointage/employee/get_all
        GET /pointage/employee/get_all.json

        :param uid: Active employee UID if any
        :param keyword: Search keyword
        :return: Mako template parameters
        """
        # -- filter the employee list/keyword
        order_by_cond = Employee.employee_name
        filter_cond = (Employee.employee_name.like('%' + keyword + '%')
                       if keyword else None)
        employee_list = self.accessor.get_employee_list(filter_cond, order_by_cond)

        # -- active_index of the employee by uid
        active_index = False
        if uid:
            uid = int(uid)
            for index, employee in enumerate(employee_list):
                if employee.uid == uid:
                    active_index = index
                    break
        return dict(employee_list=employee_list,
                    keyword=keyword,
                    active_index=active_index)

    @expose('intranet.templates.pointage.employee.new')
    def new(self, **kwargs):
        """
        Display a page to prompt the User for resource creation:

        GET /pointage/employee/new

        :param kwargs: Extra URL parameters
        :return: Mako template parameters
        """
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = u"Le formulaire comporte des champs invalides"
            flash(err_msg, status="error")
        return dict(values=kwargs, form_errors=form_errors)

    @validate({'employee_name': NotEmpty(),
               'worked_hours': Number(min=1, max=39, not_empty=True),
               'entry_date': IsoDateConverter(not_empty=True),
               'exit_date': IsoDateConverter(not_empty=False),
               'photo_path': String()},
              error_handler=new)
    @expose()
    def post(self, employee_name, worked_hours, entry_date,
             exit_date=None, photo_path=None):
        LOG.info(u"post: " + pprint.pformat(locals()))

        ctrl_dict = check_date_interval(entry_date, exit_date)
        if ctrl_dict['status'] != "ok":
            flash(ctrl_dict['message'], status=ctrl_dict['status'])
            redirect('./new',
                     employee_name=employee_name,
                     worked_hours=worked_hours,
                     entry_date=entry_date,
                     exit_date=exit_date,
                     photo_path=photo_path)

        try:
            self.accessor.insert_employee(employee_name=employee_name,
                                          worked_hours=worked_hours,
                                          entry_date=entry_date,
                                          exit_date=exit_date,
                                          photo_path=photo_path)
        except sqlalchemy.exc.IntegrityError:
            msg_fmt = (u"Nom de l’employé en doublon ! "
                       u"Le nom « {employee_name} » existe déjà.")
            err_msg = msg_fmt.format(employee_name=employee_name)
            flash(err_msg, status="error")
            redirect('./new',
                     employee_name=employee_name,
                     worked_hours=worked_hours,
                     entry_date=entry_date,
                     exit_date=exit_date,
                     photo_path=photo_path)
        else:
            msg_fmt = (u"L’employé « {employee_name} » a été créé "
                       u"dans la base de données avec succès.")
            flash(msg_fmt.format(employee_name=employee_name), status="ok")
            redirect('./new')

    @expose('intranet.templates.pointage.employee.edit')
    def edit(self, uid, **kwargs):
        """
        Display a page to prompt the User for resource modification.

        GET /pointage/employee/1/edit

        :param uid: UID of the Employee to edit
        :param kwargs: Extra URL parameters
        :return: Mako template parameters
        """
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        employee = self.accessor.get_employee(uid)
        entry_date = employee.entry_date.isoformat()
        exit_date = (None if employee.exit_date is None
                     else employee.exit_date.isoformat())
        values = dict(uid=employee.uid,
                      employee_name=employee.employee_name,
                      worked_hours=str(employee.worked_hours),
                      entry_date=entry_date,
                      exit_date=exit_date,
                      photo_path=employee.photo_path,
                      calendar_uid=employee.calendar.uid if employee.calendar else None)
        values.update(kwargs)
        # noinspection PyComparisonWithNone
        predicate = or_(Calendar.employee_uid == employee.uid, Calendar.employee_uid == None)
        calendar_list = self.calendar_accessor.get_calendar_list(filter_cond=predicate)
        return dict(values=values, form_errors=form_errors, calendar_list=calendar_list)

    # noinspection PyUnusedLocal
    @validate({'employee_name': NotEmpty(),
               'worked_hours': Number(min=1, max=39, not_empty=True),
               'entry_date': IsoDateConverter(not_empty=True),
               'exit_date': IsoDateConverter(not_empty=False),
               'photo_path': String(),
               'calendar_uid': Number(min=1, not_empty=False)},
              error_handler=edit)
    @expose()
    def put(self, uid, employee_name, worked_hours, entry_date, exit_date=None,
            photo_path=None, calendar_uid=None, **kwargs):
        """
        Update an existing record.

        POST /pointage/employee/1?_method=PUT
        PUT /pointage/employee/1

        :param uid: Employee UID
        :param employee_name: Employee display name
        :param worked_hours:
        :param entry_date: Entry date of the employee in the firm.
        :param exit_date: Exit date of the employee in the firm.
        :param photo_path: Relative path of the photo image.
        :param calendar_uid: Employee calendar (if any).
        :param kwargs: Extra URL parameters
        :return: Mako template parameters
        """
        LOG.info(u"put: " + pprint.pformat(locals()))
        calendar = self.calendar_accessor.get_calendar(calendar_uid) if calendar_uid else None
        ctrl_dict = check_date_interval(entry_date, exit_date)
        if ctrl_dict['status'] != "ok":
            flash(ctrl_dict['message'], status=ctrl_dict['status'])
            redirect('./{uid}/edit'.format(uid=uid),
                     employee_name=employee_name,
                     worked_hours=worked_hours,
                     entry_date=entry_date,
                     exit_date=exit_date,
                     photo_path=photo_path,
                     calendar_uid=calendar_uid)

        try:
            self.accessor.update_employee(uid,
                                          employee_name=employee_name,
                                          worked_hours=worked_hours,
                                          entry_date=entry_date,
                                          exit_date=exit_date,
                                          photo_path=photo_path,
                                          calendar=calendar)
        except sqlalchemy.exc.IntegrityError:
            msg_fmt = u"L'employé « {employee_name} » existe déjà."
            err_msg = msg_fmt.format(employee_name=employee_name)
            flash(err_msg, status="error")
            redirect('./{uid}/edit'.format(uid=uid),
                     employee_name=employee_name,
                     worked_hours=worked_hours,
                     entry_date=entry_date,
                     exit_date=exit_date,
                     photo_path=photo_path,
                     calendar_uid=calendar_uid)
        else:
            msg_fmt = u"L'employé « {employee_name} » est modifiée."
            flash(msg_fmt.format(employee_name=employee_name), status="ok")
            redirect('./{uid}/edit'.format(uid=uid))

    @expose('intranet.templates.pointage.employee.get_delete')
    def get_delete(self, uid):
        """
        Display a delete Confirmation page.

        GET /pointage/employee/1/delete

        :param uid: UID of the Employee to delete.
        :return: Mako template parameters
        """
        employee = self.accessor.get_employee(uid)
        return dict(employee=employee)

    @expose('intranet.templates.pointage.employee.get_delete')
    def post_delete(self, uid):
        """
        Delete an existing record.

        POST /pointage/employee/1?_method=DELETE
        DELETE /pointage/employee/1

        :param uid: UID of the Employee to delete.
        """
        employee_name = self.accessor.delete_employee(uid)
        msg_fmt = (u"L’employé « {employee_name} » a été supprimé "
                   u"de la base de données avec succès.")
        flash(msg_fmt.format(employee_name=employee_name), status="ok")
        return dict(employee=None)
