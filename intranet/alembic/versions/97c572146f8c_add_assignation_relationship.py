"""
Add assignation relationship (to OrderPhase and Employee)

:Revision ID: 97c572146f8c
:Revises: 7cd2e08fbea8
:Create Date: 2016-01-18 10:34:37.120199
"""
from __future__ import unicode_literals

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '97c572146f8c'
down_revision = u'7cd2e08fbea8'
branch_labels = None
depends_on = None


def upgrade():
    columns = [sa.Column("uid", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
               sa.Column("employee_uid", sa.Integer, sa.ForeignKey('Employee.uid',
                                                                   ondelete='CASCADE',
                                                                   onupdate='CASCADE'),
                         nullable=True, index=True),
               sa.Column("order_phase_uid", sa.Integer, sa.ForeignKey('OrderPhase.uid',
                                                                      ondelete='CASCADE',
                                                                      onupdate='CASCADE'),
                         nullable=True, index=True),
               sa.Column("assigned_hours", sa.Float, nullable=False),
               sa.Column("rate_percent", sa.Float, nullable=False),
               sa.Column("start_date", sa.DateTime, nullable=False),
               sa.Column("end_date", sa.DateTime, nullable=True),

               sa.UniqueConstraint('employee_uid', 'order_phase_uid',
                                   name="order_phase_employee_unique"),
               sa.CheckConstraint("0.0 <= assigned_hours",
                                  name="assigned_hours_check"),
               sa.CheckConstraint("0.0 <= rate_percent AND rate_percent <= 1.0",
                                  name="rate_interval_check"),
               sa.CheckConstraint("end_date IS NULL OR (start_date <= end_date)",
                                  name="date_interval_check")

               ]

    op.create_table('Assignation', *columns)


def downgrade():
    op.drop_table("Assignation")
