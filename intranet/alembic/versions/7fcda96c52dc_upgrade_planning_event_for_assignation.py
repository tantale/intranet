"""
Upgrade PlanningEvent for Assignation

:Revision ID: 7fcda96c52dc
:Revises: 97c572146f8c
:Create Date: 2016-01-18 10:42:36.658318
"""
from __future__ import unicode_literals

import datetime
import logging

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7fcda96c52dc'
down_revision = u'97c572146f8c'
branch_labels = None
depends_on = None

LOG = logging.getLogger("alembic.revision.{0}".format(revision))


def parse_iso_datetime(date_string):
    if date_string is None:
        return None
    return datetime.datetime.strptime(date_string[:19], "%Y-%m-%d %H:%M:%S")


def create_old_record(entry):
    record = dict(uid=entry[0],
                  label=entry[1],
                  description=entry[2],
                  event_start=parse_iso_datetime(entry[3]),
                  event_end=parse_iso_datetime(entry[4]),
                  editable=bool(entry[5]),
                  all_day=bool(entry[6]),
                  location=entry[7],
                  private=bool(entry[8]),
                  calendar_uid=entry[9])
    LOG.info(record)
    return record


def create_new_record(entry):
    record = dict(uid=entry[0],
                  label=entry[1],
                  description=entry[2],
                  event_start=parse_iso_datetime(entry[3]),
                  event_end=parse_iso_datetime(entry[4]),
                  editable=bool(entry[5]),
                  all_day=bool(entry[6]),
                  location=entry[7],
                  private=bool(entry[8]),
                  calendar_uid=entry[9],
                  assignation_uid=None)
    LOG.info(record)
    return record


OLD_COLUMNS = [
    sa.Column("uid", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
    sa.Column("label", sa.String(length=32), unique=False, nullable=False),
    sa.Column("description", sa.String(length=200)),
    sa.Column("event_start", sa.DateTime, nullable=False, index=True),
    sa.Column("event_end", sa.DateTime, nullable=False, index=True),
    sa.Column("editable", sa.Boolean(), nullable=False, default=True),
    sa.Column("all_day", sa.Boolean(), nullable=False, default=False),
    sa.Column("location", sa.String(length=200)),
    sa.Column("private", sa.Boolean(), nullable=False, default=False),
    sa.Column("calendar_uid", sa.Integer, sa.ForeignKey('Calendar.uid',
                                                        ondelete='CASCADE',
                                                        onupdate='CASCADE'),
              nullable=False, index=True)]

NEW_COLUMNS = OLD_COLUMNS + [sa.Column("assignation_uid", sa.Integer, sa.ForeignKey('Assignation.uid',
                                                                                    ondelete='CASCADE',
                                                                                    onupdate='CASCADE'),
                                       nullable=True, index=True),
                             sa.CheckConstraint("event_start <= event_end",
                                                name="start_before_end_check"),
                             sa.UniqueConstraint('calendar_uid', 'event_start', 'event_end',
                                                 name="dates_unique"),
                             ]


def upgrade():
    connection = op.get_bind()
    res = connection.execute("SELECT * FROM PlanningEvent")
    records = res.fetchall()

    op.drop_table("PlanningEvent")
    table = op.create_table('PlanningEvent', *NEW_COLUMNS)

    updated_records = map(create_new_record, records)
    op.bulk_insert(table, updated_records)


def downgrade():
    connection = op.get_bind()
    res = connection.execute("SELECT * FROM PlanningEvent")
    records = res.fetchall()

    op.drop_table("PlanningEvent")
    table = op.create_table('PlanningEvent', *OLD_COLUMNS)

    updated_records = map(create_old_record, records)
    op.bulk_insert(table, updated_records)
