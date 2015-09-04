"""
:module: intranet.model.pointage.employee
:date: 2013-07-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from sqlalchemy.types import String, Float
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Date

from intranet.model import DeclarativeBase


class Employee(DeclarativeBase):
    """
    Employee management.

    .. versionadded:: 1.2.0
        - The UID is the personal ID.
        - The name 'employee_name' isn't anymore unique: we tolerate duplicated names.
        - The worked hours field can be a decimal value, eg.: 31.2 hours.
    """
    __tablename__ = 'Employee'

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    employee_name = Column(String(length=50), unique=False, nullable=False,
                           index=True)
    worked_hours = Column(Float, nullable=False)
    entry_date = Column(Date, nullable=False, index=True)
    exit_date = Column(Date, nullable=True, index=True)
    photo_path = Column(String(length=200), nullable=True)

    # todo: implement the *worked_hours* relationship in Employee table
    #
    # worked_hours_uid = Column(Integer, ForeignKey('Calendar.uid',
    #                                             ondelete='CASCADE',
    #                                             onupdate='CASCADE'),
    #                         nullable=True)
    #
    # worked_hours = relationship('Calendar',
    #                           backref=backref('employee_list',
    #                                           cascade='all,delete-orphan'))

    def __init__(self, employee_name, worked_hours, entry_date,
                 exit_date=None, photo_path=None):
        """
        Initialize employee's information.

        :param employee_name: employee's name (unique and not null)

        :param worked_hours: weekly worked hours (required), eg.: 39 h/week
        :type worked_hours: float

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
