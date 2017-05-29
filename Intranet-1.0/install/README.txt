Tantale Intranet - version 2.2.1
--------------------------------

Procédure d’installation et de migration de la base de donnée.

Copier la base de données de production à la place du fichier ``productiondata.db``.

Activer la virtualenv::

    Scripts\activate      # Sous Windows


Exécuter le programme de migration de la base de données::

    alembic -c work/alembic.ini upgrade head


Tester l’application::

    # Changer le port en 127.0.0.1 puis :
    paster serve work/production.ini

    # -> Le serveur doit démarrer.


Redémarer Apache

- Aller dans les services Windows en relancer Apache24
- Vérifier avec l’URL du service : http://chipheures-intranet/
