# -*- coding: utf-8 -*-
"""
automap_demo
============

Date: 2015-03-31

Author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from __future__ import unicode_literals, print_function
import contextlib

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension
import transaction


def automap_demo():

    # engine, suppose it has two tables 'user' and 'address' set up
    here = "/Users/laurentlaporte/git/repo-intranet-master/Intranet-1.0/__backup/"
    # here = "/Users/laurentlaporte/Desktop"
    # engine = create_engine('sqlite:///{here}/productiondata.db'.format(here=here), echo=False)
    engine = create_engine('mysql+mysqlconnector://root@localhost:3306/planning', echo=False)

    # produce our own MetaData object
    metadata = MetaData()

    # we can reflect it ourselves from a database, using options
    # such as 'only' to limit what tables we look at...
    metadata.reflect(engine)

    for table in metadata.sorted_tables:
        print(table)
        for column in table.columns:
            print(repr(column))

    session_maker = sessionmaker(bind=engine,
                                 autoflush=True,
                                 autocommit=False,
                                 extension=ZopeTransactionExtension())

    with contextlib.closing(session_maker()) as session:
        frequency_list = session.query(metadata.tables["frequency"]).all()
        for frequency in frequency_list:
            print(frequency)


if __name__ == '__main__':
    automap_demo()
