# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.employee
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from formencode.validators import NotEmpty, Number
from intranet.accessors import DuplicateFoundError
from intranet.accessors.employee import EmployeeAccessor
from intranet.model.pointage.employee import Employee
from intranet.validators.date_interval import check_date_interval
from intranet.validators.iso_date_converter import IsoDateConverter
from tg.controllers.restcontroller import RestController
from tg.controllers.util import redirect
from tg.decorators import with_trailing_slash, expose, validate, \
    without_trailing_slash
from tg.flash import flash
import logging
import pylons


LOG = logging.getLogger(__name__)


class EmployeeController(RestController):
    """
    Create / Modify / Remove Employees
    """

    def __init__(self, main_menu):
        self.main_menu = main_menu

    @without_trailing_slash
    @expose('intranet.templates.pointage.employee.index')
    def index(self, uid=None, keyword=None):
        """
        Display the index page.
        """
        return dict(main_menu=self.main_menu, uid=uid, keyword=keyword)

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
        accessor = EmployeeAccessor()
        employee = accessor.get_employee(uid)
        return dict(employee=employee)

    @with_trailing_slash
    @expose('json')
    @expose('intranet.templates.pointage.employee.get_all')
    def get_all(self, keyword=None, uid=None):
        """
        Display all records in a resource.

        GET /pointage/employee/
        GET /pointage/employee.json
        GET /pointage/employee/get_all
        GET /pointage/employee/get_all.json

        :param uid: Active employee's UID if any
        """
        # -- filter the employee list/keyword
        accessor = EmployeeAccessor()
        order_by_cond = Employee.employee_name
        filter_cond = (Employee.employee_name.like('%' + keyword + '%')
                       if keyword else None)
        employee_list = accessor.get_employee_list(filter_cond, order_by_cond)

        # -- active_index of the employee by uid
        active_index = False
        if uid:
            uid = int(uid)
            for index, employee in enumerate(employee_list):
                if employee.uid == uid:
                    active_index = index
                    break
        return dict(employee_list=employee_list, keyword=keyword,
                    active_index=active_index)

    @expose('intranet.templates.pointage.employee.new')
    def new(self, **kw):
        """
        Display a page to prompt the User for resource creation:

        GET /pointage/employee/new
        """
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        if form_errors:
            err_msg = (u"Le formulaire comporte des champs invalides")
            flash(err_msg, status="error")
        return dict(values=kw, form_errors=form_errors)

    @validate({'employee_name': NotEmpty(),
               'worked_hours': Number(min=1, max=39, not_empty=True),
               'entry_date': IsoDateConverter(not_empty=True),
               'exit_date': IsoDateConverter(not_empty=False)},
              error_handler=new)
    @expose()
    def post(self, employee_name, worked_hours, entry_date,
                 exit_date=None, photo_path=None):
        LOG.info("EmployeeController.post")
        LOG.debug("- employee_name: {!r}".format(employee_name))
        LOG.debug("- worked_hours:  {!r}".format(worked_hours))
        LOG.debug("- entry_date:    {!r}".format(entry_date))
        LOG.debug("- exit_date:     {!r}".format(exit_date))

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
            accessor = EmployeeAccessor()
            accessor.insert_employee(employee_name=employee_name,
                                              worked_hours=worked_hours,
                                              entry_date=entry_date,
                                              exit_date=exit_date,
                                              photo_path=photo_path)
        except DuplicateFoundError:
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
    def edit(self, uid, **kw):
        """
        Display a page to prompt the User for resource modification.

        GET /pointage/employee/1/edit

        :param uid: UID of the Employee to edit
        """
        form_errors = pylons.tmpl_context.form_errors  # @UndefinedVariable
        accessor = EmployeeAccessor()
        employee = accessor.get_employee(uid)
        entry_date = employee.entry_date.isoformat()
        exit_date = (None if employee.exit_date is None
                     else employee.exit_date.isoformat())
        values = dict(uid=employee.uid,
                      employee_name=employee.employee_name,
                      worked_hours=str(employee.worked_hours),
                      entry_date=entry_date,
                      exit_date=exit_date,
                      photo_path=employee.photo_path)
        values.update(kw)
        return dict(values=values, form_errors=form_errors)

    @validate({'employee_name': NotEmpty(),
               'worked_hours': Number(min=1, max=39, not_empty=True),
               'entry_date': IsoDateConverter(not_empty=True),
               'exit_date': IsoDateConverter(not_empty=False)},
              error_handler=edit)
    @expose()
    def put(self, uid, employee_name, worked_hours, entry_date, exit_date,
            photo_path, **kw):
        """
        Update an existing record.

        POST /pointage/employee/1?_method=PUT
        PUT /pointage/employee/1
        """
        LOG.info("EmployeeController.post")
        LOG.debug("- uid:           {!r}".format(uid))
        LOG.debug("- employee_name: {!r}".format(employee_name))
        LOG.debug("- worked_hours:  {!r}".format(worked_hours))
        LOG.debug("- entry_date:    {!r}".format(entry_date))
        LOG.debug("- exit_date:     {!r}".format(exit_date))

        ctrl_dict = check_date_interval(entry_date, exit_date)
        if ctrl_dict['status'] != "ok":
            flash(ctrl_dict['message'], status=ctrl_dict['status'])
            redirect('./{uid}/edit'.format(uid=uid),
                     employee_name=employee_name,
                     worked_hours=worked_hours,
                     entry_date=entry_date,
                     exit_date=exit_date,
                     photo_path=photo_path)

        try:
            accessor = EmployeeAccessor()
            accessor.update_employee(uid,
                                     employee_name=employee_name,
                                     worked_hours=worked_hours,
                                     entry_date=entry_date,
                                     exit_date=exit_date,
                                     photo_path=photo_path)
        except DuplicateFoundError:
            msg_fmt = (u"L'employé « {employee_name} » existe déjà.")
            err_msg = msg_fmt.format(employee_name=employee_name)
            flash(err_msg, status="error")
            redirect('./{uid}/edit'.format(uid=uid),
                     employee_name=employee_name,
                     worked_hours=worked_hours,
                     entry_date=entry_date,
                     exit_date=exit_date,
                     photo_path=photo_path)
        else:
            msg_fmt = (u"L'employé « {employee_name} » est modifiée.")
            flash(msg_fmt.format(employee_name=employee_name), status="ok")
            redirect('./{uid}/edit'.format(uid=uid))

    @expose('intranet.templates.pointage.employee.get_delete')
    def get_delete(self, uid):
        """
        Display a delete Confirmation page.

        GET /pointage/employee/1/delete

        :param uid: UID of the Employee to delete.
        """
        accessor = EmployeeAccessor()
        employee = accessor.get_employee(uid)
        return dict(employee=employee)

    @expose('intranet.templates.pointage.employee.get_delete')
    def post_delete(self, uid):
        """
        Delete an existing record.

        POST /pointage/employee/1?_method=DELETE
        DELETE /pointage/employee/1

        :param uid: UID of the Employee to delete.
        """
        accessor = EmployeeAccessor()
        old_employee = accessor.delete_employee(uid)
        msg_fmt = (u"L’employé « {employee_name} » a été supprimé "
                   u"de la base de données avec succès.")
        flash(msg_fmt.format(employee_name=old_employee.employee_name),
              status="ok")
        return dict(employee=None)
