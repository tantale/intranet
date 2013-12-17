# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in Intranet.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::

    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
"""
from intranet import model  # @UnusedImport
from intranet.lib import app_globals, helpers  # @UnusedImport
from paste.cascade import Cascade  # @UnresolvedImport
from paste.urlparser import StaticURLParser  # @UnresolvedImport
from pylons.configuration import config
from tg.configuration import AppConfig
import intranet


class IntranetAppConfig(AppConfig):
    def add_static_file_middleware(self, app):
        # -- The upload file storage deliver files statically too.
        # To do that, we add a 'file_storage_app' in the application's chain.
        # @note: 'file_storage_dir' is defined in the '*.ini' files.
        # @see: 'development.ini' or 'production.ini'.
        static_app = StaticURLParser(config['pylons.paths']['static_files'])
        file_storage_app = StaticURLParser(config['file_storage_dir'])
        app = Cascade([static_app, file_storage_app, app])
        return app


base_config = IntranetAppConfig()

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
base_config.model = intranet.model  # @UndefinedVariable
base_config.DBSession = intranet.model.DBSession  # @UndefinedVariable
