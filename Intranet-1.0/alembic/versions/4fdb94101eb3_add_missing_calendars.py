"""
Add missing calendars: one for each employee

:Revision ID: 4fdb94101eb3
:Revises: e81333c7679
:Create Date: 2015-12-20 08:59:07.343836
"""
from __future__ import unicode_literals

import logging
import random

import sqlalchemy.exc as exc
from alembic import op
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import func

from intranet.maintenance.versions.v02_00.model import DeclarativeBase
from intranet.maintenance.versions.v02_00.planning.calendar import Calendar
from intranet.maintenance.versions.v02_00.planning.week_hours import WeekHours
from intranet.maintenance.versions.v02_00.pointage.employee import Employee

#: revision identifiers, used by Alembic.
revision = '4fdb94101eb3'
down_revision = u'e81333c7679'
branch_labels = None
depends_on = None


LOG = logging.getLogger("alembic.revision.{0}".format(revision))

Session = sessionmaker()


class Updater(object):
    def __init__(self, session):
        self.session = session
        self.background_colors = [
            "#ffdfdf", "#ffdbfb", "#e6dbff", "#e0eaf8", "#c0f7fe", "#caffd8", "#ffffd7", "#ffeab7"]
        self.text_color = "#000000"

    def attach_new_calendar(self, employee):
        # -- Create a new Calendar and attach it to the newly created employee
        week_hours_list = self.session.query(WeekHours).all()
        if week_hours_list:
            week_hours = week_hours_list[0]

            # -- Create the "best" label for this calendar
            label = employee.employee_name

            calendar_list = self.session.query(Calendar).filter(Calendar.label.like(u"%{0}%".format(label))).all()
            existing_labels = frozenset(c.label for c in calendar_list)
            if label in existing_labels:
                count = len(existing_labels) + 1
                label_fmt = u"{employee_name} ({count})"
                label = label_fmt.format(employee_name=employee.employee_name, count=count)
                while label in existing_labels:
                    count += 1
                    count = len(existing_labels) + 1
                    label = label_fmt.format(employee_name=employee.employee_name, count=count)

            description = u"Calendrier de {0}".format(label)
            try:
                background_color = random.choice(self.background_colors)
                last_position = self.session.query(func.max(Calendar.position)).scalar() or 0
                calendar = Calendar(last_position + 1, label, description,
                                    background_color, background_color, self.text_color)
                calendar.week_hours = week_hours
                calendar.employee = employee
                self.session.add(calendar)
                self.session.commit()
            except exc.IntegrityError:
                self.session.abort()
                raise

    def delete_calendar(self, employee):
        try:
            calendar = employee.calendar
            employee.calendar = None
            self.session.delete(calendar)
            self.session.commit()
        except exc.IntegrityError:
            self.session.abort()
            raise


def upgrade():
    bind = op.get_bind()
    DeclarativeBase.metadata.create_all(bind=bind)

    session = Session(bind=bind)
    session._model_changes = False  # if you are using Flask-SQLAlchemy, this works around a bug
    updater = Updater(session)

    # noinspection PyComparisonWithNone
    employee_list = session.query(Employee).filter(Employee.calendar == None).all()
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
    employee_list = session.query(Employee).filter(Employee.calendar == None).all()
    for employee in employee_list:
        LOG.info(u"Delete the calendar from {employee_name}".format(employee_name=employee.employee_name))
        updater.delete_calendar(employee)
