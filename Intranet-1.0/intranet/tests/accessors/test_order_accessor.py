# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import datetime
import logging
import random
import unittest

import sqlalchemy
import sqlalchemy.exc
import transaction
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors.pointage.cal_event import CalEventAccessor
from intranet.accessors.pointage.employee import EmployeeAccessor
from intranet.accessors.pointage.order import OrderAccessor
from intranet.model import DeclarativeBase
from intranet.model.pointage.cal_event import CalEvent
from intranet.model.pointage.order import Order

LOG = logging.getLogger(__name__)


class TestOrderAccessor(unittest.TestCase):
    DEBUG = True

    @classmethod
    def setUpClass(cls):
        super(TestOrderAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestOrderAccessor, self).setUp()

        # -- Connecting to the database
        engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

        # -- Create a Employee
        self.employee_accessor = EmployeeAccessor(self.session)
        for employee_name in ["Pierre", "Paul", "Jacques"]:
            worked_hours = 39.0
            entry_date = datetime.date(2010, 11, 15)
            self.employee_accessor.insert_employee(employee_name=employee_name,
                                                   worked_hours=worked_hours,
                                                   entry_date=entry_date,
                                                   exit_date=None,
                                                   photo_path=None)

    def test_prepare_planning(self):
        employee_name = "you"

        # -- Create a "old" Order with tracked time
        self.order_accessor = OrderAccessor(self.session)
        orders = [dict(order_ref="Order#{0}".format(n),
                       project_cat="project_cat",
                       creation_date=datetime.date(2015, 10, 1) + datetime.timedelta(days=n),
                       close_date=datetime.date(2015, 11, 16) + datetime.timedelta(days=n))
                  for n in range(100)]
        for order in orders:
            self.order_accessor.insert_order(**order)

        self.cal_event_accessor = CalEventAccessor(self.session)
        try:
            employees = self.employee_accessor.get_employee_list()
            for order in self.order_accessor.get_order_list():
                for order_phase in order.order_phase_list:
                    for times in xrange(random.randrange(10)):
                        # choose a day between creation_date and close_date
                        period = order.close_date - order.creation_date
                        days = random.randrange(period.days)
                        # choose start and end hours
                        hour_start = random.randrange(8, 19)
                        hour_end = random.randrange(hour_start, 19)
                        tracked_date = datetime.datetime.combine(order.creation_date, datetime.time(0))
                        event_start = tracked_date + datetime.timedelta(days=days, hours=hour_start)
                        event_end = tracked_date + datetime.timedelta(days=days, hours=hour_end)
                        cal_event = CalEvent(event_start, event_end, comment=u"")
                        cal_event.employee = random.choice(employees)
                        cal_event.order_phase = order_phase
                        # print(cal_event)
                        self.session.add(cal_event)
            transaction.commit()
        except:
            transaction.abort()
            raise

        # -- Create a "new" Order without tracked time
        self.order_accessor.insert_order(order_ref="NewOrder",
                                         project_cat="project_cat",
                                         creation_date=datetime.date(2016, 1, 21),
                                         close_date=None)

        print("Estimate OrderPhase duration...")
        new_order = self.order_accessor.get_order_list(Order.order_ref == "NewOrder")[0]

        order_uid = new_order.uid
        self.order_accessor.estimate_duration(order_uid, closed=True)

        new_order = self.order_accessor.get_order(order_uid)
        for order_phase in new_order.order_phase_list:
            print("{label}: {duration}".format(label=order_phase.label, duration=order_phase.estimated_duration))
