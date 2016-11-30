"""
:module: intranet.accessors.employee
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import logging
import os
import time

import tg
import transaction

from intranet.accessors import BasicAccessor
from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor
from intranet.accessors.sql_utils import overlap_cond
from intranet.model.file_storage import FileStorage
from intranet.model.planning.calendar import Calendar
from intranet.model.pointage.employee import Employee

LOG = logging.getLogger(__name__)


class EmployeeAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(EmployeeAccessor, self).__init__(record_class=Employee, session=session)
        self.calendar_accessor = CalendarAccessor(session)
        self.week_hours_accessor = WeekHoursAccessor(session)

    def get_employee(self, uid):
        """
        Get a employee by UID.

        :type uid: int | str | unicode
        :param uid: Employee UID.
        :rtype: Employee
        :return: The matching employee.
        :raise sqlalchemy.orm.exc.NoResultFound: if the record is not found.
        """
        return super(EmployeeAccessor, self)._get_record(uid)

    def get_employee_by_name(self, employee_name):
        """
        Get the first Employee of a given name.

        Useful for testing but not for production because the name may not be unique.

        .. versionadded:: 2.2.0

        :type employee_name: str | unicode
        :param employee_name: Employee name (label).
        :rtype: Employee
        :return: The found Employee.
        :raises: sqlalchemy.orm.exc.NoResultFound
        :raises: sqlalchemy.orm.exc.MultipleResultsFound
        """
        return self.session.query(Employee).filter(Employee.employee_name == employee_name).one()

    def get_last_employee(self):
        """
        Get the last inserted employee.

        :rtype: Employee
        :return: Employee
        """
        return self.session.query(Employee).order_by(Employee.uid.desc()).first()

    def get_employee_list(self, filter_cond=None, order_by_cond=None):
        return super(EmployeeAccessor, self)._get_record_list(filter_cond, order_by_cond)

    # noinspection PyTypeChecker
    def insert_employee(self, **kwargs):
        photo_path = kwargs.pop('photo_path', u'')
        LOG.debug("insert_employee: photo_path={path!r}".format(path=photo_path))
        super(EmployeeAccessor, self)._insert_record(**kwargs)

        # -- Insert the photo if any
        if not isinstance(photo_path, (str, unicode)):
            try:
                # -- Get the newly created employee
                new_employee = self.get_last_employee()
                # -- insert the photo, because photo_path is a FieldStorage
                new_photo_path = self.store_photo(new_employee.uid, photo_path)
                # -- update photo path in new employee
                new_employee.photo_path = new_photo_path
                transaction.commit()
            except:
                transaction.abort()
                raise

        # -- Create a new Calendar and attach it to the newly created employee
        week_hours_list = self.week_hours_accessor.get_week_hours_list()
        if week_hours_list:
            week_hours = week_hours_list[0]
            # -- Get the newly created employee
            new_employee = self.get_last_employee()

            # -- Create the "best" label for this calendar
            label = new_employee.employee_name
            calendar_list = self.calendar_accessor.get_calendar_list(Calendar.label.like(u"%{0}%".format(label)))
            existing_labels = frozenset(c.label for c in calendar_list)
            if label in existing_labels:
                count = len(existing_labels) + 1
                label_fmt = u"{employee_name} ({count})"
                label = label_fmt.format(employee_name=new_employee.employee_name, count=count)
                while label in existing_labels:
                    count += 1
                    count = len(existing_labels) + 1
                    label = label_fmt.format(employee_name=new_employee.employee_name, count=count)

            # label can't have duplicate, so:
            self.calendar_accessor.insert_calendar(week_hours_uid=week_hours.uid,
                                                   label=label,
                                                   description=u"Calendrier de {0}".format(label))
            calendar = self.calendar_accessor.get_by_label(label)
            self.update_employee(new_employee.uid, calendar=calendar)

    # noinspection PyTypeChecker
    def update_employee(self, uid, **kwargs):
        photo_path = kwargs.pop('photo_path', u'')
        LOG.debug("update_employee: uid={uid!r}, photo_path={path!r}"
                  .format(uid=uid, path=photo_path))
        if not isinstance(photo_path, (str, unicode)):
            # -- replace the photo, because photo_path is a FieldStorage
            employee = self.get_employee(uid)
            self.delete_photo(employee.photo_path)
            new_photo_path = self.store_photo(employee.uid, photo_path)
            kwargs.update(photo_path=new_photo_path)
        return super(EmployeeAccessor, self)._update_record(uid, **kwargs)

    def delete_employee(self, uid):
        LOG.debug("delete_employee: uid={uid!r}".format(uid=uid))
        employee = self.get_employee(uid)
        photo_path = employee.photo_path
        employee_name = employee.employee_name
        try:
            self.session.delete(employee)
            self.delete_photo(photo_path)
            transaction.commit()
        except:
            transaction.abort()
            raise
        return employee_name

    # noinspection PyMethodMayBeStatic
    def store_photo(self, uid, photo_storage):
        if photo_storage is None:
            return None
        # -- upload photo file (@see: FieldStorage)
        relpath_fmt = "/photo/pointage/employee/employee_{uid}_{time}{ext}"
        ext = os.path.splitext(photo_storage.filename)[1]
        relpath = relpath_fmt.format(uid=uid, ext=ext, time=time.time())
        file_storage = FileStorage(tg.config.file_storage_dir)
        if relpath in file_storage:
            del file_storage[relpath]
        file_storage[relpath] = photo_storage.file.read()
        return relpath

    # noinspection PyMethodMayBeStatic
    def delete_photo(self, photo_path):
        if photo_path is None:
            return
        file_storage = FileStorage(tg.config.file_storage_dir)
        if photo_path in file_storage:
            del file_storage[photo_path]

    def get_active_employees(self, start_date_utc, end_date_utc=None):
        """
        Get the employees currently working at a given date interval.

        .. versionadded:: 2.2.0

        :type start_date_utc: datetime.date
        :param start_date_utc: Start date of the interval (UTC date).
        :type end_date_utc: datetime.date
        :param end_date_utc: End date of the interval (UTC date).
        :return: The ordered list of employees, possibly empty.
        """
        end_date_utc = end_date_utc or start_date_utc
        filter_cond = overlap_cond(start_date_utc, end_date_utc,
                                   Employee.entry_date, Employee.exit_date)
        query = self.session.query(self.record_class)
        return query.filter(filter_cond).order_by(Employee.employee_name).all()
