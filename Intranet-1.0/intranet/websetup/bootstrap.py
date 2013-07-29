# -*- coding: utf-8 -*-
"""Setup the Intranet-1.0 application"""
from intranet import model
from tg import config
import logging
import transaction


def bootstrap(command, conf, vars):  # @ReservedAssignment
    """Place any commands to setup intranet here"""

    # <websetup.bootstrap.before.auth

    # <websetup.bootstrap.after.auth>
