<%! import pkg_resources %>
<%inherit file="local:templates.master"/>

<%def name="title()"><%
version = pkg_resources.get_distribution('intranet').version
%>\
${_(u"Bienvenu sur l’intranet de pointage {version}".format(version=version))}</%def>

<h1>${_(u"Présentation")}</h1>

<p>${_(u"L’Intranet de pointage du temps est une application réseau de type client / \
serveur permettant d’enregistrer les temps passés sur les commandes/projets, \
par chacun des employés. L’objectif étant d’avoir une vue claire et synthétique \
du temps total passé sur les commandes et ainsi d’estimer les gains (et les \
pertes) et puis d’ajuster les tarifs pour les commandes à venir.")}</p>
