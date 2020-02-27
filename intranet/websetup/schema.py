# -*- coding: utf-8 -*-
"""Setup the Intranet application"""
from tg import config
import transaction
import os


def setup_schema(command, conf, vars):  # @ReservedAssignment
    """Place any commands to setup intranet here"""
    # Load the models

    # <websetup.websetup.schema.before.model.import>
    from intranet import model
    # <websetup.websetup.schema.after.model.import>

    # <websetup.websetup.schema.before.metadata.create_all>
    print "Creating tables"
    bind_engine = config['pylons.app_globals'].sa_engine
    model.metadata.create_all(bind=bind_engine)  # @UndefinedVariable
    # <websetup.websetup.schema.after.metadata.create_all>

    transaction.commit()
    from migrate.versioning.shell import main
    from migrate.exceptions import DatabaseAlreadyControlledError
    try:
        # -- change to current working directory to the parent of "migration/"
        work_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        os.chdir(work_dir)

        # -- run the 'migrate version_control' command:
        main(argv=['version_control'],
             url=config['sqlalchemy.url'],
             repository='migration',
             name='migration')
    except DatabaseAlreadyControlledError:
        print 'Database already under version control'
