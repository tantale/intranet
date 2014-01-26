"""
:package: intranet.controllers.tools
:date: 2014-01-26
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.lib.base import BaseController

from intranet.controllers.tools.fix_bad_centuries import \
    FixBadCenturiesController


class ToolsController(BaseController):
    """
    Tools controller.
    """

    fix_bad_centuries = FixBadCenturiesController()
