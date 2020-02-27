# -*- coding: utf-8 -*-
"""
Add planning tables

:Revision ID: e81333c7679
:Revises: 49e949166da9
:Create Date: 2015-12-15 13:38:15.642852
"""
from __future__ import unicode_literals

import datetime
import logging

import sqlalchemy.exc
import transaction
from alembic import op
from sqlalchemy.orm import sessionmaker

from intranet.maintenance.versions.v02_00.mapping import *
from intranet.maintenance.versions.v02_00.model import DeclarativeBase

# revision identifiers, used by Alembic.
revision = 'e81333c7679'
down_revision = u'49e949166da9'
branch_labels = None
depends_on = None

LOG = logging.getLogger("alembic.revision.{0}".format(revision))

Session = sessionmaker()


def _(x):
    return x


class RecordNotFoundError(StandardError):
    """
    Exception raised when a record is missing in the database. Wrong uid?...
    """

    def __init__(self, class_name, uid):
        msg_fmt = "Record #{uid} not found in {class_name} table!"
        err_msg = msg_fmt.format(class_name=class_name,
                                 uid=uid)
        super(RecordNotFoundError, self).__init__(err_msg)
        self.uid = uid


class BasicAccessor(object):
    def __init__(self, record_class, session=None):
        self.record_class = record_class
        self.class_name = self.record_class.__name__
        self.session = session

    def _get_record(self, uid):
        if isinstance(uid, basestring):
            uid = int(uid)
        elif isinstance(uid, (tuple, list)):
            uid = map(int, uid)
        record = self.session.query(self.record_class).get(uid)
        if record is None:
            raise RecordNotFoundError(self.class_name, uid)
        return record

    def _get_record_list(self, filter_cond=None, order_by_cond=None):
        query = self.session.query(self.record_class)
        if filter_cond is not None:
            if isinstance(filter_cond, (tuple, list)):
                query = query.filter(*filter_cond)
            else:
                query = query.filter(filter_cond)
        if order_by_cond is not None:
            if isinstance(order_by_cond, (tuple, list)):
                query = query.order_by(*order_by_cond)
            else:
                query = query.order_by(order_by_cond)
        return query.all()


class WeekDayAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(WeekDayAccessor, self).__init__(TargetWeekDay, session=session)

    def setup(self):
        try:
            with transaction.manager:
                # ISO iso_weekday: Monday is 1 and Sunday is 7
                self.session.add_all([
                    TargetWeekDay(1, _(u"Lundi"), _(u"Le Lundi")),
                    TargetWeekDay(2, _(u"Mardi"), _(u"Le Mardi")),
                    TargetWeekDay(3, _(u"Mercredi"), _(u"Le Mercredi")),
                    TargetWeekDay(4, _(u"Jeudi"), _(u"Le Jeudi")),
                    TargetWeekDay(5, _(u"Vendredi"), _(u"Le Vendredi")),
                    TargetWeekDay(6, _(u"Samedi"), _(u"Le Samedi")),
                    TargetWeekDay(7, _(u"Dimanche"), _(u"Le Dimanche"))
                ])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()

    def get_week_day_list(self, filter_cond=None, order_by_cond=None):
        """
        Search the records matching the given *filter* and sorted according to the given *order-by* condition.

        :param filter_cond: Matching predicate, can be a list of predicates.
        :param order_by_cond: Order-by condition, can be a list of conditions.
        :rtype: list[WeekDay]
        :return: Ordered list of WeekDay instances.
        """
        return super(WeekDayAccessor, self)._get_record_list(filter_cond, order_by_cond)


class WeekHoursAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(WeekHoursAccessor, self).__init__(TargetWeekHours, session=session)

    def setup(self):
        try:
            with transaction.manager:
                self.session.add_all([
                    TargetWeekHours(1, _(u"Grille d’horaires normales"),
                                    _(u"Grille d’horaires d’ouverture de l’entreprise"))
                ])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()

    def get_week_hours(self, uid):
        """
        Get a week_hours given its UID.

        :type uid: int or str or unicode
        :param uid: UID of the record.
        :rtype: WeekHours
        :return: The WeekHours.
        """
        return super(WeekHoursAccessor, self)._get_record(uid)

    def get_week_hours_list(self, filter_cond=None, order_by_cond=None):
        """
        Search the records matching the given *filter* and sorted according to the given *order-by* condition.

        :param filter_cond: Matching predicate, can be a list of predicates.
        :param order_by_cond: Order-by condition, can be a list of conditions.
        :rtype: list[WeekHours]
        :return: Ordered list of WeekHours instances.
        """
        return super(WeekHoursAccessor, self)._get_record_list(filter_cond, order_by_cond)


class DayPeriodAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(DayPeriodAccessor, self).__init__(TargetDayPeriod, session=session)
        self.week_hours_accessor = WeekHoursAccessor(session)

    def setup(self, week_hours_uid):
        try:
            with transaction.manager:
                week_hours = self.week_hours_accessor.get_week_hours(week_hours_uid)
                week_hours.day_period_list.extend([
                    TargetDayPeriod(1, _(u"Matin"), _(u"Horaires du matin")),
                    TargetDayPeriod(2, _(u"Après-midi"), _(u"Horaires de l’après-midi")),
                ])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()  # abort() is required here, why?...

    def get_day_period_list(self, filter_cond=None, order_by_cond=None):
        """
        Get a filtered the list of day periods.

        :param filter_cond: SQL Alchemy filter predicate.
        :param order_by_cond: SQL Alchemy Order-by condition.
        :rtype: list[DayPeriod]
        :return: list of day periods.
        """
        return self._get_record_list(filter_cond=filter_cond, order_by_cond=order_by_cond)


class HoursIntervalAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(HoursIntervalAccessor, self).__init__(TargetHoursInterval, session=session)
        self.week_hours_accessor = WeekHoursAccessor(session)
        self.day_period_accessor = DayPeriodAccessor(session)
        self.week_day_accessor = WeekDayAccessor(session)

    def get_week_hours_list(self, filter_cond=None, order_by_cond=None):
        return self.week_hours_accessor.get_week_hours_list(filter_cond, order_by_cond)

    def get_day_period_list(self, filter_cond=None, order_by_cond=None):
        return self.day_period_accessor.get_day_period_list(filter_cond, order_by_cond)

    def get_week_day_list(self, filter_cond=None, order_by_cond=None):
        return self.week_day_accessor.get_week_day_list(filter_cond, order_by_cond)

    def insert_hours_interval(self, week_day_uid, day_period_uid, start_hour, end_hour):
        with transaction.manager:
            hours_interval = TargetHoursInterval(start_hour, end_hour)
            hours_interval.week_day_uid = week_day_uid
            hours_interval.day_period_uid = day_period_uid
            self.session.add(hours_interval)

    def setup(self, week_hours_uid):
        # -- default hours intervals of the week (in local time)
        wh_dict = {1: [None,
                       (datetime.time(14, 0), datetime.time(17, 45))],
                   2: [(datetime.time(8, 30), datetime.time(12, 30)),
                       (datetime.time(14, 0), datetime.time(17, 45))],
                   3: [(datetime.time(8, 30), datetime.time(12, 30)),
                       (datetime.time(14, 0), datetime.time(17, 45))],
                   4: [(datetime.time(8, 30), datetime.time(12, 30)),
                       (datetime.time(14, 0), datetime.time(17, 45))],
                   5: [(datetime.time(8, 30), datetime.time(12, 30)),
                       (datetime.time(14, 0), datetime.time(17, 30))],
                   6: [(datetime.time(8, 30), datetime.time(12, 30)),
                       None],
                   7: []}
        try:
            with transaction.manager:
                week_hours = self.week_hours_accessor.get_week_hours(week_hours_uid)
                week_days = {wd.iso_weekday: wd for wd in self.get_week_day_list()}
                day_periods = {dp.position: dp for dp in week_hours.day_period_list}
                for weekday, periods in wh_dict.iteritems():
                    for position, interval in enumerate(periods, 1):
                        if interval:
                            self.insert_hours_interval(week_days[weekday].uid,
                                                       day_periods[position].uid,
                                                       start_hour=interval[0],
                                                       end_hour=interval[1])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()  # abort() is required here, why?...


class CalendarAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(CalendarAccessor, self).__init__(TargetCalendar, session=session)
        self.week_hours_accessor = WeekHoursAccessor(session)

    def setup(self, week_hours_uid):
        LOG.info(u"Setup the default calendar...")
        try:
            with transaction.manager:
                week_hours = self.week_hours_accessor.get_week_hours(week_hours_uid)
                week_hours.calendar_list.extend([
                    TargetCalendar(1, _(u"Calendrier principal"),
                                   _(u"Calendrier principal commun à toute de l’entreprise"))
                ])
        except sqlalchemy.exc.IntegrityError as exc:
            LOG.warning(exc)
            # setup already done.
            transaction.abort()

    def get_week_hours(self, week_hours_uid):
        return self.week_hours_accessor.get_week_hours(week_hours_uid)

    def get_week_hours_list(self, filter_cond=None, order_by_cond=None):
        return self.week_hours_accessor.get_week_hours_list(filter_cond=filter_cond, order_by_cond=order_by_cond)


class FrequencyAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(FrequencyAccessor, self).__init__(TargetFrequency, session=session)

    def setup(self):
        try:
            with transaction.manager:
                self.session.add_all([
                    TargetFrequency(_("Apériodique"), _("Horaires valables toute l'année"), 0, 1),
                    TargetFrequency(_("Semaines impaires"), _("Horaires valables les semaines impaires"), 1, 2),
                    TargetFrequency(_("Semaines paires"), _("Horaires valables les semaines paires"), 0, 2)
                ])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()


class PlanningEventAccessor(BasicAccessor):
    def __init__(self, session=None):
        super(PlanningEventAccessor, self).__init__(TargetPlanningEvent, session=session)
        self.calendar_accessor = CalendarAccessor(session)

    def setup(self):
        try:
            with transaction.manager:
                self.session.add_all([])
        except sqlalchemy.exc.IntegrityError:
            # setup already done.
            transaction.abort()  # abort() is required here, why?...


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
