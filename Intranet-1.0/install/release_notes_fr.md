﻿Journal des versions
====================

Version 2.2.1 (2016-12-19)
--------------------------

Bugs corrigés
^^^^^^^^^^^^^

- [Issue #37](https://github.com/tantale/intranet/issues/37) [eventResize] Interdire le redimensionnement d’une tâche
  sur plusieurs jours. [Laurent LAPORTE]
- [Issue #28](https://github.com/tantale/intranet/issues/28) [OrderPhase] Ne pas afficher la liste des phases
  si au moins une tâche est planifiée. [Laurent LAPORTE]
- [Issue #38](https://github.com/tantale/intranet/issues/38) [Order] Mettre à jour la commande après estimation des
  tâches. [Laurent LAPORTE]
- [Issue #42](https://github.com/tantale/intranet/issues/42) [Employee] Ajouter formulaire de modification du
  calendrier. [Laurent LAPORTE]
- [Issue #39](https://github.com/tantale/intranet/issues/39) [Employee] Impossible d’ajouter une photo. [Laurent
  LAPORTE]
- [Issue #41](https://github.com/tantale/intranet/issues/41) La planification ne tient pas compte des événements
  utilisateur. [Laurent LAPORTE]
- [Issue #48](https://github.com/tantale/intranet/issues/40) Assigner heures ne correspond pas au temps restant.
  [Laurent LAPORTE]

Version 2.2.0 (2016-11-30)
--------------------------

Nouveautés
^^^^^^^^^^

- Nouvelle rubrique « Planning » : cette rubrique présente les calendriers des employés.
- Planning des événements : ensemble de calendriers associés aux utilisateurs.
- Paramétrage des calendriers.


Version 1.4.0 (2015-06-25)
--------------------------

Nouveautés
^^^^^^^^^^

- Nouvelle rubrique « Statistiques des pointages » : bilan des pointages effectués sur les commandes. Total par phase et par commande.


Améliorations
^^^^^^^^^^^^^

- Mémorisation de la position du volet de gauche,
- Pointage : mémorisation de l‘utilisateur en cours de sélection,
- Calendrier : mémorisation de la vue (mois, semaine, jour) et de la date en cours,
- Mise à jour des bibliothèques JavaScript tierces « fullcalendar » et « jquery-layout ».


Modifications
^^^^^^^^^^^^^

- Remplacement de l’icône « Calendrier » par l’icône « Horloge » pour la rubrique « Gestion des pointages ». L‘icône « Calendrier » sera dédié à la planification.


Bugs corrigés
^^^^^^^^^^^^^

- Correction d’une anomalie provoquée par le déplacement du volet de gauche au-dessus du calendrier ;
- Correction du menu d‘accès rapide : les menus « Administration » et « Pointage » s’affiche correctement (de manière dynamique).


Version 1.3.0 (2015-03-03)
--------------------------


Nouveautés
^^^^^^^^^^

- Nouvelle rubrique « Préférences » utilisée pour la configuration de l’application.
- Ajout de la possibilié de paramétrer les catégories de commandes (libellé, couleurs, ordre de tri, regroupement).


Améliorations

- Ajout de pages d’aide à l’utilisation des différentes rubriques : gestion des employés et des commandes, rubrique « Préférences ».


Bugs corrigés
^^^^^^^^^^^^^

- La vue « Modifier une commande » affiche un nom de catégorie par défaut lorsque la commande a perdu sa catégorie (suite à sa suppression).