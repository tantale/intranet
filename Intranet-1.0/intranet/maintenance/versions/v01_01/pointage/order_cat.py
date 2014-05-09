"""
:Module: intranet.maintenance.versions.v01_01.pointage.order_cat
:Created on: 2014-05-02
:Author: Tantale Solutions <tantale.solutions@gmail.com>
"""
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from intranet.maintenance.versions.v01_01.model import DeclarativeBase


class OrderCat(DeclarativeBase):
    """
    Order category
    """
    __tablename__ = 'OrderCat'

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    cat_name = Column(String(length=50), unique=True, nullable=False, index=True)  # @IgnorePep8
    cat_group = Column(String(length=50), nullable=False, index=True)
    label = Column(String(length=50), nullable=False)
    css_def = Column(String(length=200), nullable=False)

    def __init__(self, cat_name, cat_group, label, css_def):
        """
        Initialize an order category.

        :param cat_name: category name / CSS selector (unique).

        :param cat_group: label of the category's group.

        :param label: label of the category.

        :param css_def: CSS definition
        """
        self.cat_name = cat_name
        self.cat_group = cat_group
        self.label = label
        self.css_def = css_def

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.cat_name!r}, "
                    "{self.cat_group!r}, "
                    "{self.label!r}, "
                    "{self.css_def!r})")
        return repr_fmt.format(self=self)
