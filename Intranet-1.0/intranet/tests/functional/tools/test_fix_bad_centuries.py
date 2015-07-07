"""
:module: intranet.tests.functional.tools.test_fix_bad_centuries
:date: 2014-01-26
:author: Laurent LAPORTE <sandlol2009@gmail.com>

Test case of 'intranet.controllers.tools.fix_bad_centuries' module.
"""
import datetime
import json
import unittest

from nose.tools import ok_, eq_

from intranet.accessors.pointage.employee import EmployeeAccessor

from intranet.model.pointage.employee import Employee
from intranet.tests import *  # @UnusedWildImport
from intranet.controllers.tools.fix_bad_centuries import fix_century


class TestFunctions(unittest.TestCase):

    def test_fix_century(self):
        curr_date = datetime.datetime.today()
        bad_date = curr_date.replace(year=curr_date.year % 100)
        actual = fix_century(bad_date)
        self.assertEqual(actual, curr_date)


class TestFixBadCenturiesController(TestController):
    """
    Test case of 'FixBadCenturiesController' class.
    """

    def __init__(self, *args, **kwargs):
        TestController.__init__(self, *args, **kwargs)

    def _cleanup(self):
        accessor = EmployeeAccessor()
        filter_cond = Employee.employee_name == "MrTest"
        employee_list = accessor.get_employee_list(filter_cond)
        for employee in employee_list:
            accessor.delete_employee(employee.uid)

    def setUp(self):
        TestController.setUp(self)
        self._cleanup()
        bad_date = datetime.datetime(14, 01, 26)
        accessor = EmployeeAccessor()
        accessor.insert_employee(employee_name="MrTest",
                                 worked_hours=39,
                                 entry_date=bad_date,
                                 exit_date=None,
                                 photo_path=None)

    def tearDown(self):
        self._cleanup()
        TestController.tearDown(self)

    def test_index(self):
        # webtest.app.TestResponse
        response = self.app.get('/tools/fix_bad_centuries.json')
        obj = json.loads(response.body)
        ok_('employee_list' in obj)
        expected_list = [{u'employee_name': u'MrTest',
                          u'worked_hours': 39,
                          u'entry_date': u'0014-01-26',
                          u'exit_date': None,
                          u'photo_path': None}]
        for record in obj['employee_list']:
            del record['uid']  # not comparable
        eq_(obj['employee_list'], expected_list)
        ok_('order_list' in obj)
        eq_(obj['order_list'], [])
        ok_('cal_event_list' in obj)
        eq_(obj['cal_event_list'], [])


if __name__ == "__main__":
    unittest.main()
