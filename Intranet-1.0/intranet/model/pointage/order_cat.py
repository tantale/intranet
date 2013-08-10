"""
:module: intranet.model.pointage.order_cat
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.model import DeclarativeBase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text


class OrderCat(DeclarativeBase):
    """
    Order category
    """
    __tablename__ = 'OrderCat'

    uid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    cat_name = Column(Text, unique=True, nullable=False, index=True)
    cat_group = Column(Text, nullable=False, index=True)
    label = Column(Text, nullable=False)
    css_def = Column(Text, nullable=False)

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
