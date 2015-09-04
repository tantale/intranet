# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import unittest
import logging

from sqlalchemy import create_engine
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import desc, asc
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.accessors import RecordNotFoundError
from intranet.accessors.planning.frequency import FrequencyAccessor
from intranet.model import DeclarativeBase
from intranet.model.planning.frequency import Frequency

LOG = logging.getLogger(__name__)


class TestFrequencyAccessor(unittest.TestCase):
    DEBUG = False

    @classmethod
    def setUpClass(cls):
        super(TestFrequencyAccessor, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG if cls.DEBUG else logging.FATAL)

    def setUp(self):
        super(TestFrequencyAccessor, self).setUp()

        # -- Connecting to the database
        engine = create_engine('sqlite:///:memory:', echo=False)
        DeclarativeBase.metadata.create_all(engine)  # @UndefinedVariable

        # -- Creating a Session
        session_maker = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
        self.session = session_maker()

    def test_setup(self):
        accessor = FrequencyAccessor(self.session)
        accessor.setup()
        accessor.setup()  # on second setup, do nothing

    def test_delete_frequency(self):
        accessor = FrequencyAccessor(self.session)
        accessor.insert_frequency("frequency1", "description", 0, 2)
        accessor.delete_frequency(1)
        with self.assertRaises(RecordNotFoundError) as context:
            accessor.delete_frequency(123)
        LOG.debug(context.exception)

    def test_get_frequency(self):
        accessor = FrequencyAccessor(self.session)
        accessor.insert_frequency("frequency1", "description", 0, 2)
        accessor.insert_frequency("frequency2", "description", 1, 2)
        (f1, f2) = accessor.get_frequency_list()
        frequency = accessor.get_frequency(f1.uid)
        self.assertEqual(frequency, f1)
        frequency = accessor.get_frequency(f2.uid)
        self.assertEqual(frequency, f2)
        with self.assertRaises(RecordNotFoundError):
            accessor.get_frequency(123)

    def test_insert_frequency(self):
        accessor = FrequencyAccessor(self.session)
        accessor.insert_frequency("frequency1", "description", 0, 2)

        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_frequency("frequency1", "description2", 1, 2)
        LOG.debug(context.exception)

        # (modulo, quotient) is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_frequency("frequency3", "description3", 0, 2)
        LOG.debug(context.exception)

        # 0 < quotient
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_frequency("frequency4", "description4", 1, 0)
        LOG.debug(context.exception)

        # 0 <= modulo < quotient
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_frequency("frequency5", "description5", -1, 1)
        LOG.debug(context.exception)

        # 0 <= modulo < quotient
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.insert_frequency("frequency6", "description6", 5, 2)
        LOG.debug(context.exception)

    def test_get_frequency_list(self):
        accessor = FrequencyAccessor(self.session)
        self.assertFalse(accessor.get_frequency_list())

        accessor.insert_frequency("frequency1", "description", 0, 2)
        accessor.insert_frequency("frequency2", "description", 1, 2)
        curr = accessor.get_frequency_list()
        self.assertEqual(curr[0].label, "frequency1")
        self.assertEqual(curr[1].label, "frequency2")

        curr = accessor.get_frequency_list(Frequency.label == "frequency2")
        self.assertEqual(len(curr), 1)
        self.assertEqual(curr[0].label, "frequency2")

        accessor.insert_frequency("frequency3", "description", 0, 1)
        curr = accessor.get_frequency_list(order_by_cond=desc(Frequency.label))
        self.assertEqual(len(curr), 3)
        self.assertEqual(curr[0].label, "frequency3")
        self.assertEqual(curr[1].label, "frequency2")
        self.assertEqual(curr[2].label, "frequency1")

        curr = accessor.get_frequency_list(order_by_cond=(asc(Frequency.quotient), asc(Frequency.modulo)))
        self.assertEqual(len(curr), 3)
        fractions = [(x.modulo, x.quotient) for x in curr]
        self.assertEqual(fractions, [(0, 1), (0, 2), (1, 2)])

    def test_update_frequency(self):
        accessor = FrequencyAccessor(self.session)
        accessor.insert_frequency("frequency1", "description", 0, 2)
        uid = 1

        accessor.update_frequency(uid, label="new frequency", description="new description", modulo=12, quotient=24)
        curr = accessor.get_frequency(uid)
        self.assertEqual(curr.label, "new frequency")
        self.assertEqual(curr.description, "new description")
        self.assertEqual(curr.modulo, 12)
        self.assertEqual(curr.quotient, 24)

        accessor.insert_frequency("frequency1", "description", 0, 2)

        # label is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_frequency(uid, label="frequency1")
        LOG.debug(context.exception)

        # (modulo, quotient) is unique
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_frequency(uid, modulo=0, quotient=2)
        LOG.debug(context.exception)

        # 0 < quotient
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_frequency(uid, quotient=0)
        LOG.debug(context.exception)

        # 0 <= modulo < quotient
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_frequency(uid, modulo=-1)
        LOG.debug(context.exception)

        # 0 <= modulo < quotient
        with self.assertRaises(sqlalchemy.exc.IntegrityError) as context:
            accessor.update_frequency(uid, modulo=5, quotient=2)
        LOG.debug(context.exception)
