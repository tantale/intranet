# -*- coding: utf-8 -*-
"""Unit and functional test suite for Intranet-1.0."""

from intranet.model import *
from nose.tools import eq_
from os import path
from paste.deploy import loadapp  # @UnresolvedImport
from paste.script.appinstall import SetupCommand  # @UnresolvedImport
from routes import url_for
from tg import config
from webtest import TestApp
import sys


__all__ = ['setup_db', 'teardown_db', 'TestController', 'url_for']


def setup_db():
    """Method used to build a database"""
    engine = config['pylons.app_globals'].sa_engine
    init_model(engine)
    metadata.create_all(engine)  # @UndefinedVariable 'create_all'


def teardown_db():
    """Method used to destroy a database"""
    engine = config['pylons.app_globals'].sa_engine
    metadata.drop_all(engine)  # @UndefinedVariable 'drop_all'


class TestController(object):
    """
    Base functional test case for the controllers.

    The Intranet-1.0 application instance (``self.app``) set up in this test
    case (and descendants) has authentication disabled, so that developers can
    test the protected areas independently of the :mod:`repoze.who` plugins
    used initially. This way, authentication can be tested once and separately.

    Check intranet.tests.functional.test_authentication for the repoze.who
    integration tests.

    This is the officially supported way to test protected areas with
    repoze.who-testutil (http://code.gustavonarea.net/repoze.who-testutil/).

    """

    application_under_test = 'main_without_authn'

    def setUp(self):
        """Method called by nose before running each test"""
        # Loading the application:
        conf_dir = config.here
        wsgiapp = loadapp('config:test.ini#%s' % self.application_under_test,
                          relative_to=conf_dir)
        self.app = TestApp(wsgiapp)
        # Setting it up:
        test_file = path.join(conf_dir, 'test.ini')
        cmd = SetupCommand('setup-app')
        cmd.run([test_file])

    def tearDown(self):
        """Method called by nose after running each test"""
        # Cleaning up the database:
        DBSession.remove()
        teardown_db()
