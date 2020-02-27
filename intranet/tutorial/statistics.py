# -*- coding: utf-8 -*-
"""
:Module: statistics
:Author: Laurent LAPORTE <llaporte@jouve.fr>
:Created on: 2015-03-24
:Project: Intranet-1.0
"""
from __future__ import print_function, unicode_literals
import collections
import logging

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy

from intranet.accessors.pointage.order import OrderAccessor
from intranet.model.pointage.order import Order

LOG = logging.getLogger(__name__)


def main():
    LOG.info("-- sqlalchemy version: {module.__version__}".format(module=sqlalchemy))

    # -- Connecting to the database
    LOG.info("-- Connecting to the database...")
    here = "/Users/laurentlaporte/git/repo-intranet-master/Intranet-1.0/__backup/"
    here = "/Users/laurentlaporte/Desktop"
    engine = create_engine('sqlite:///{here}/productiondata.db'.format(here=here), echo=False)

    # -- Creating a Session
    LOG.info("-- Creating a session...")
    session_maker = sessionmaker(bind=engine,
                                 autoflush=True,
                                 autocommit=False,
                                 extension=ZopeTransactionExtension())
    session = session_maker()

    # -- Cumul des pointages
    general_stats = collections.Counter()

    accessor = OrderAccessor(session)
    rows = []
    for order in accessor.get_order_list(Order.project_cat == "colorMeuble", Order.creation_date):
        general_stats.update(order.statistics)
        rows.append([order, order.statistics])

    keys = list(sorted(general_stats.keys()))
    row_fmt = u'{uid:05d} {order_ref:<32s} {creation_date} {close_date} {values}'
    fmt_duration = lambda x: "{0:>7s}".format("–.––") if x is None else "{0:7.2f}".format(x)
    fmt_date = lambda x: "––/––/––––" if x is None else x.strftime("%d/%m/%Y")
    for row in rows:
        order, order_stats = row
        values = [fmt_duration(order_stats.get(key)) for key in keys]
        values.append(fmt_duration(sum(order_stats[key] for key in keys)))
        attrs = dict(uid=order.uid,
                     order_ref=order.order_ref,
                     creation_date=fmt_date(order.creation_date),
                     close_date=fmt_date(order.close_date),
                     values=" ".join(values))
        print(row_fmt.format(**attrs))

    values = [fmt_duration(general_stats.get(key)) for key in keys]
    values.append(fmt_duration(sum(general_stats[key] for key in keys)))
    attrs = dict(uid=0,
                 order_ref="TOTAL DURATION",
                 creation_date="..........",
                 close_date="..........",
                 values=" ".join(values))
    print(row_fmt.format(**attrs))


if __name__ == '__main__':
    main()
