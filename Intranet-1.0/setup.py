# -*- coding: utf-8 -*-
# quicks tarted Options:
#
# sqlalchemy: True
# auth:       None
# mako:       True
#
#

# # This is just a work-around for a Python2.7 issue causing
# # interpreter crash at exit when trying to log an info message.
# try:
#     import logging  # @UnusedImport
#     import multiprocessing  # @UnusedImport
# except:
#     pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup, find_packages

tests_require = [
    'WebTest == 1.4.3',
    'nose',
    'coverage',
    'wsgiref']

install_requires = [
    # This two packages must have version fixed, and must be installed in this order:
    'WebOb == 1.1.1',
    'WebTest == 1.4.3',

    # 'WebOb==1.1.1',
    # 'Pylons==1.0',
    'WebFlash==0.1a9',  # forced to use an alpha release
    # 'WebError==0.10.3',
    # 'Babel==0.9.6',
    # 'crank==0.6.4',
    "TurboGears2 == 2.2.2",
    "tg.devtools == 2.2.2",

    "Genshi == 0.7",
    "Mako == 0.7.3",
    "zope.sqlalchemy >= 0.4",
    "repoze.tm2 >= 1.0a5",
    "SQLAlchemy >= 1.0.11, < 1.1",
    "tw2.forms == 2.2.0.3",
    "alembic >= 0.8.4, < 0.9",
]

setup(name='Intranet',
      version='2.2.0',
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
      tests_require=tests_require,
      package_data={'intranet': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*/*/*/*',
                                 'public/*/*/*/*/*']},
      data_files=[('', ['install/intranet.conf',
                        'install/README.txt',
                        'install/release_notes_en.txt',
                        'install/release_notes_fr.txt',
                        'install/intranet.wsgi']),
                  ('work', ['install/work/alembic.ini',
                            'install/work/production.ini',
                            'install/work/productiondata.db'])],
      message_extractors={'intranet': [('**.py', 'python', None),
                                       ('templates/**.mak', 'mako', None),
                                       ('public/**', 'ignore', None)]},

      entry_points={'paste.app_factory': ['main = intranet.config.middleware:make_app'],
                    'paste.app_install': ['main = pylons.util:PylonsInstaller'],
                    'console_scripts': ['intranet_upgrade = intranet.maintenance.versions.v01_02.upgrade:main']},

      dependency_links=["http://tg.gy/222"],
      zip_safe=False)
