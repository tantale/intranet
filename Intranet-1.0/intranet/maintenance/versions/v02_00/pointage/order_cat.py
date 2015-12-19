"""
:module: intranet.model.pointage.order_cat
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import re
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from intranet.maintenance.versions.v02_00.model import DeclarativeBase


def format_css_def(css):
    entry_list = ("{key}: {value}".format(key=key, value=value) for key, value in css.iteritems())
    css_def = "; ".join(entry_list)
    return css_def


def format_code(code):
    return "color{code}".format(code=code)


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

    def __init__(self, cat_name, cat_group, label, css_def, code=None, css=None):
        """
        Initialize an order category.

        :param cat_name: category name / CSS selector (unique).

        :param cat_group: label of the category's group.

        :param label: label of the category.

        :param css_def: CSS definition
        """
        self.cat_name = cat_name or format_code(code)
        self.cat_group = cat_group
        self.label = label
        self.css_def = css_def or format_css_def(css)

    def __repr__(self):
        repr_fmt = ("{self.__class__.__name__}("
                    "{self.cat_name!r}, "
                    "{self.cat_group!r}, "
                    "{self.label!r}, "
                    "{self.css_def!r})")
        return repr_fmt.format(self=self)

    @property
    def code(self):
        return self.cat_name[5:]  # drop "color" prefix

    @code.setter
    def code(self, code):
        self.cat_name = format_code(code)

    @property
    def css(self):
        entry_list = filter(None, re.split(r";\s*", self.css_def))
        try:
            css = dict(re.split(r":\s+", entry) for entry in entry_list)
        except ValueError:
            css = dict()
        css.setdefault("color", "#000000")
        css.setdefault("background-color", "#ffffff")
        return css

    @css.setter
    def css(self, css):
        self.css_def = format_css_def(css)
