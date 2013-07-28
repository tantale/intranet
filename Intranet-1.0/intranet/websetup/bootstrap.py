# -*- coding: utf-8 -*-
"""Setup the Intranet-1.0 application"""

import logging
from tg import config
from intranet import model
import transaction

def bootstrap(command, conf, vars):
    """Place any commands to setup intranet here"""

    # <websetup.bootstrap.before.auth

    # <websetup.bootstrap.after.auth>
