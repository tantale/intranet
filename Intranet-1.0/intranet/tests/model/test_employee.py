"""
:module: intranet.tests.model.test_employee
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>

Test case of 'intranet.model.pointage.employee' module.
"""
from intranet import model
from intranet.model import DBSession
from intranet.tests.model import ModelTest
from nose.tools import eq_
import datetime
import transaction


class TestEmployee(ModelTest):
    """
    Test case of 'Employee' class.
    """

    klass = model.Employee
    attrs = dict(employee_name="John DOE",
                 worked_hours=39,
                 entry_date=datetime.date(2004, 2, 27),
                 exit_date=datetime.date(2012, 12, 31),
                 photo_path="/photos/john_doe.jpg")

    def test_create_obj(self):
        """Employee object can be created"""
        self.obj = DBSession.query(model.Employee).one()
        for key, value in self.attrs.iteritems():
            eq_(getattr(self.obj, key), value)

    def test_query_obj(self):
        """Employee objects can be queried"""
        super(TestEmployee, self).test_query_obj()

    def test_delete_obj(self):
        """Employee objects can be deleted"""
        try:
            DBSession.delete(self.obj)
            transaction.commit()
        except:
            transaction.abort()
            raise
