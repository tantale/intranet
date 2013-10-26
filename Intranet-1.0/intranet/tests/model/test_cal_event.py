# -*- coding: utf-8 -*-
"""
:module: intranet.tests.model.test_cal_event
:date: 2013-09-16
:author: Laurent LAPORTE <sandlol2009@gmail.com>

Test case of 'intranet.model.pointage.cal_event' module.
"""
from intranet.model import DBSession
from intranet.model.pointage.cal_event import CalEvent
from intranet.model.pointage.employee import Employee
from intranet.model.pointage.order import Order
from intranet.tests import setup_db, teardown_db
from intranet.tests.model.test_cal_event_data import EMPLOYEE_LIST, ORDER_LIST
import datetime
import transaction
import unittest


# Create an empty database before we start our tests for this module
def setup():
    """Function called by nose on module load"""
    setup_db()


# Tear down that database
def teardown():
    """Function called by nose after all tests in this module ran"""
    teardown_db()


class TestCalEvent(unittest.TestCase):
    """
    Test case of 'CalEvent' class.
    """

    def parse_date(self, date_str):
        if date_str:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            return None

    def setUp(self):
        # -- create some employees
        try:
            DBSession.add_all(EMPLOYEE_LIST)
            transaction.commit()
        except:
            transaction.abort()
            raise

        # -- create some orders with phases
        try:
            DBSession.add_all(ORDER_LIST)
            transaction.commit()
        except:
            transaction.abort()
            raise

    def test_add_event(self):
        employee_list = DBSession.query(Employee).all()
        employee_0 = employee_list[0]
        order_list = DBSession.query(Order).all()
        order_0 = order_list[0]
        order_1 = order_list[1]
        try:
            event_0 = CalEvent(title=u"Preparation [100]",
                              event_start=datetime.datetime(2010, 5, 2, 8, 0),
                              event_end=datetime.datetime(2010, 5, 2, 9, 0),
                              comment=u"Préparation commande #1")
            employee_0.cal_event_list.append(event_0)
            order_0.order_phase_list[0].cal_event_list.append(event_0)

            event_1 = CalEvent(title=u"Usinage [200]",
                              event_start=datetime.datetime(2010, 5, 2, 9, 0),
                              event_end=datetime.datetime(2010, 5, 2, 11, 0),
                              comment=u"Usinage commande #1")
            employee_0.cal_event_list.append(event_1)
            order_0.order_phase_list[1].cal_event_list.append(event_1)

            event_2 = CalEvent(title=u"Assemblage [100]",
                              event_start=datetime.datetime(2010, 5, 2, 11, 0),
                              event_end=datetime.datetime(2010, 5, 2, 12, 0),
                              comment=u"Assemblage commande #1")
            employee_0.cal_event_list.append(event_2)
            order_0.order_phase_list[2].cal_event_list.append(event_2)

            event_3 = CalEvent(title=u"Preparation [200]",
                              event_start=datetime.datetime(2010, 5, 2, 14, 0),
                              event_end=datetime.datetime(2010, 5, 2, 16, 0),
                              comment=u"Préparation command #2")
            employee_0.cal_event_list.append(event_3)
            order_1.order_phase_list[0].cal_event_list.append(event_3)

            event_3 = CalEvent(title=u"Finition [100]",
                              event_start=datetime.datetime(2010, 5, 2, 17, 0),
                              event_end=datetime.datetime(2010, 5, 2, 18, 0),
                              comment=u"Finition commande #1")
            employee_0.cal_event_list.append(event_3)
            order_0.order_phase_list[2].cal_event_list.append(event_3)

            transaction.commit()
        except:
            transaction.abort()
            raise

        event_list = DBSession.query(CalEvent).all()
        for event in event_list:
            print event

        employee_list = DBSession.query(Employee).all()
        for employee in employee_list:
            print(employee.employee_name)
            for cal_event in employee.cal_event_list:
                print("- " + cal_event.title)

        # TODO: to be continued...
        self.assertEqual(event.title, u"Preparation [100]")


if __name__ == "__main__":
    unittest.main()
