"""Apache mod_wsgi script for project ${project_name}
Point to this script in your apache config file.
"""
import sys

# This block provides support for the default virtualenv
# deployment pattern.  The option `--virtualenv=` on the
# `paster modwsgi_deploy` command line will skip this section entirely.
prev_sys_path = list(sys.path)

import site
site.addsitedir('C:\\Program Files\\Tantale\\Intranet\\Lib\\site-packages')

# Set the environment variable PYTHON_EGG_CACHE to an appropriate directory
# where the Apache user has write permission and into which it can unpack egg files.
import os
os.environ['PYTHON_EGG_CACHE'] = "C:\\Apache24\\python-eggs"

# Initialize logging module from your TurboGears config file
from paste.script.util.logging_config import fileConfig
fileConfig('C:\\Program Files\\Tantale\\work\\production.ini')

# Finally, load your application's production.ini file.
from paste.deploy import loadapp
application = loadapp('config:C:\\Program Files\\Tantale\\\work\\production.ini')
