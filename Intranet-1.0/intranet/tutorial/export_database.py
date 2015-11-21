# -*- coding: utf-8 -*-
"""
Demonstration: How to export a database in JSON
"""
from __future__ import unicode_literals, print_function

import argparse
import contextlib
import datetime
import io
import json
import os

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
            return obj.isoformat()

        return super(DatetimeEncoder, self).default(obj)


def export_database(connection_uri, json_dir):
    """
    Export all records to files using JSON syntax

    :param connection_uri: SQLAlchemy's connection URI
    :param json_dir: target directory
    """

    # -- First we connect to the database to introspect the existing tables
    engine = create_engine(connection_uri, echo=False)

    # -- We produce our own MetaData object
    metadata = MetaData()

    # -- We use `reflect` to introspect the tables
    # we can reflect it ourselves from a database, using options
    # such as 'only' to limit what tables we look at...
    metadata.reflect(engine)

    # -- We convert the metadata to a JSON file
    schema_obj = dict(connection_uri=connection_uri,
                      sorted_tables=[])
    for table in metadata.sorted_tables:
        table_obj = dict(name=table.name,
                         columns=[repr(column) for column in table.columns])
        schema_obj["sorted_tables"].append(table_obj)

    metadata_json = os.path.join(json_dir, "__metadata__.json")
    if not os.path.isdir(json_dir):
        os.makedirs(json_dir)
    print("Writing '{path}'...".format(path=metadata_json))
    with io.open(metadata_json, mode="wb") as fd:
        fd.write(json.dumps(schema_obj, indent=4))

    # -- We dump each table records
    session_maker = sessionmaker(bind=engine,
                                 autoflush=True,
                                 autocommit=False,
                                 extension=ZopeTransactionExtension())

    with contextlib.closing(session_maker()) as session:
        for table in metadata.sorted_tables:
            names = [column.name for column in table.columns]
            records = session.query(table).all()
            table_obj = dict(name=table.name,
                             records=[dict(zip(names, record)) for record in records])
            table_json = os.path.join(json_dir, table.name + ".json")
            print("Writing '{path}'...".format(path=table_json))
            with io.open(table_json, mode="wb") as fd:
                fd.write(json.dumps(table_obj, indent=4, cls=DatetimeEncoder))


def main():
    parser = argparse.ArgumentParser(description="Export database to JSON data")
    parser.add_argument("db_path", help="SQLITE database path")
    parser.add_argument("json_dir", help="Folder path used to store JSON files")
    args = parser.parse_args()
    connection_uri = 'sqlite:///{path}'.format(path=args.db_path)
    export_database(connection_uri, args.json_dir)


if __name__ == '__main__':
    main()
