# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import argparse
import contextlib
import datetime
import io
import json

import transaction
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.sqltypes import *
from zope.sqlalchemy.datamanager import ZopeTransactionExtension


def import_database(connection_uri, *json_paths):
    """
    Export all records to files using JSON syntax

    :param connection_uri: SQLAlchemy's connection URI
    :param json_paths: target directory
    """
    # -- First we connect to the database to introspect the existing tables
    print("Connect to {0}...".format(connection_uri))
    engine = create_engine(connection_uri, echo=False)

    # -- We produce our own MetaData object
    metadata = MetaData()

    # -- We use `reflect` to introspect the tables
    # we can reflect it ourselves from a database, using options
    # such as 'only' to limit what tables we look at...
    metadata.reflect(engine)

    # -- We prepare a new session
    session_maker = sessionmaker(bind=engine,
                                 autoflush=True,
                                 autocommit=False,
                                 extension=ZopeTransactionExtension())

    with contextlib.closing(session_maker()) as session:
        for json_path in json_paths:
            with io.open(json_path, mode="rb") as fd:
                table_obj = json.loads(fd.read())

            table = metadata.tables[table_obj["name"]]
            print("Import in '{0}' table:".format(table.name))

            for record_obj in table_obj["records"]:
                values = []
                for column in table.columns:
                    value = record_obj[column.name]
                    if value is None:
                        values.append(value)
                    elif isinstance(column.type, (BOOLEAN, INTEGER, SMALLINT, VARCHAR)):
                        values.append(value)
                    elif isinstance(column.type, DATETIME):
                        values.append(datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S"))
                    elif isinstance(column.type, DATE):
                        values.append(datetime.datetime.strptime(value, "%Y-%m-%d").date())
                    elif isinstance(column.type, TIME):
                        values.append(datetime.datetime.strptime(value, "%H:%M:%S").time())
                    else:
                        raise ValueError(column.type)
                try:
                    with transaction.manager:
                        session.execute(table.insert(values))
                    print("- Imported: " + repr(values))
                except IntegrityError:
                    print("- Ignored:  " + repr(values))
                except Exception:
                    print("ERROR: " + repr(values))
                    print("Values are: " + repr(record_obj))
                    raise


def main():
    parser = argparse.ArgumentParser(description="Import JSON data in database")
    parser.add_argument("db_path", help="SQLITE database path")
    parser.add_argument("json_paths", nargs='+', help="Path to JSON file to load")
    args = parser.parse_args()
    connection_uri = 'sqlite:///{path}'.format(path=args.db_path)
    import_database(connection_uri, *args.json_paths)


if __name__ == '__main__':
    main()
