"""
:module: intranet.tutorial.transaction_manager
:date: 2013-09-08
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from zope.sqlalchemy import ZopeTransactionExtension
from intranet.model import DeclarativeBase
from intranet.model.pointage.order import Order
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import datetime
import logging
import sqlalchemy
import transaction

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

    # -- Adding New Objects
    LOG.info("-- Adding new objects...")
    order_ref = "order_ref"
    project_cat = "project_cat"
    creation_date = datetime.datetime.now()
    close_date = None
    order1 = Order(order_ref, project_cat, creation_date, close_date)
    order2 = Order(order_ref, project_cat, creation_date, close_date)

    LOG.info("-- Starting transaction...")
    try:
        session.add_all([order1, order2])
        LOG.info("-- dirty: {!r}".format(session.dirty))
        LOG.info("-- new: {!r}".format(session.new))
        transaction.commit()
        LOG.info("-- Transaction finished.")
    except IntegrityError:
        transaction.abort()
        LOG.info("-- Transaction rollbacked.")

    order_list = session.query(Order).all()
    LOG.info("-- {count:d} order(s) found."
             .format(count=len(order_list)))
    for order in order_list:
        LOG.info("-- Order: {order!r}"
                 .format(order=order))


if __name__ == '__main__':
    BASIC_FORMAT = "%(levelname)s: %(message)s"
    logging.basicConfig(format=BASIC_FORMAT,
                        level=logging.INFO)
    main()
