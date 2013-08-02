# -*- coding: utf-8 -*-
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if flash:
	<div class="row"><div class="span8 offset2">
	${flash | n}
	</div></div>
%endif
%if curr_employee:
<form id="employee_update" class="ui-widget" action="update" method="post" enctype="multipart/form-data">
	<fieldset>
		<legend class="ui-widget-header">Modifier les informations concernant ${curr_employee.employee_name}</legend>
		<table>
			<tr>
				<td style="vertical-align: top;">
					<div class="picture_box">
						<div class="picture_box_inner imgLiquid">
							<img id="employee_update__picture" alt="Photo" src="${curr_employee.photo_path}"/>
						</div>
					</div>
				</td>
				<td><p><label for="employee_update__employee_name">Nom :</label>
						<input id="employee_update__employee_name" type="text" name="employee_name"
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
					<p><label for="employee_update__photo_path">Photo :</label>
						<input id="employee_update__photo_path" type="file" name="photo_path"
							value="${curr_employee.photo_path}"
							accept="image/*"
							title="Photo d’identité (optionnelle)" /></p></td>
			</tr>
			<tr>
				<td class="alignRight" colspan="2">
				<input type="hidden" name="uid" value="${curr_employee.uid}" />
				<button id="employee_update__update" type="submit" class="update_button"
					title="Modifier les informations concernant cet employé">Modifier</button></td>
			</tr>
		</table>
	</fieldset>
</form>

<form id="employee_delete" class="minimal_form" action="delete" method="post">
	<p>
		<input type="hidden" name="uid" value="${curr_employee.uid}" />
		<button id="employee_delete__delete" type="submit" class="delete_button"
			title="Supprimer les informations concernant ${curr_employee.employee_name}">Supprimer</button>
	</p>
</form>
%endif

<form id="employee_return" class="minimal_form" action="/pointage/employee/" method="post">
	<p>
		<button id="employee_return__return" type="submit" class="return_button"
			title="Retoune et met à jour la liste des employés">Retour</button>
	</p>
</form>

<script>
	if (!Modernizr.inputtypes.date) {
		$('#employee_content input[type=date]').datepicker();
	}
	$("#employee_content .imgLiquid").imgLiquid({
		fill : true,
		horizontalAlign : "center",
		verticalAlign : "center"
	});
	$("#employee_content .update_button").button({
		text : true,
		icons : {
			primary : "ui-icon-pencil"
		}
	});
	$("#employee_content .return_button").button({
		text : true,
		icons : {
			primary : "ui-icon-arrowreturnthick-1-w"
		}
	});
	$("#employee_content .delete_button").button({
		text : true,
		icons : {
			primary : "ui-icon-trash"
		}
	});
	$('#employee_update').ajaxForm({
		target : '#employee_content'
	});
	$('#employee_delete').ajaxForm({
		target : '#employee_content'
	});
</script>