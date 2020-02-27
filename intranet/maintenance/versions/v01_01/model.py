# encoding: utf-8
"""
:Module: intranet.maintenance.versions.v01_01.model
:Created on: 2014-05-02
:Author: Tantale Solutions <tantale.solutions@gmail.com>
"""
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension


LOG = logging.getLogger(__name__)


# Global session manager.  DBSession() returns the session object
# appropriate for the current web request.
maker = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

# By default, the data model is defined with SQLAlchemy's declarative
# extension, but if you need more control, you can switch to the traditional
# method.
DeclarativeBase = declarative_base()

# Global metadata.
# The default metadata is the one from the declarative base.
metadata = DeclarativeBase.metadata

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)

def create_database(data_path):
    # -- Build the connection's URL
    connect_url = "sqlite:///{path}".format(path=data_path)
    
    # -- Connecting to the database
    LOG.info("-- Connecting to the database...")
    engine = create_engine(connect_url, echo=True)

    LOG.info("-- Creating the database...")
    DeclarativeBase.metadata.create_all(engine)
    

# Import your model modules here.
from intranet.maintenance.versions.v01_01.pointage.cal_event import CalEvent  # @UnusedImport
from intranet.maintenance.versions.v01_01.pointage.employee import Employee  # @UnusedImport
from intranet.maintenance.versions.v01_01.pointage.order import Order  # @UnusedImport
from intranet.maintenance.versions.v01_01.pointage.order_cat import OrderCat  # @UnusedImport
from intranet.maintenance.versions.v01_01.pointage.order_phase import OrderPhase  # @UnusedImport
