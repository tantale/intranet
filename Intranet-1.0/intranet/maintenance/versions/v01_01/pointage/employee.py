"""
:Module: intranet.maintenance.versions.v01_01.pointage.employee
:Created on: 2014-05-02
:Author: Tantale Solutions <tantale.solutions@gmail.com>
"""
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Date

from intranet.maintenance.versions.v01_01.model import DeclarativeBase


class Employee(DeclarativeBase):
    """Employee management."""
    __tablename__ = 'Employee'

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    employee_name = Column(String(length=50), unique=True, nullable=False,
                           index=True)
    worked_hours = Column(Integer, nullable=False)
    entry_date = Column(Date, nullable=False, index=True)
    exit_date = Column(Date, nullable=True, index=True)
    photo_path = Column(String(length=200), nullable=True)

    def __init__(self, employee_name, worked_hours, entry_date,
                 exit_date=None, photo_path=None):
        """
        Initialize employee's information.

        :param employee_name: employee's name (unique and not null)

        :param worked_hours: weekly worked hours (required), eg.: 39 h/week
        :type worked_hours: int

        :param entry_date: entry date in the company (required)
        :type entry_date: datetime.date

        :param exit_date: exit date from the company, or None if still active
        :type exit_date: datetime.date

        :param photo_path: photo path of the employee if any, or None
        """
        self.employee_name = employee_name
        self.worked_hours = worked_hours
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.photo_path = photo_path

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.employee_name!r}, "
                    "{self.worked_hours!r}, "
                    "{self.entry_date!r}, "
                    "exit_date={self.exit_date!r}, "
                    "photo_path={self.photo_path!r})")
        return repr_fmt.format(self=self)
