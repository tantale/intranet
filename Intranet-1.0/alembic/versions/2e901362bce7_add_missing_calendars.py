"""
add missing calendars

:Revision ID: 2e901362bce7
:Revises: e81333c7679
:Create Date: 2015-12-20 08:01:52.007411
"""
from __future__ import unicode_literals

import logging

import sqlalchemy as sa
import sqlalchemy.exc as exc
import sqlalchemy.sql as sql
import transaction
from alembic import op
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
revision = '2e901362bce7'
down_revision = u'e81333c7679'
branch_labels = None
depends_on = None


LOG = logging.getLogger("alembic.revision.{0}".format(revision))

Session = sessionmaker()


class Updater(object):
    def __init__(self, session):
        self.session = session
        self.week_hours_accessor = WeekHoursAccessor(session)
        self.calendar_accessor = CalendarAccessor(session)

    def attach_new_calendar(self, employee):
        # -- Create a new Calendar and attach it to the newly created employee
        week_hours_list = self.week_hours_accessor.get_week_hours_list()
        if week_hours_list:
            week_hours = week_hours_list[0]

            # -- Create the "best" label for this calendar
            label = employee.employee_name
            calendar_list = self.calendar_accessor.get_calendar_list(Calendar.label.like(u"%{0}%".format(label)))
            existing_labels = frozenset(c.label for c in calendar_list)
            if label in existing_labels:
                count = len(existing_labels) + 1
                label_fmt = u"{employee_name} ({count})"
                label = label_fmt.format(employee_name=employee.employee_name, count=count)
                while label in existing_labels:
                    count += 1
                    count = len(existing_labels) + 1
                    label = label_fmt.format(employee_name=employee.employee_name, count=count)
            self.calendar_accessor.insert_calendar(week_hours_uid=week_hours.uid,
                                                   label=label,
                                                   description=u"Calendrier de {0}".format(label))
            calendar = self.calendar_accessor.get_by_label(label)
            try:
                with transaction.manager:
                    employee.calendar=calendar
            except exc.IntegrityError:
                transaction.abort()
                raise

    def delete_calendar(self, employee):
        try:
            with transaction.manager:
                calendar = employee.calendar
                employee.calendar=None
                self.session.delete(calendar)
        except exc.IntegrityError:
            transaction.abort()
            raise


def upgrade():
    bind = op.get_bind()
    DeclarativeBase.metadata.create_all(bind=bind)

    session = Session(bind=bind)
    session._model_changes = False  # if you are using Flask-SQLAlchemy, this works around a bug
    updater = Updater(session)

    # noinspection PyComparisonWithNone
    employee_list = session.query(TargetEmployee).filter(TargetEmployee.calendar == None).all()
    for employee in employee_list:
        LOG.info(u"Attach a new calendar to {employee_name}".format(employee_name=employee.employee_name))
        updater.attach_new_calendar(employee)


def downgrade():
    bind = op.get_bind()
    DeclarativeBase.metadata.create_all(bind=bind)

    session = Session(bind=bind)
    session._model_changes = False  # if you are using Flask-SQLAlchemy, this works around a bug
    updater = Updater(session)

    # noinspection PyComparisonWithNone
    employee_list = session.query(TargetEmployee).filter(TargetEmployee.calendar == None).all()
    for employee in employee_list:
        LOG.info(u"Delete the calendar from {employee_name}".format(employee_name=employee.employee_name))
        updater.delete_calendar(employee)
