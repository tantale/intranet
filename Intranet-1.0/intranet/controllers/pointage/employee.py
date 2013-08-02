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
from sqlalchemy.exc import IntegrityError
from tg.decorators import with_trailing_slash, expose
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


class EmployeeController(BaseController):
    """
    Create / Modify / Remove Employees
    """

    @with_trailing_slash
    @expose('intranet.templates.pointage.employee')
    @expose('json')
    def index(self):
        employee_list = (DBSession.query(Employee)
                         .order_by(Employee.employee_name)
                         .all())
        return dict(employee_list=employee_list)

    @expose('intranet.templates.pointage.employee_edit')
    def search(self, keyword):
        curr_employee = (DBSession.query(Employee)
                         .filter(Employee.employee_name == keyword)
                         .first())
        if curr_employee is None:
            if keyword:
                msg_fmt = (u"La recherche n’a donnée aucun résultat : "
                           u"aucun employé ne porte le nom « {keyword} ».")
                flash(msg_fmt.format(keyword=keyword), status="warning")
            else:
                msg = (u"La recherche n’a donnée aucun résultat : "
                       u"le mot-clef est vide (non renseigné).")
                flash(msg, status="warning")
        return dict(curr_employee=curr_employee)

    @expose('intranet.templates.pointage.employee_new')
    def new(self):
        new_employee = Employee(employee_name=None,
                                worked_hours=None,
                                entry_date=None,
                                exit_date=None,
                                photo_path=None)
        msg = u"Veuillez saisir les informations pour créer un nouvel employé."
        flash(msg, status="info")
        return dict(new_employee=new_employee)

    @expose('intranet.templates.pointage.employee_edit')
    def select(self, uid):
        curr_employee = DBSession.query(Employee).get(int(uid))
        if curr_employee is None:
                msg_fmt = (u"La sélection n’a donnée aucun résultat : "
                           u"L’identifiant {uid} n’existe pas.")
                flash(msg_fmt.format(uid=uid), status="error")
        return dict(curr_employee=curr_employee)

    @expose('intranet.templates.pointage.employee_edit')
    def update(self, uid, employee_name, worked_hours, entry_date,
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

            try:
                if isinstance(photo_path, (str, unicode)):
                    photo_storage = None
                else:
                    photo_storage = photo_path  # FieldStorage

                # -- update
                employee = DBSession.query(Employee).get(uid)
                self.delete_photo(employee.photo_path)
                new_photo_path = self.store_photo(employee.uid, photo_storage)
                employee.employee_name = employee_name
                employee.worked_hours = worked_hours
                employee.entry_date = entry_date
                employee.exit_date = exit_date
                employee.photo_path = new_photo_path
                transaction.commit()
            except IntegrityError as cause:
                LOG.error(cause)
                transaction.abort()
                msg_fmt = (u"Nom de l’employé en doublon ! "
                           u"Le nom « {value} » existe déjà.")
                raise InvalidFieldError(msg_fmt.format(value=employee_name))

        except InvalidFieldError as exc:
            flash(exc.message, status="error")
        else:
            msg_fmt = (u"La mise à jour des informations concernant "
                       u"« {employee_name} » est terminée.")
            flash(msg_fmt.format(employee_name=employee_name),
                  status="ok")

        curr_employee = DBSession.query(Employee).get(int(uid))
        return dict(curr_employee=curr_employee)

    @expose('intranet.templates.pointage.employee_edit')
    def delete(self, uid):
        curr_employee = DBSession.query(Employee).get(int(uid))

        if LOG.isEnabledFor(logging.DEBUG):
            msg_fmt = ("delete: uid={uid!r}")
            LOG.debug(msg_fmt.format(uid=uid))

        self.delete_photo(curr_employee.photo_path)
        DBSession.delete(curr_employee)
        transaction.commit()

        msg_fmt = (u"L’employé « {employee_name} » a été supprimé "
                   u"de la base de données avec succès.")
        flash(msg_fmt.format(employee_name=curr_employee.employee_name),
              status="ok")
        return dict(curr_employee=None)

    @expose('intranet.templates.pointage.employee_new')
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
            new_employee = Employee(employee_name=employee_name,
                                    worked_hours=worked_hours,
                                    entry_date=entry_date,
                                    exit_date=exit_date,
                                    photo_path=photo_path)
            return dict(new_employee=new_employee)

        if not isinstance(photo_path, (str, unicode)):
            photo_storage = photo_path  # FieldStorage
            # -- search the employee to get it's uid
            employee = (DBSession.query(Employee)
                        .filter(Employee.employee_name == employee_name)
                        .one())
            # -- update photo path in current employee
            employee.photo_path = self.store_photo(employee.uid, photo_storage)
            transaction.commit()

        msg_fmt = (u"L’employé « {employee_name} » a été créé "
                   u"dans la base de données avec succès.")
        flash(msg_fmt.format(employee_name=employee_name), status="ok")
        return dict(new_employee=None)

    def store_photo(self, uid, photo_storage):
        if photo_storage is None:
            return None
        # -- upload photo file (@see: FieldStorage)
        relpath_fmt = "/photo/pointage/employee/employee_{uid}{ext}"
        ext = os.path.splitext(photo_storage.filename)[1]
        relpath = relpath_fmt.format(uid=uid, ext=ext)
        file_storage = FileStorage(tg.config.file_storage_dir)
        if relpath in file_storage:
            del file_storage[relpath]
        file_storage[relpath] = photo_storage.file.read()
        return relpath

    def delete_photo(self, photo_path):
        if photo_path is None:
            return
        file_storage = FileStorage(tg.config.file_storage_dir)
        if photo_path in file_storage:
            del file_storage[photo_path]
