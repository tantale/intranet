# -*- coding: utf-8 -*-
# quickstarted Options:
#
# sqlalchemy: True
# auth:       None
# mako:       True
#
#

# This is just a work-around for a Python2.7 issue causing
# interpreter crash at exit when trying to log an info message.
try:
    import logging  # @UnusedImport
    import multiprocessing  # @UnusedImport
except:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs = ['WebTest >= 1.2.3',
            'nose == 1.1.2',
            'coverage',
            'wsgiref']

install_requires = ["Genshi == 0.7",
                    "Mako == 0.7.3",
                    "zope.sqlalchemy >= 0.4",
                    "repoze.tm2 >= 1.0a5",
                    "sqlalchemy",
                    "tw2.forms == 2.2.0.3",
                    "TurboGears2 == 2.2.2",

                    "alembic",
                    # 'MySQL-python',
                    ]

setup(
    name='Intranet',
    version='2.0.0',
    description='Intranet for time tracking and planning',
    author='Laurent LAPORTE',
    author_email='tantale.solutions@gmail.com',
    url='http://tantalesolutions.wordpress.com/',
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools'],
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'intranet': ['i18n/*/LC_MESSAGES/*.mo',
                               'templates/*/*/*/*/*',
                               'public/*/*/*/*/*']},
    message_extractors={'intranet': [('**.py', 'python', None),
                                     ('templates/**.mak', 'mako', None),
                                     ('public/**', 'ignore', None)]},

    entry_points = {'paste.app_factory': ['main = intranet.config.middleware:make_app'],
                    'paste.app_install': ['main = pylons.util:PylonsInstaller'],
                    'console_scripts': ['intranet_upgrade = intranet.maintenance.versions.v01_02.upgrade:main']},

    dependency_links=["http://tg.gy/222"],
    zip_safe=False
)
