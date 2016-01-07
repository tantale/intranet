"""
drop 'migrate_version' table (replaced by 'alembic_version')

:Revision ID: 7cd2e08fbea8
:Revises: 4fdb94101eb3
:Create Date: 2016-01-07 14:22:00.978337
"""
from __future__ import unicode_literals

import sqlalchemy as sa
import sqlalchemy.exc as exc
from alembic import op

# revision identifiers, used by Alembic.
revision = '7cd2e08fbea8'
down_revision = u'4fdb94101eb3'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.drop_table("migrate_version")
    except exc.OperationalError:
        pass


def downgrade():
    migrate_version = op.create_table("migrate_version",
                                      sa.Column('repository_id', sa.VARCHAR(length=250), primary_key=True,
                                                nullable=False),
                                      sa.Column('repository_path', sa.TEXT()),
                                      sa.Column('version', sa.INTEGER()))
    records = [{"repository_id": "migration",
                "version": 0,
                "repository_path": "migration"}]
    op.bulk_insert(migrate_version, records)
