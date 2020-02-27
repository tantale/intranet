# -*- coding: utf-8 -*-
"""
:module: intranet.tutorial.event_calendar
:date: 2013-09-30
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import datetime
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension  # @UnresolvedImport
import sqlalchemy
import transaction

from intranet.accessors.pointage.cal_event import CalEventAccessor
from intranet.model import DeclarativeBase
from intranet.tests.model.test_cal_event_data import EMPLOYEE_LIST, ORDER_LIST

LOG = logging.getLogger(__name__)


def main():
    LOG.info("-- sqlalchemy version: {module.__version__}"
             .format(module=sqlalchemy))

    # -- Connecting to the database
    LOG.info("-- Connecting to the database...")
    engine = create_engine('sqlite:///:memory:', echo=True)

    LOG.info("-- Creating the database...")
    DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

    # -- Creating a Session
    LOG.info("-- Creating a session...")
    session_maker = sessionmaker(bind=engine,
                                 autoflush=True,
                                 autocommit=False,
                                 extension=ZopeTransactionExtension())
    session = session_maker()

    # -- Create some employees
    LOG.info("-- Create some employees...")
    try:
        session.add_all(EMPLOYEE_LIST)
        transaction.commit()
    except:
        transaction.abort()
        raise

    # -- Create some orders with phases
    LOG.info("-- Create some orders with phases...")
    try:
        session.add_all(ORDER_LIST)
        transaction.commit()
    except:
        transaction.abort()
        raise

#    employee_list = session.query(Employee).all()
#    employee_0 = employee_list[0]
#    employee_1 = employee_list[1]
#
#    order_list = session.query(Order).all()
#    order_0 = order_list[0]
#    order_1 = order_list[1]

    # -- Create some events
    LOG.info("-- Create some calendar events...")
    accessor = CalEventAccessor(session)
#    employee_uid = employee_0.uid
#    order_phase_uid = order_0.order_phase_list[0].uid
    employee_uid = 1
    order_phase_uid = 2
    LOG.info("-- Insert an event for employee #{employee_uid} and "
             "order phase #{order_phase_uid}..."
             .format(employee_uid=employee_uid,
                     order_phase_uid=order_phase_uid))
    accessor.insert_cal_event(employee_uid, order_phase_uid,
                              title=u"Preparation [100]",
                              event_start=datetime.datetime(2010, 5, 2, 8, 0),
                              event_end=datetime.datetime(2010, 5, 2, 9, 0),
                              comment=u"Préparation commande #1")


if __name__ == '__main__':
    BASIC_FORMAT = "%(levelname)s: %(message)s"
    logging.basicConfig(format=BASIC_FORMAT,
                        level=logging.INFO)
    main()
