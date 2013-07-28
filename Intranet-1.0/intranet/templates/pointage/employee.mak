# -*- coding: utf-8 -*-
<%inherit file="local:templates.pointage.master"/>\
<%def name="title()">Gestion des employés</%def>\
<%def name="extra_css()"></%def>\
<%def name="extra_script()">\
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.employee.js')}"></script>\
</%def>\
<%def name="add_button()">\
<p class="alignCenter">
	<a id="employee_add" class="addButton" href="#">Nouvel employé</a>
</p>\
</%def>\
<%def name="accordion()">\
<h2>Employés</h2>
<div>
	<p class="selectEmpButton"><a href="#"><img alt="Photo" src="upload/thierry.min.png"></a> <a href="#" class="searchable">Thierry</a></p>
	<p class="selectEmpButton"><a href="#"><img alt="Photo" src="upload/elise.min.png"></a> <a href="#" class="searchable">Élise</a>	</p>
	<p class="selectEmpButton"><a href="#"><img alt="Photo" src="upload/nicolas.min.png"></a> <a href="#" class="searchable">Nicolas</a></p>
	<p class="selectEmpButton"><a href="#"><img alt="Photo" src="public/images/silhouette.min.png"></a> <a href="#" class="searchable">Jacques</a></p>
</div>\
</%def>\

<form id="employee_update" class="ui-widget" action="employee/update" method="post" enctype="multipart/form-data">
	<fieldset>
		<legend class="ui-widget-header">Modifier les informations concernant un employé</legend>
		<table>
			<tr>
				<td valign="top">
					<div class="picture_box">
						<div class="picture_placeholder imgLiquid" style="width: 3.5cm; height: 4.5cm;">
							<img id="employee_update__picture" alt="Photo" src="upload/thierry.png"/>
						</div>
					</div>
				</td>
				<td><p>
						<label for="employee_update__name">Nom :</label> <input id="employee_update__name" type="text" name="name"
							placeholder="Nom / prénom" value="Therry"
							title="Nom de l’employé (requis)" />
					</p>
					<p>
						<label for="employee_update__taux">Taux horaire :</label> <input id="employee_update__taux" type="number"
							name="taux" placeholder="39" size="2" min="1" max="39"
							title="Nombre d’heures par semaine (requis)" />h/sem.
					</p>
					<p>
						<label for="employee_update__entry_date">Date d’entrée :</label> <input id="employee_update__entry_date"
							type="date" name="entry_date"
							title="Date d’entrée dans la société (requis)" />
					</p>
					<p>
						<label for="employee_update__exit_date">Date de sortie :</label> <input id="employee_update__exit_date"
							type="date" name="exit_date"
							title="Date de sortie de la société si hors effectif (optionnel)" />
					</p>
					<p>
						<label for="employee_update__file">Photo :</label> <input id="employee_update__file" type="file" name="file"
							accept="image/*"
							title="Photo d’identité (optionnelle)" />
					</p></td>
			</tr>
			<tr>
				<td class="alignRight" colspan="2"><button id="employee_update__update" type="submit"
				title="Modifier les informations concernant un employé">Modifier</button></td>
			</tr>
		</table>

	</fieldset>
</form>
