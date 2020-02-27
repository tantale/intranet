"""
Upgrade Order Phase for Assignation

:Revision ID: 62355bae7318
:Revises: 7fcda96c52dc
:Create Date: 2016-01-18 11:02:50.821546
"""
from __future__ import unicode_literals

import datetime
import logging

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '62355bae7318'
down_revision = u'7fcda96c52dc'
branch_labels = None
depends_on = None

LOG = logging.getLogger("alembic.revision.{0}".format(revision))


def parse_iso_datetime(date_string):
    if date_string is None:
        return None
    return datetime.datetime.strptime(date_string[:19], "%Y-%m-%d %H:%M:%S")


def create_old_record(entry):
    record = dict(uid=entry[0],
                  order_uid=entry[1],
                  position=entry[2],
                  label=entry[3])
    LOG.info(record)
    return record


def create_new_record(entry):
    record = dict(uid=entry[0],
                  order_uid=entry[1],
                  position=entry[2],
                  label=entry[3],
                  estimated_duration=None,
                  remain_duration=None,
                  task_status=STATUS_PENDING)
    LOG.info(record)
    return record


STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE = "PENDING", "IN_PROGRESS", "DONE"
ALL_STATUS = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE]

OLD_COLUMNS = [
    sa.Column("uid", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
    sa.Column("order_uid", sa.Integer, sa.ForeignKey('Order.uid',
                                                     ondelete='CASCADE',
                                                     onupdate='CASCADE'),
              nullable=False, index=True),
    sa.Column("position", sa.Integer, nullable=False),
    sa.Column("label", sa.String(length=50), nullable=False)]

NEW_COLUMNS = OLD_COLUMNS + [
    sa.Column("estimated_duration", sa.Float, nullable=True),
    sa.Column("remain_duration", sa.Float, nullable=True),
    sa.Column("task_status", sa.Enum(*ALL_STATUS), nullable=False, default=STATUS_PENDING),
    sa.CheckConstraint("position > 0", name="position_check")
]


def upgrade():
    connection = op.get_bind()
    res = connection.execute("SELECT * FROM OrderPhase")
    records = res.fetchall()

    op.drop_table("OrderPhase")
    table = op.create_table('OrderPhase', *NEW_COLUMNS)

    updated_records = map(create_new_record, records)
    op.bulk_insert(table, updated_records)


def downgrade():
    connection = op.get_bind()
    res = connection.execute("SELECT * FROM OrderPhase")
    records = res.fetchall()

    op.drop_table("OrderPhase")
    table = op.create_table('OrderPhase', *OLD_COLUMNS)

    updated_records = map(create_old_record, records)
    op.bulk_insert(table, updated_records)
