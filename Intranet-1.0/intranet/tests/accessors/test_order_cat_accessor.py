# -*- coding: utf-8 -*-
"""
Short title of test_order_cat_accessor module
===============================

Module: ${PACKAGE}.test_order_cat_accessor

Created on: 2015-09-10
"""
from __future__ import unicode_literals, print_function
import pprint
import unittest
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors.pointage.order_cat import OrderCatAccessor
from intranet.model import DeclarativeBase
from intranet.model.pointage.order_cat import OrderCat

LOG = logging.getLogger(__name__)


class TestOrderCatAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestOrderCatAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestOrderCatAccessor, self).setUp()

        # -- Connecting to the database
        engine = create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

        self.accessor = OrderCatAccessor(self.session)

    # def test_get_order_cat(self):
    #     self.fail()

    # def test_get_order_cat_list(self):
    #     self.fail()

    def test_insert_order_cat(self):
        LOG.info("Insert a OrderCat...")
        cat_name = "Meubles"
        cat_group = "Commandes"
        label = "Fab. de meubles"
        css_def = "color: #000000; background-color: #ffffff"
        self.accessor.insert_order_cat(cat_name=cat_name, cat_group=cat_group, label=label, css_def=css_def)

        LOG.info("Check the list of OrderCat...")
        order_cat_list = self.accessor.get_order_cat_list()
        self.assertEqual(len(order_cat_list), 1)
        order_cat = order_cat_list[0]
        assert isinstance(order_cat, OrderCat)
        self.assertEqual(order_cat.cat_name, cat_name)
        self.assertEqual(order_cat.cat_group, cat_group)
        self.assertEqual(order_cat.label, label)
        self.assertEqual(order_cat.css_def, css_def)

    # def test_update_order_cat(self):
    #     self.fail()

    # def test_delete_order_cat(self):
    #     self.fail()

    def test_get_order_cat_groups(self):
        LOG.info("Insert the OrderCat...")
        css_def = "color: #000000; background-color: #ffffff"
        LOG.info("Insert first group...")
        group1 = {"Commandes": [dict(cat_name="Meubles", label="Les meubles", css_def=css_def),
                                dict(cat_name="Cuisine", label="La cuisine", css_def=css_def)]}
        group2 = {"Divers": [dict(cat_name="Nettoyage", label="Nettoyage atelier", css_def=css_def)]}
        for group in [group1, group2]:
            for cat_group, order_cat_list in group.iteritems():
                for order_cat in order_cat_list:
                    self.accessor.insert_order_cat(cat_group=cat_group, **order_cat)

        LOG.info("Read the groups...")
        order_cat_groups = self.accessor.get_order_cat_groups()
        LOG.debug(pprint.pformat(order_cat_groups))

        LOG.info("Check the result...")
        self.assertEqual(len(order_cat_groups), 2)
        self.assertEqual(order_cat_groups.keys(), ["Commandes", "Divers"])
        expected = dict(group1, **group2)
        for cat_group, order_cat_list in order_cat_groups.iteritems():
            expected_list = expected[cat_group]
            for order_cat, attrs in zip(order_cat_list, expected_list):
                for key, value in attrs.iteritems():
                    self.assertEqual(getattr(order_cat, key), value)
