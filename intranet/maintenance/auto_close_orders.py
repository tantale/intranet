# coding: utf-8
u"""
Clôture automatique des commandes
=================================

L'application ``auto_close_orders`` clôture automatiquement les commandes qui n'ont plus de
pointage depuis un certain temps (au moins 3\xa0mois).

L'objectifde cette application est de répondre à plusieurs exigences\xa0:

- Pour le calcul du crédit d'impôt en faveur des métiers d'art (CIMA), il est nécessaire de
  distinguer les commandes terminées (clôturées) des commandes en cours, notamment en fin d'exercice.
- La performance du logiciel de pointage s'en trouve améliorée, car seules les commandes en cours
  sont réellement affichées\xa0: on évite un temps de latence lors du pointage.
- L'estimation de la durée des tâches est plus pertinente si est s'effectue sur des tâches clôturées.

Une tâche planifiée permettra d'exécuter cette application périodiquement (par exemple\xa0: chaque
jour) pour maintenir à jour la base de données.

Comment est effectuée la clôture automatique des commandes\xa0?

- L'application recherche toutes les commandes non clôturée. Pour chaque commande, l'application
  récupère la liste des phases et recherche tous les pointages associés, triés dans l'ordre
  chronologique des dates de fin de tâche.

- On détermine alors la date de la phase la plus récente. Si cette date est supérieure à 3 mois,
  on considèrera que la tâche est terminée. On mettra à jour la date de clôture de la commandent
  fonction de la date de la dernière phase.

.. note::

   La clôture d'une commande est réversible. Si l'utilisateur considère qu'une commande est encore
   en cours, il pourra supprimer la date de clôture (la remettre à blanc) et procéder à un pointage.
   Ainsi, la commande restera en cours encore pendant 3\xa0mois.
"""
import argparse
import datetime
import glob
import logging
import os
import shutil

import pkg_resources
import transaction
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

from intranet.model import CalEvent
from intranet.model import Order
from intranet.model import OrderPhase

VERSION = str(pkg_resources.get_distribution("intranet"))
LOG = logging.getLogger("intranet.maintenance.auto_close_orders.main")


def backup_file(path, lru=10):
    # type: (str, int) -> None
    parent, basename = os.path.split(path)
    backup_dir = os.path.join(parent, "_backups")
    if not os.path.exists(backup_dir):
        LOG.debug(u"Create the backup directory: '{backup_dir}'".format(backup_dir=backup_dir))
        os.makedirs(backup_dir)
    # create a new backup
    name, ext = os.path.splitext(basename)
    now = datetime.datetime.now()
    backup_name = "{name}.{date:%Y-%m-%d_%H%M%S}.save{ext}".format(name=name, ext=ext, date=now)
    LOG.info(u'Database backup: "{path}"...'.format(path=backup_name))
    shutil.copy2(path, os.path.join(backup_dir, backup_name))
    # keep only 10 backups
    pattern = os.path.join(backup_dir, "{name}.*.save{ext}".format(name=name, ext=ext))
    existing = sorted(glob.glob(pattern))
    for old_path in existing[:-lru]:
        LOG.debug(u"Remove old backup file: '{old_path}'".format(old_path=old_path))
        os.remove(old_path)


def auto_close(db_path, time_limit):
    # type: (str, datetime.date) -> None

    backup_file(db_path)

    # -- Connect to the source database
    LOG.info(u'Connect to the database: "{path}"...'.format(path=db_path))
    source_url = "sqlite:///{path}".format(path=db_path)
    source_engine = create_engine(source_url, echo=False)

    db_session_maker = sessionmaker(
        bind=source_engine, autoflush=True, autocommit=False, extension=ZopeTransactionExtension(),
    )
    #: :type db_session: sqlalchemy.orm.session.Session
    db_session = db_session_maker()

    # Requête de recherche des commandes non clôturées
    order_uid_list = (
        item[0] for item in db_session.query(Order.uid).order_by(Order.uid).filter(Order.close_date.is_(None)).all()
    )
    for order_uid in order_uid_list:
        fmt = u"Searching tracked times for #{order_uid}..."
        LOG.info(fmt.format(order_uid=order_uid))

        # Requête de recherche de la date du dernier pointage d'une commande
        result = (
            db_session.query(Order)
            .with_entities(Order.uid, CalEvent.event_end)
            .join(OrderPhase)
            .join(CalEvent)
            .filter(CalEvent.event_end.isnot(None))
            .filter(Order.uid == order_uid)
            .order_by(CalEvent.event_end.desc())
            .first()
        )
        last_event_end = result[1] if result else time_limit
        if last_event_end < time_limit:
            fmt = u"=> Closing the order #{order_uid} at {last_event_end}."
            LOG.info(fmt.format(last_event_end=last_event_end, order_uid=order_uid))
            with transaction.manager:
                order = db_session.query(Order).get(order_uid)
                order.close_date = last_event_end
        else:
            fmt = u"=> Keeping the order #{order_uid} opened."
            LOG.info(fmt.format(order_uid=order_uid))

    LOG.warning(u'Database "{path}" updated.'.format(path=db_path))


class PathType(object):
    """
    Factory for creating Path object types
    """

    def __init__(self, file_ok=True, dir_ok=True, exists=False):
        self._file_ok = file_ok
        self._dir_ok = dir_ok
        self._exists = exists

    def __call__(self, string):
        if self._file_ok and self._exists:
            if not os.path.isfile(string):
                raise argparse.ArgumentTypeError("Missing file '{}'".format(string))
        if self._dir_ok and self._exists:
            if not os.path.isdir(string):
                raise argparse.ArgumentTypeError("Missing directory '{}'".format(string))
        return string

    def __repr__(self):
        cls = self.__class__.__name__
        fmt = "<{cls}(file_ok={self._file_ok}, dir_ok={self._dir_ok}, exists={self._exists})>"
        return fmt.format(cls=cls, self=self)


def parse_args(argv=None):
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(
        # fmt: off
        prog="auto_close_orders.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # fmt: on
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        default=0,
        help="Display user messages [default: %(default)s]",
    )
    parser.add_argument("-V", "--version", action="version", version=VERSION)
    parser.add_argument(
        "-t",
        "--time-limit",
        dest="time_limit",
        default=90,
        help="time from which a project is considered to be completed [default: %(default)s days]",
        metavar="DAYS",
    )
    parser.add_argument(
        "db_path",
        type=PathType(dir_ok=False, exists=True),
        help="Path to the database file to read",
        metavar="DB_PATH",
    )
    args = parser.parse_args(argv)
    return args


def main(argv=None):
    args = parse_args(argv)

    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(args.verbose, len(levels) - 1)]
    logging_format = "%(levelname)-7s: %(name)s: %(message)s"
    logging.basicConfig(format=logging_format, level=level)
    logging.getLogger("txn").setLevel(logging.CRITICAL)
    logging.getLogger("sqlalchemy").setLevel(level + 10)

    time_limit = datetime.datetime.now() - datetime.timedelta(days=args.time_limit)
    auto_close(args.db_path, time_limit)


if __name__ == "__main__":
    main()
