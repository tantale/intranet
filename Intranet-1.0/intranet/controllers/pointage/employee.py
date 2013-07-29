# -*- coding: utf-8 -*-
"""
:module: intranet.controllers.pointage.employee
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.lib.base import BaseController
from intranet.model import DBSession
from intranet.model.file_storage import FileStorage
from intranet.model.pointage.employee import Employee
from pylons.controllers.util import redirect
from sqlalchemy.exc import IntegrityError
from tg import expose
from tg.decorators import with_trailing_slash
from tg.flash import flash
import datetime
import logging
import os
import tg
import transaction


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


def parse_date(field_name, field_value, date_fmt="%Y-%m-%d"):
    try:
        return datetime.datetime.strptime(field_value, date_fmt)
    except ValueError as cause:
        LOG.error(cause)
        msg_fmt = (u"Champ « {name} » invalide ! "
                   u"La valeur {value} n’est pas une date.")
        raise InvalidFieldError(msg_fmt.format(name=field_name,
                                               value=field_value))


def parse_date_interval(field_name1, field_value1, field_name2, field_value2,
                        date_fmt="%Y-%m-%d"):
    date1 = parse_date(field_name1, field_value1, date_fmt)
    date2 = parse_date(field_name2, field_value2, date_fmt)
    if date1 >= date2:
        msg_fmt = (u"Intervalle de dates invalide ! "
                   u"La date « {name1} » {value1:%d/%m/%Y} "
                   u"doit être antérieure à "
                   u"la date « {name2} »{value2:%d/%m/%Y}.")
        raise InvalidFieldError(msg_fmt.format(name1=field_name1,
                                               value1=field_value1,
                                               name2=field_name2,
                                               value2=field_value2))
    return (date1, date2)


class EmployeeController(BaseController):
    """
    Create / Modify / Remove Employees
    """

    @with_trailing_slash
    @expose('intranet.templates.pointage.employee')
    @expose('json')
    def index(self, uid=None):
        employee_list = (DBSession.query(Employee)
                         .order_by(Employee.employee_name)
                         .all())
        if uid:
            curr_employee = DBSession.query(Employee).get(int(uid))
        else:
            curr_employee = employee_list[0] if employee_list else None
        return dict(curr_employee=curr_employee,
                    employee_list=employee_list)

    @expose('intranet.templates.pointage.employee')
    def delete(self, uid):
        curr_employee = DBSession.query(Employee).get(int(uid))

        if LOG.isEnabledFor(logging.DEBUG):
            msg_fmt = ("delete: uid={uid!r}")
            LOG.debug(msg_fmt.format(uid=uid))

        DBSession.delete(curr_employee)
        transaction.commit()

        employee_list = (DBSession.query(Employee)
                         .order_by(Employee.employee_name)
                         .all())
        curr_employee = employee_list[0] if employee_list else None
        return dict(curr_employee=curr_employee,
                    employee_list=employee_list)

    @expose('intranet.templates.pointage.employee')
    def create(self, employee_name, worked_hours, entry_date,
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

            try:
                employee = Employee(employee_name, worked_hours, entry_date,
                                    exit_date, photo_path=None)
                DBSession.add(employee)
                transaction.commit()
            except IntegrityError as cause:
                LOG.error(cause)
                transaction.abort()
                msg_fmt = (u"Nom de l’employé en doublon ! "
                           u"Le nom « {value} » existe déjà.")
                raise InvalidFieldError(msg_fmt.format(value=employee_name))

        except InvalidFieldError as exc:
            flash(exc.message, status="error")
            redirect(".")

        curr_employee = (DBSession.query(Employee)
                         .filter(Employee.employee_name == employee_name)
                         .one())

        if photo_path is not None:
            photo_storage = photo_path  # FieldStorage

            # -- upload photo file (@see: FieldStorage)
            relpath_fmt = "pointage/employee/employee_{uid}{ext}"
            ext = os.path.splitext(photo_storage.filename)[1]
            relpath = relpath_fmt.format(uid=curr_employee.uid, ext=ext)
            file_storage = FileStorage(tg.config.file_storage_dir)
            if LOG.isEnabledFor(logging.DEBUG):
                msg_fmt = "Store the photo to: '{relpath}'"
                LOG.debug(msg_fmt.format(relpath=relpath))
            file_storage[relpath] = photo_storage.file.read()

            # -- update photo path in current employee
            image_url = "/file_storage/{relpath}".format(relpath=relpath)
            if LOG.isEnabledFor(logging.DEBUG):
                msg_fmt = "Set the image's URL to: '{image_url}'"
                LOG.debug(msg_fmt.format(image_url=image_url))
            curr_employee.photo_path = image_url
            transaction.commit()

        redirect('./?uid=' + curr_employee.uid)
