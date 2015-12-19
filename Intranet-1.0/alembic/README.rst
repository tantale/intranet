Alembic
=======

Create a Migration Script
-------------------------

::

    $ alembic revision -m "create account table"


Running the migration
---------------------

::

    $ alembic upgrade head

Relative upgrades/downgrades are also supported. To move two versions from the current, a decimal value “+N” can be supplied:

::

    $ alembic upgrade +2

Negative values are accepted for downgrades:

::

    $ alembic downgrade -1

Downgrade back to nothing:

::

    $ alembic downgrade base


Getting Information
-------------------

The current revision:

::

    $ alembic current

The full information about each revision:

::

    $ alembic history --verbose
