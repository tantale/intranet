<%inherit file="local:templates.master"/>
<%def name="title()">Intranet de pointage – Variables d’environnement</%def>

<p>
	Sur cette page, vous pouvez voir toutes les variables WSGI que votre objet
	<tt>request</tt>
	possède : celles en majuscules qui sont requises par la spécification, celles fournies par le composent
	<tt>Components</tt>
	(triées par composent), et enfin, celles avec l’espace de nom « <tt>wsgi.</tt> » qui sont des informations très utiles pour votre serveur WSGI.
</p>

<p>Les variables sont :</p>
<table class="table">
	%for key in sorted(environment):
	<tr>
		<td>${key}</td>
		<td>${environment[key]}</td>
	</tr>
	%endfor
</table>
