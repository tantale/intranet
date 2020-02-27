# -*- coding: utf-8 -*-
import unittest

from intranet.tests.accessors.test_employee_accessor import TestCalendarAccessor as BaseClass


class TestWithProfile(BaseClass):
    @unittest.skip(u"not tested")
    def test_get_employee_by_name(self):
        super(TestWithProfile, self).test_get_employee_by_name()

    @unittest.skip(u"not tested")
    def test_get_employee_by_name_NoResultFound(self):
        super(TestWithProfile, self).test_get_employee_by_name_NoResultFound()

    @unittest.skip(u"not tested")
    def test_get_employee_by_name_MultipleResultsFound(self):
        super(TestWithProfile, self).test_get_employee_by_name_MultipleResultsFound()

    @unittest.skip(u"not tested")
    def test_insert_employee(self):
        super(TestWithProfile, self).test_insert_employee()


if __name__ == '__main__':
    unittest.main()
