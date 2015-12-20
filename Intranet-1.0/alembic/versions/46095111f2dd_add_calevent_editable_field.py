"""
Add CalEvent.editable field

:Revision ID: 46095111f2dd
:Revises: 
:Create Date: 2015-12-15 13:37:16.822293
"""
from __future__ import unicode_literals

import datetime
import logging

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '46095111f2dd'
down_revision = None
branch_labels = None
depends_on = None

LOG = logging.getLogger("alembic.revision.{0}".format(revision))


def create_old_record(entry):
    record = dict(uid=entry[0],
                  employee_uid=entry[1],
                  order_phase_uid=entry[2],
                  event_start=parse_iso_datetime(entry[3]),
                  event_end=parse_iso_datetime(entry[4]),
                  comment=entry[5])
    LOG.info(record)
    return record


def create_new_record(entry):
    record = dict(uid=entry[0],
                  employee_uid=entry[1],
                  order_phase_uid=entry[2],
                  event_start=parse_iso_datetime(entry[3]),
                  event_end=parse_iso_datetime(entry[4]),
                  comment=entry[5])
    if len(entry) == 6:
        record.update(editable=True)
    elif len(entry) == 7:
        record.update(editable=entry[6])
    else:
        raise ValueError(entry)
    LOG.info(record)
    return record


def parse_iso_datetime(date_string):
    if date_string is None:
        return None
    return datetime.datetime.strptime(date_string[:19], "%Y-%m-%d %H:%M:%S")


def upgrade():
    connection = op.get_bind()
    res = connection.execute("SELECT * FROM CalEvent")
    records = res.fetchall()

    op.drop_table("CalEvent")

    columns = [sa.Column("uid", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
               sa.Column("employee_uid", sa.Integer, sa.ForeignKey('Employee.uid',
                                                                   ondelete='CASCADE',
                                                                   onupdate='CASCADE'), nullable=True, index=True),
               sa.Column("order_phase_uid", sa.Integer, sa.ForeignKey('OrderPhase.uid',
                                                                      ondelete='CASCADE',
                                                                      onupdate='CASCADE'), nullable=True, index=True),
               sa.Column("event_start", sa.DateTime, nullable=False, index=True),
               sa.Column("event_end", sa.DateTime, nullable=False, index=True),
               sa.Column("comment", sa.String(length=200), nullable=True),
               sa.Column("editable", sa.Boolean(), nullable=True, default=True)]

    employee_table = op.create_table('CalEvent', *columns)

    new_records = map(create_new_record, records)

    op.bulk_insert(employee_table, new_records)


def downgrade():
    connection = op.get_bind()
    res = connection.execute("SELECT * FROM CalEvent")
    records = res.fetchall()

    op.drop_table("CalEvent")

    columns = [sa.Column("uid", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
               sa.Column("employee_uid", sa.Integer, sa.ForeignKey('Employee.uid',
                                                                   ondelete='CASCADE',
                                                                   onupdate='CASCADE'), nullable=True, index=True),
               sa.Column("order_phase_uid", sa.Integer, sa.ForeignKey('OrderPhase.uid',
                                                                      ondelete='CASCADE',
                                                                      onupdate='CASCADE'), nullable=True, index=True),
               sa.Column("event_start", sa.DateTime, nullable=False, index=True),
               sa.Column("event_end", sa.DateTime, nullable=False, index=True),
               sa.Column("comment", sa.String(length=200), nullable=True)]

    employee_table = op.create_table('CalEvent', *columns)

    new_records = map(create_old_record, records)

    op.bulk_insert(employee_table, new_records)


