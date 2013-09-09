# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.employee
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.accessors import DuplicateFoundError
from intranet.accessors.employee import EmployeeAccessor
from intranet.model.pointage.employee import Employee
from tg.controllers.restcontroller import RestController
from tg.decorators import with_trailing_slash, expose
from tg.flash import flash
import datetime
import logging


LOG = logging.getLogger(__name__)


class InvalidFieldError(ValueError):
    pass


def parse_text(field_name, field_value):
    if not field_value:
        msg_fmt = (u"Champ « {name} » non renseigné (champ requis) !")
        raise InvalidFieldError(msg_fmt.format(name=field_name))
    return field_value


def parse_integer(field_name, field_value):
    try:
        return int(field_value)
    except ValueError as cause:
        LOG.error(cause)
        msg_fmt = (u"Champ « {name} » invalide ! "
                   u"La valeur {value} n’est pas un nombre.")
        raise InvalidFieldError(msg_fmt.format(name=field_name,
                                               value=field_value))


def parse_date(field_name, field_value):
    date = None
    for date_fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            date = datetime.datetime.strptime(field_value, date_fmt)
            break
        except ValueError as cause:
            LOG.error(cause)
    if date:
        return date
    msg_fmt = (u"Champ « {name} » invalide ! "
               u"La valeur {value} n’est pas une date.")
    raise InvalidFieldError(msg_fmt.format(name=field_name,
                                           value=field_value))


def parse_date_interval(field_name1, field_value1, field_name2, field_value2):
    date1 = parse_date(field_name1, field_value1)
    date2 = parse_date(field_name2, field_value2)
    if date1 >= date2:
        msg_fmt = (u"Intervalle de dates invalide ! "
                   u"La date « {name1} » {value1:%d/%m/%Y} "
                   u"doit être antérieure à "
                   u"la date « {name2} » {value2:%d/%m/%Y}.")
        raise InvalidFieldError(msg_fmt.format(name1=field_name1,
                                               value1=date1,
                                               name2=field_name2,
                                               value2=date2))
    return (date1, date2)


