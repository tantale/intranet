"""
:module: intranet.accessors.employee
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.accessors import BasicAccessor
from intranet.model.file_storage import FileStorage
from intranet.model.pointage.employee import Employee
import os
import tg
import time
import transaction
import logging


LOG = logging.getLogger(__name__)


class EmployeeAccessor(BasicAccessor):

    def __init__(self, session=None):
        super(EmployeeAccessor, self).__init__(record_class=Employee,
                                               session=session)

    def get_employee(self, uid):
        return super(EmployeeAccessor, self)._get_record(uid)

    def get_employee_list(self, filter_cond=None, order_by_cond=None):
        return super(EmployeeAccessor, self)._get_record_list(filter_cond,
                                                             order_by_cond)

    def insert_employee(self, **kwargs):
        photo_path = kwargs.pop('photo_path', u'')
        LOG.debug("insert_employee: photo_path={path!r}"
                  .format(path=photo_path))
        new_employee = super(EmployeeAccessor, self)._insert_record(**kwargs)
        if not isinstance(photo_path, (str, unicode)):
            try:
                # -- insert the photo, because photo_path is a FieldStorage
                filter_cond = Employee.employee_name == kwargs['employee_name']
                new_employee = self.get_employee_list(filter_cond)[0]
                new_photo_path = self.store_photo(new_employee.uid, photo_path)
                # -- update photo path in new employee
                new_employee.photo_path = new_photo_path
                transaction.commit()
            except:
                transaction.abort()
                raise
        return new_employee

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
        old_employee = super(EmployeeAccessor, self)._delete_record(uid)
        self.delete_photo(old_employee.photo_path)
        return old_employee

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

    def delete_photo(self, photo_path):
        if photo_path is None:
            return
        file_storage = FileStorage(tg.config.file_storage_dir)
        if photo_path in file_storage:
            del file_storage[photo_path]
