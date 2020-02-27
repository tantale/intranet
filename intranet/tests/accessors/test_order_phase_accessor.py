# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import datetime
import logging
import unittest

import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors.pointage.order import OrderAccessor
from intranet.accessors.pointage.order_phase import OrderPhaseAccessor
from intranet.model import DeclarativeBase

LOG = logging.getLogger(__name__)


class TestOrderPhaseAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestOrderPhaseAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestOrderPhaseAccessor, self).setUp()

        # -- Connecting to the database
        engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

        order_accessor = OrderAccessor(self.session)
        order_ref = "My order_ref"
        project_cat = "My project_cat"
        creation_date = datetime.datetime(2016, 2, 14, 12, 30)
        order_accessor.insert_order(order_ref=order_ref,
                                    project_cat=project_cat,
                                    creation_date=creation_date)

    def test_insert_order_phase(self):
        order_accessor = OrderAccessor(self.session)
        order_phase_accessor = OrderPhaseAccessor(self.session)

        order = order_accessor.get_order_list()[-1]
        order_uid = order.uid

        order_phase_list = order_phase_accessor.get_order_phase_list()
        for order_phase in order_phase_list:
            LOG.debug(order_phase)
        default_list = [dict(position=order_phase.position,
                             label=order_phase.label,
                             description=order_phase.description)
                        for order_phase in order_phase_list]

        attrs_list = [dict(position=6,
                           label="Phase 1",
                           description=None),
                      dict(position=7,
                           label="Phase 2",
                           description="Description 2"),
                      dict(position=8,
                           label="Phase 2",
                           description="Description 2 bis")]
        for attrs in attrs_list:
            order_phase_accessor.insert_order_phase(order_uid, **attrs)

        order_phase_list = order_phase_accessor.get_order_phase_list()
        for order_phase in order_phase_list:
            LOG.debug(order_phase)

        expected_list = [dict(position=order_phase.position,
                              label=order_phase.label,
                              description=order_phase.description)
                         for order_phase in order_phase_list]
        self.assertEqual(expected_list, default_list + attrs_list)

    def test_update_order_phase(self):
        order_phase_accessor = OrderPhaseAccessor(self.session)

        order_phase_list = order_phase_accessor.get_order_phase_list()
        for order_phase in order_phase_list:
            LOG.debug(order_phase)

        for order_phase in order_phase_list:
            order_phase_accessor.update_order_phase(order_phase.uid, description=u"hello")

        order_phase_list = order_phase_accessor.get_order_phase_list()
        for order_phase in order_phase_list:
            LOG.debug(order_phase)
            self.assertEqual(order_phase.description, u"hello")

    def test_delete_order_phase(self):
        order_phase_accessor = OrderPhaseAccessor(self.session)

        order_phase_list = order_phase_accessor.get_order_phase_list()
        for order_phase in order_phase_list:
            LOG.debug(order_phase)

        last = order_phase_list[-1]
        last_uid = last.uid
        order_phase_accessor.delete_order_phase(last_uid)

        current_list = order_phase_accessor.get_order_phase_list()
        uid_list = [current.uid for current in current_list]
        self.assertNotIn(last_uid, uid_list)
