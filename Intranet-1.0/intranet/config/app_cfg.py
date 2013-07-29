# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in Intranet-1.0.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::

    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
"""

from tg.configuration import AppConfig

import intranet
from intranet import model
from intranet.lib import app_globals, helpers

base_config = AppConfig()
base_config.renderers = []
base_config.prefer_toscawidgets2 = True

base_config.package = intranet

# Enable json in expose
base_config.renderers.append('json')

# Enable genshi in expose to have a lingua franca for extensions
# and pluggable apps
# you can remove this if you don't plan to use it.
# base_config.renderers.append('genshi')

# Set the default renderer
base_config.default_renderer = 'mako'
base_config.renderers.append('mako')

# Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = True
base_config.model = intranet.model
base_config.DBSession = intranet.model.DBSession
