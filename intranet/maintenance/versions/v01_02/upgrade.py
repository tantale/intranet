#!/usr/local/bin/python2.7
# encoding: utf-8
'''
intranet.maintenance.versions.v01_02.upgrade -- Upgrade and cleanup the database

intranet.maintenance.versions.v01_02.upgrade is a GUI application used to upgrade the database from version 1.1.x to 1.2.0.

@author:     Laurent LAPORTE

@copyright:  2014 Tantale Solutions. All rights reserved.

@license:    Private license

@contact:    tantale.solution@gmail.com
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import logging
import os
import sys

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
import transaction
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.maintenance.versions.v01_01.model import CalEvent as SourceCalEvent
from intranet.maintenance.versions.v01_01.model import Employee as SourceEmployee
from intranet.maintenance.versions.v01_01.model import Order as SourceOrder
from intranet.maintenance.versions.v01_01.model import OrderCat as SourceOrderCat
from intranet.maintenance.versions.v01_01.model import init_model as source_init_model
from intranet.maintenance.versions.v01_02.model import CalEvent as TargetCalEvent
from intranet.maintenance.versions.v01_02.model import Employee as TargetEmployee
from intranet.maintenance.versions.v01_02.model import Order as TargetOrder
from intranet.maintenance.versions.v01_02.model import OrderCat as TargetOrderCat
from intranet.maintenance.versions.v01_02.model import OrderPhase as TargetOrderPhase
from intranet.maintenance.versions.v01_02.model import create_database as target_create_database
from intranet.maintenance.versions.v01_02.model import init_model as target_init_model


__all__ = []
__version__ = 0.1
__date__ = '2014-04-30'
__updated__ = '2014-04-30'

DEBUG = False
TESTRUN = False
PROFILE = False


LOG = logging.getLogger('intranet.maintenance.versions.v01_02.upgrade')


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = u"Upgrade and clean database to version 1.02"
    program_license = '''%s

  Created by Laurent LAPORTE on %s.
  Copyright 2014 Tantale Solutions. All rights reserved.

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                            help="Display INFO messages [default: %(default)s]")
        parser.add_argument("-D", "--debug", dest="debug", action="store_true",
                            help="Display DEBUG messages [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="source_data",
                            help="Path to the database file to read",
                            metavar="SOURCE_DATA")
        parser.add_argument(dest="target_data",
                            help="Path to the database file to write",
                            metavar="TARGET_DATA")

        # -- Process arguments
        args = parser.parse_args()

        # -- logging level
        level = logging.CRITICAL
        if args.debug:
            level = logging.DEBUG
        elif args.verbose:
            level = logging.INFO

        logging_format = "%(levelname)-7s\t%(name)s\t%(message)s"
        logging.basicConfig(format=logging_format, level=level)

        if not os.path.isfile(args.source_data):
            err_msg = "Source database not found: \"{path}\"".format(path=args.source_data)
            raise CLIError(err_msg)

        if os.path.isfile(args.target_data):
            err_msg = "Target database already exist: \"{path}\"".format(path=args.target_data)
            raise CLIError(err_msg)

        LOG.info(u"Starting upgrade...")
        upgrade(args.source_data, args.target_data)
        LOG.info(u"Upgrade done.")

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as exc:
        if DEBUG or TESTRUN:
            raise(exc)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + str(exc) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


def upgrade_order_cat(source):
    target = TargetOrderCat(source.cat_name, source.cat_group, source.label, source.css_def)
    target.uid = source.uid
    return target


def upgrade_employee(source):
    target = TargetEmployee(source.employee_name, float(source.worked_hours), source.entry_date, source.exit_date, source.photo_path)
    target.uid = source.uid
    return target


def upgrade_order_phase(source):
    target = TargetOrderPhase(source.position, source.label)
    target.uid = source.uid
    return target


def upgrade_order(source):
    target = TargetOrder(source.order_ref, source.project_cat, source.creation_date, source.close_date)
    target.order_phase_list = map(upgrade_order_phase, source.order_phase_list)
    target.uid = source.uid
    return target


def upgrade_cal_event(source):
    target = TargetCalEvent(source.event_start, source.event_end, source.comment, editable=True)
    target.uid = source.uid
    target.employee_uid = source.employee_uid
    target.order_phase_uid = source.order_phase_uid
    return target


def upgrade(source_data, target_data):
    if not os.path.isfile(target_data):
        target_dir = os.path.dirname(target_data)
        if target_dir and not os.path.isdir(target_dir):
            os.makedirs(target_dir)
        # -- create the target database from scratch
        target_create_database(target_data)

    # -- Connect to the source database
    LOG.info("-- Connect to the source database: \"{path}\"...".format(path=source_data))
    source_url = "sqlite:///{path}".format(path=source_data)
    source_engine = create_engine(source_url, echo=True)
    source_init_model(source_engine)
    source_maker = sessionmaker(bind=source_engine,
                                 autoflush=True,
                                 autocommit=False,
                                 extension=ZopeTransactionExtension())
    source_session = source_maker()

    # -- Connect to the target database
    LOG.info("-- Connect to the target database: \"{path}\"...".format(path=target_data))
    target_url = "sqlite:///{path}".format(path=target_data)
    target_engine = create_engine(target_url, echo=True)
    target_init_model(target_engine)
    target_maker = sessionmaker(bind=target_engine,
                                 autoflush=True,
                                 autocommit=False,
                                 extension=ZopeTransactionExtension())
    target_session = target_maker()

    LOG.info("-- upgrade OrderCat...")
    order_cat_list = source_session.query(SourceOrderCat).all()
    order_cat_list = map(upgrade_order_cat, order_cat_list)
    try:
        target_session.add_all(order_cat_list)
        transaction.commit()
    except:
        transaction.abort()
        raise

    LOG.info("-- upgrade Employee...")
    employee_list = source_session.query(SourceEmployee).all()
    employee_list = map(upgrade_employee, employee_list)
    try:
        target_session.add_all(employee_list)
        transaction.commit()
    except:
        transaction.abort()
        raise

    LOG.info("-- upgrade Order...")
    order_list = source_session.query(SourceOrder).all()
    order_list = map(upgrade_order, order_list)
    try:
        target_session.add_all(order_list)
        transaction.commit()
    except:
        transaction.abort()
        raise

    LOG.info("-- upgrade CalEvent...")
    cal_event_list = source_session.query(SourceCalEvent).all()
    cal_event_list = map(upgrade_cal_event, cal_event_list)
    try:
        target_session.add_all(cal_event_list)
        transaction.commit()
    except:
        transaction.abort()
        raise


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-D")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'intranet.maintenance.versions.v01_02.upgrade_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