class EmployeeController(RestController):
    """
    Create / Modify / Remove Employees
    """

    @with_trailing_slash
    @expose('intranet.templates.pointage.employee.index')
    @expose('json')
    def index(self):
        accessor = EmployeeAccessor()
        order_by_cond = Employee.employee_name
        employee_list = accessor.get_employee_list(order_by_cond=order_by_cond)
        return dict(employee_list=employee_list)

    @with_trailing_slash
    @expose('intranet.templates.pointage.employee.get_all')
    @expose('json')
    def get_all(self):
        accessor = EmployeeAccessor()
        order_by_cond = Employee.employee_name
        employee_list = accessor.get_employee_list(order_by_cond=order_by_cond)
        return dict(employee_list=employee_list)

    @with_trailing_slash
    @expose('intranet.templates.pointage.employee.get_all')
    @expose('json')
    def search(self, keyword):
        accessor = EmployeeAccessor()
        filter_cond = (Employee.employee_name.like('%' + keyword + '%')
                       if keyword else None)
        order_by_cond = Employee.employee_name
        employee_list = accessor.get_employee_list(filter_cond,
                                                   order_by_cond)
        return dict(employee_list=employee_list)

    @expose('intranet.templates.pointage.employee.new')
    def new(self):
        new_employee = Employee(employee_name=None,
                                worked_hours=None,
                                entry_date=None,
                                exit_date=None,
                                photo_path=None)
        return dict(new_employee=new_employee)

    @expose('intranet.templates.pointage.employee.edit')
    def edit(self, uid):
        accessor = EmployeeAccessor()
        curr_employee = accessor.get_employee(int(uid))
        if curr_employee is None:
            msg_fmt = (u"La sélection n’a donnée aucun résultat : "
                       u"L’identifiant {uid} n’existe pas.")
            flash(msg_fmt.format(uid=uid), status="error")
        return dict(curr_employee=curr_employee)

    @expose('intranet.templates.pointage.employee.edit')
    def put(self, uid, employee_name, worked_hours, entry_date,
                 exit_date=None, photo_path=None):

        if LOG.isEnabledFor(logging.DEBUG):
            msg_fmt = ("update: "
                       "uid={uid!r}, "
                       "employee_name={employee_name!r}, "
                       "worked_hours={worked_hours!r}, "
                       "entry_date={entry_date!r}, "
                       "exit_date={exit_date!r}, "
                       "photo_path={photo_path!r})")
            LOG.debug(msg_fmt.format(uid=uid,
                                     employee_name=employee_name,
                                     worked_hours=worked_hours,
                                     entry_date=entry_date,
                                     exit_date=exit_date,
                                     photo_path=photo_path))

        employee_name_field = u"Nom"
        worked_hours_field = u"h/sem. travaillées"
        entry_date_field = u"Date d’entrée"
        exit_date_field = u"Date de sortie"

        try:
            employee_name = parse_text(employee_name_field, employee_name)
            worked_hours = parse_integer(worked_hours_field, worked_hours)
            if exit_date:
                entry_date, exit_date = parse_date_interval(entry_date_field,
                                                            entry_date,
                                                            exit_date_field,
                                                            exit_date)
            else:
                entry_date = parse_date(entry_date_field, entry_date)
                exit_date = None

            # -- update
            accessor = EmployeeAccessor()
            accessor.update_employee(uid,
                                     employee_name=employee_name,
                                     worked_hours=worked_hours,
                                     entry_date=entry_date,
                                     exit_date=exit_date,
                                     photo_path=photo_path)

        except DuplicateFoundError:
            msg_fmt = (u"Nom de l’employé en doublon ! "
                       u"Le nom « {value} » existe déjà.")
            flash(msg_fmt.format(value=employee_name), status="error")

        except InvalidFieldError as exc:
            flash(exc.message, status="error")

        else:
            msg_fmt = (u"La mise à jour des informations concernant "
                       u"« {employee_name} » est terminée.")
            flash(msg_fmt.format(employee_name=employee_name),
                  status="ok")

        accessor = EmployeeAccessor()
        curr_employee = accessor.get_employee(uid)
        return dict(curr_employee=curr_employee)

    @expose('intranet.templates.pointage.employee.edit')
    def post_delete(self, uid):
        accessor = EmployeeAccessor()
        old_employee = accessor.delete_employee(uid)
        msg_fmt = (u"L’employé « {employee_name} » a été supprimé "
                   u"de la base de données avec succès.")
        flash(msg_fmt.format(employee_name=old_employee.employee_name),
              status="ok")
        return dict(curr_employee=None)

    @expose('intranet.templates.pointage.employee.new')
    def post(self, employee_name, worked_hours, entry_date,
                 exit_date=None, photo_path=None):

        if LOG.isEnabledFor(logging.DEBUG):
            msg_fmt = ("create: "
                       "employee_name={employee_name!r}, "
                       "worked_hours={worked_hours!r}, "
                       "entry_date={entry_date!r}, "
                       "exit_date={exit_date!r}, "
                       "photo_path={photo_path!r})")
            LOG.debug(msg_fmt.format(employee_name=employee_name,
                                     worked_hours=worked_hours,
                                     entry_date=entry_date,
                                     exit_date=exit_date,
                                     photo_path=photo_path))

        employee_name_field = u"Nom"
        worked_hours_field = u"h/sem. travaillées"
        entry_date_field = u"Date d’entrée"
        exit_date_field = u"Date de sortie"

        try:
            employee_name = parse_text(employee_name_field, employee_name)
            worked_hours = parse_integer(worked_hours_field, worked_hours)
            if exit_date:
                entry_date, exit_date = parse_date_interval(entry_date_field,
                                                            entry_date,
                                                            exit_date_field,
                                                            exit_date)
            else:
                entry_date = parse_date(entry_date_field, entry_date)
                exit_date = None

            accessor = EmployeeAccessor()
            accessor.insert_employee(employee_name=employee_name,
                                              worked_hours=worked_hours,
                                              entry_date=entry_date,
                                              exit_date=exit_date,
                                              photo_path=photo_path)

        except DuplicateFoundError:
            msg_fmt = (u"Nom de l’employé en doublon ! "
                       u"Le nom « {value} » existe déjà.")
            flash(msg_fmt.format(value=employee_name), status="error")
            new_employee = Employee(employee_name=employee_name,
                                    worked_hours=worked_hours,
                                    entry_date=entry_date,
                                    exit_date=exit_date,
                                    photo_path=photo_path)
            return dict(new_employee=new_employee)

        except InvalidFieldError as exc:
            flash(exc.message, status="error")
            new_employee = Employee(employee_name=employee_name,
                                    worked_hours=worked_hours,
                                    entry_date=entry_date,
                                    exit_date=exit_date,
                                    photo_path=photo_path)
            return dict(new_employee=new_employee)

        msg_fmt = (u"L’employé « {employee_name} » a été créé "
                   u"dans la base de données avec succès.")
        flash(msg_fmt.format(employee_name=employee_name), status="ok")
        return dict(new_employee=None)
