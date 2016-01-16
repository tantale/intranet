============================
Tantale Intranet Application
============================

Installation in development mode (editable)
===========================================

First we create a new virtualenv with up-to-date versions of ``pip`` ``setuptools`` and ``wheel`` (which is used for application packaging).

Create the virtualenv for ``intranet-master``::

    cd ~/virtualenv
    rm -rf py-intranet-master/
    /usr/local/bin/virtualenv ~/virtualenv/py-intranet-master
    source ~/virtualenv/py-intranet-master/bin/activate
    pip install -U pip setuptools wheel

Install applications requirements for ``intranet-master``::

    cd ~/workspace/intranet-master/Intranet-1.0/
    rm -rf .eggs/
    pip install -e .

In development context, we need the TurboGears2 development tools, and extra libraries (to help releasing).

Install development requirements for ``intranet-master``::

    pip install tg.devtools==2.2.2  # TurboGears2 tools
    pip install docutils            # Documentation Utilities
    pip install gitchangelog        # Generates a changelog thanks to git log.


Installation and Setup
======================

Install ``Intranet`` using the setup.py script::

    $ cd Intranet
    $ pip install -r requirements.txt -f dist/

Create the project database for any model classes defined::

    $ paster setup-app development.ini

Start the paste http server::

    $ paster serve development.ini

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ paster serve --reload development.ini

Then you are ready to go.
