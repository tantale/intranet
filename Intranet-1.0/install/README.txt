Tantale Intranet - version 2.1.0
--------------------------------

Procédure d’installation et me migration de la base de donnée.

Copier la base de données de production à la place du fichier ``productiondata.db``.

Activer la virtualenv::

    Script/activate      # Sous Windows


Exécuter le programme de migration de la base de données::

    alembic -c work/alembic.ini upgrade head


Tester l’application::

    paster serve work/production.ini


Le serveur doit démarrer.
