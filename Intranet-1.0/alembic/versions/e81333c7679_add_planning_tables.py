"""
Add planning tables

:Revision ID: e81333c7679
:Revises: 49e949166da9
:Create Date: 2015-12-15 13:38:15.642852
"""
from __future__ import unicode_literals

import logging

from alembic import op
from sqlalchemy.orm import sessionmaker

from intranet.maintenance.versions.v02_00.model import DeclarativeBase
# noinspection PyUnresolvedReferences
from intranet.maintenance.versions.v02_00.mapping import *

from intranet.accessors.planning.calendar import CalendarAccessor
from intranet.accessors.planning.day_period import DayPeriodAccessor
from intranet.accessors.planning.frequency import FrequencyAccessor
from intranet.accessors.planning.hours_interval import HoursIntervalAccessor
from intranet.accessors.planning.planning_event import PlanningEventAccessor
from intranet.accessors.planning.week_day import WeekDayAccessor
from intranet.accessors.planning.week_hours import WeekHoursAccessor

# revision identifiers, used by Alembic.
revision = 'e81333c7679'
down_revision = u'49e949166da9'
branch_labels = None
depends_on = None

LOG = logging.getLogger("alembic.revision.{0}".format(revision))

Session = sessionmaker()


def upgrade():
    LOG.info("Create new tables...")
    bind = op.get_bind()
    DeclarativeBase.metadata.create_all(bind=bind)

    session = Session(bind=bind)
    session._model_changes = False  # if you are using Flask-SQLAlchemy, this works around a bug

    week_day_accessor = WeekDayAccessor(session)
    week_hours_accessor = WeekHoursAccessor(session)
    day_period_accessor = DayPeriodAccessor(session)
    hours_interval_accessor = HoursIntervalAccessor(session)
    calendar_accessor = CalendarAccessor(session)
    frequency_accessor = FrequencyAccessor(session)
    planning_event_accessor = PlanningEventAccessor(session)

    LOG.info("Setup with default records...")
    week_day_accessor.setup()
    week_hours_accessor.setup()
    week_hours_list = week_hours_accessor.get_week_hours_list()
    for week_hours in week_hours_list:
        day_period_accessor.setup(week_hours.uid)
        hours_interval_accessor.setup(week_hours.uid)
        calendar_accessor.setup(week_hours.uid)
    frequency_accessor.setup()
    planning_event_accessor.setup()

    LOG.info("Commit.")
    session.commit()
    LOG.info("Done.")


def downgrade():
    LOG.info("Drop the tables...")
    bind = op.get_bind()
    DeclarativeBase.metadata.drop_all(bind=bind, tables=[
        TargetWeekDay.__table__,
        TargetWeekHours.__table__,
        TargetDayPeriod.__table__,
        TargetHoursInterval.__table__,
        TargetFrequency.__table__,
        TargetCalendar.__table__,
        TargetYearPeriod.__table__,
        TargetPlanningEvent.__table__])
    LOG.info("Done.")
