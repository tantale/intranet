# -*- coding: utf-8 -*-
"""Unit test suite for the models of the application."""
from intranet.model import DBSession
from intranet.tests import setup_db, teardown_db
from nose.tools import eq_
import transaction

__all__ = ['ModelTest']


# Create an empty database before we start our tests for this module
def setup():
    """Function called by nose on module load"""
    setup_db()


# Tear down that database
def teardown():
    """Function called by nose after all tests in this module ran"""
    teardown_db()


class ModelTest(object):
    """Base unit test case for the models."""

    klass = None
    attrs = {}

    def __init__(self):
        self.obj = None  # created during setUp

    def setUp(self):
        """Prepare model test fixture."""
        try:
            new_attrs = {}
            new_attrs.update(self.attrs)
            new_attrs.update(self.do_get_dependencies())
            self.obj = self.klass(**new_attrs)
            DBSession.add(self.obj)
            transaction.commit()
        except:
            transaction.abort()
            raise

    def tearDown(self):
        """Finish model test fixture."""
        try:
            for obj in DBSession.query(self.klass).all():
                DBSession.delete(obj)
            transaction.commit()
        except:
            transaction.abort()
            raise

    def do_get_dependencies(self):
        """Get model test dependencies.

        Use this method to pull in other objects that need to be created
        for this object to be build properly.

        """
        return {}

    def test_query_obj(self):
        """Model objects can be queried"""
        for obj in DBSession.query(self.klass).all():
            for key, value in self.attrs.iteritems():
                eq_(getattr(obj, key), value)
