"""
Add Order Phase description

:Revision ID: 17ec5aac4ab4
:Revises: 62355bae7318
:Create Date: 2016-02-14 21:45:50.305657
"""
from __future__ import unicode_literals

import logging

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '17ec5aac4ab4'
down_revision = u'62355bae7318'
branch_labels = None
depends_on = None

LOG = logging.getLogger("alembic.revision.{0}".format(revision))

STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE = "PENDING", "IN_PROGRESS", "DONE"
ALL_TASK_STATUS = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE]


def parse_float(value):
    if value is None:
        return value
    return float(value)


OLD_COLUMNS = [
    sa.Column("uid", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
    sa.Column("order_uid", sa.Integer, sa.ForeignKey('Order.uid', ondelete='CASCADE', onupdate='CASCADE'),
              nullable=False, index=True),
    sa.Column("position", sa.Integer, nullable=False),
    sa.Column("label", sa.String(length=50), nullable=False),
    sa.Column("estimated_duration", sa.Float, nullable=True),
    sa.Column("remain_duration", sa.Float, nullable=True),
    sa.Column("task_status", sa.Enum(*ALL_TASK_STATUS), nullable=False, default=STATUS_PENDING)
]


def create_old_record(entry):
    record = dict(uid=entry[0],
                  order_uid=int(entry[1]),
                  position=int(entry[2]),
                  label=entry[3],
                  # description
                  estimated_duration=parse_float(entry[5]),
                  remain_duration=parse_float(entry[6]),
                  task_status=entry[7])
    LOG.info(record)
    return record


NEW_COLUMNS = [
    sa.Column("uid", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
    sa.Column("order_uid", sa.Integer, sa.ForeignKey('Order.uid', ondelete='CASCADE', onupdate='CASCADE'),
              nullable=False, index=True),
    sa.Column("position", sa.Integer, nullable=False),
    sa.Column("label", sa.String(length=50), nullable=False),
    sa.Column("description", sa.String(length=200), nullable=True),
    sa.Column("estimated_duration", sa.Float, nullable=True),
    sa.Column("remain_duration", sa.Float, nullable=True),
    sa.Column("task_status", sa.Enum(*ALL_TASK_STATUS), nullable=False, default=STATUS_PENDING)
]


def create_new_record(entry):
    record = dict(uid=entry[0],
                  order_uid=int(entry[1]),
                  position=int(entry[2]),
                  label=entry[3],
                  description=None,
                  estimated_duration=parse_float(entry[4]),
                  remain_duration=parse_float(entry[5]),
                  task_status=entry[6])
    LOG.info(record)
    return record


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
