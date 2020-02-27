"""
Fix OrderCat CSS values

:Revision ID: 49e949166da9
:Revises: 46095111f2dd
:Create Date: 2015-12-15 13:37:57.122273
"""
from __future__ import unicode_literals

import logging

import sqlalchemy as sa
import sqlalchemy.sql as sql
from alembic import op

# revision identifiers, used by Alembic.
revision = '49e949166da9'
down_revision = u'46095111f2dd'
branch_labels = None
depends_on = None

LOG = logging.getLogger("alembic.revision.{0}".format(revision))

order_cat = sql.table("OrderCat",
                      sql.column("uid", sa.Integer),
                      sql.column("css_def", sa.String(length=200)))


def upgrade():
    connection = op.get_bind()
    res = connection.execute("SELECT uid, css_def FROM OrderCat")
    map(upgrade_order_cat, res.fetchall())


def downgrade():
    connection = op.get_bind()
    res = connection.execute("SELECT uid, css_def FROM OrderCat")
    map(downgrade_order_cat, res.fetchall())


def update_css_def(uid, css_def):
    values = {'css_def': op.inline_literal(css_def)}
    stmt = order_cat.update().where(order_cat.c.uid == uid).values(values)
    LOG.info(stmt)
    op.execute(stmt)


def upgrade_order_cat(record):
    uid, css_def = record
    new_css_def = css_def.replace("white", "#ffffff").replace("black", "#000000")
    if css_def != new_css_def:
        update_css_def(uid, new_css_def)


def downgrade_order_cat(record):
    uid, css_def = record
    new_css_def = css_def.replace("#ffffff", "white").replace("#000000", "black")
    if css_def != new_css_def:
        update_css_def(uid, new_css_def)
