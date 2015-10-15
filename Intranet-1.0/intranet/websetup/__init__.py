# -*- coding: utf-8 -*-
"""Setup the Intranet application"""
import logging

from intranet.config.environment import load_environment
from schema import setup_schema
import bootstrap

__all__ = ['setup_app']

log = logging.getLogger(__name__)


# noinspection PyShadowingBuiltins
def setup_app(command, conf, vars):  # @ReservedAssignment
    """Place any commands to setup intranet here"""
    load_environment(conf.global_conf, conf.local_conf)
    setup_schema(command, conf, vars)
    bootstrap.bootstrap(command, conf, vars)
