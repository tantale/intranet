# -*- coding: utf-8 -*-
<%inherit file="local:templates.pointage.master"/>\
<%def name="title()">Gestion des employés</%def>\
<%def name="extra_css()"></%def>\
<%def name="extra_script()">\
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.employee.js')}"></script>\
<script>
	$(function() {
	%if curr_employee:
		display_employee_update_form(null);
	%else:
		display_employee_create_form(null);
	%endif
		$("#toolbar_employee").button('disable');
	});
</script>
</%def>\
<%def name="add_button()">\
<p class="alignCenter">
	<a class="addButton" href="#">Nouvel employé</a>
</p>\
</%def>\
<%def name="accordion()">\
<h2>Employés</h2>
<div>
%if employee_list:
	%for employee in employee_list:
		<%img_src = employee.photo_path if employee.photo_path else tg.url('/images/silhouette.min.png')%>\
		<p id="employee_${employee.uid}" class="selectButton">\
		<a href="?uid=${employee.uid}"><img class="imgLiquid" style="width: 38px; height: 42px;" id="employee_update__picture" alt="${employee.employee_name} - Photo" src="${img_src}" /></a> \
		<a href="?uid=${employee.uid}" class="searchable">${employee.employee_name}</a></p>
	%endfor
%else:
	<p>Aucun employé en base de données</p>
%endif
</div>\
</%def>\

%if curr_employee:
<%img_src = curr_employee.photo_path if curr_employee.photo_path else tg.url('/images/silhouette.png')%>\
<form id="employee_update" class="ui-widget" action="update" method="post" enctype="multipart/form-data">
	<fieldset>
		<legend class="ui-widget-header">Modifier les informations concernant ${curr_employee.employee_name}</legend>
		<table>
			<tr>
				<td valign="top">
					<div class="picture_box">
						<div class="picture_placeholder imgLiquid" style="width: 3.5cm; height: 4.5cm;">
							<img id="employee_update__picture" alt="Photo" src="${img_src}"/>
						</div>
					</div>
				</td>
				<td><p><label for="employee_update__name">Nom :</label>
						<input id="employee_update__name" type="text" name="employee_name"
							value="${curr_employee.employee_name}"
							placeholder="Nom / prénom"
							title="Nom de l’employé (requis)" /></p>
					<p><label for="employee_update__worked_hours">h/sem. travaillées :</label>
						<input id="employee_update__worked_hours" type="number" name="worked_hours"
							value="${curr_employee.worked_hours}"
							placeholder="39" size="2" min="1" max="39"
							title="Nombre d’heures travaillées par semaine (requis)" /></p>
					<p><label for="employee_update__entry_date">Date d’entrée :</label>
						<input id="employee_update__entry_date" type="date" name="entry_date"
							value="${curr_employee.entry_date}"
							title="Date d’entrée dans la société (requis)" /></p>
					<p><label for="employee_update__exit_date">Date de sortie :</label>
						<input id="employee_update__exit_date" type="date" name="exit_date"
							value="${curr_employee.exit_date}"
							title="Date de sortie de la société si hors effectif (optionnel)" /></p>
					<p><label for="employee_update__file">Photo :</label>
						<input id="employee_update__file" type="file" name="photo_path"
							value="${curr_employee.photo_path}"
							accept="image/*"
							title="Photo d’identité (optionnelle)" /></p></td>
			</tr>
			<tr>
				<td class="alignRight" colspan="2">
				<input id="employee_update__uid" type="hidden" name="uid"
							value="${curr_employee.uid}" />
				<a class="delButton" href="delete?uid=${curr_employee.uid}"
					title="Supprimer les informations concernant cet employé">Supprimer</a>
				<button id="employee_update__update" type="submit"
					title="Modifier les informations concernant cet employé">Modifier</button></td>
			</tr>
		</table>

	</fieldset>
</form>
%endif

<form id="employee_create" class="ui-widget" action="create" method="post" enctype="multipart/form-data">
	<fieldset>
		<legend class="ui-widget-header">Saisir les informations concernant un nouvel employé</legend>
		<table>
			<tr>
				<td valign="top">
					<div class="picture_box">
						<div class="picture_placeholder imgLiquid" style="width: 3.5cm; height: 4.5cm;">
							<img id="employee_create__picture" alt="Photo" src="${tg.url('/images/silhouette.png')}"/>
						</div>
					</div>
				</td>
				<td><p><label for="employee_create__name">Nom :</label>
						<input id="employee_create__name" type="text" name="employee_name"
							placeholder="Nom / prénom"
							title="Nom de l’employé (requis)" /></p>
					<p><label for="employee_create__worked_hours">h/sem. travaillées :</label>
						<input id="employee_create__worked_hours" type="number" name="worked_hours"
							placeholder="39" size="2" min="1" max="39"
							title="Nombre d’heures travaillées par semaine (requis)" /></p>
					<p><label for="employee_create__entry_date">Date d’entrée :</label>
						<input id="employee_create__entry_date" type="date" name="entry_date"
							title="Date d’entrée dans la société (requis)" /></p>
					<p><label for="employee_create__exit_date">Date de sortie :</label>
						<input id="employee_create__exit_date" type="date" name="exit_date"
							title="Date de sortie de la société si hors effectif (optionnel)" /></p>
					<p><label for="employee_create__file">Photo :</label>
						<input id="employee_create__file" type="file" name="photo_path"
							accept="image/*"
							title="Photo d’identité (optionnelle)" /></p></td>
			</tr>
			<tr>
				<td class="alignRight" colspan="2">
				<button id="employee_create__cancel" type="reset"
					title="Annuler">Annuler</button>
				<button id="employee_create__create" type="submit"
					title="Saisir les informations concernant un nouvel employé">Créer un employé</button></td>
			</tr>
		</table>

	</fieldset>
</form>
