# -*- coding: utf-8 -*-
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if flash:
	<div class="row"><div class="span8 offset2">
	${flash | n}
	</div></div>
%endif
%if new_employee:
<form id="employee_create" class="ui-widget"
	action="${tg.url('/pointage/employee/')}"
	method="post" enctype="multipart/form-data">
	<fieldset>
		<legend class="ui-widget-header">Saisir les informations concernant un nouvel employé</legend>
		<table>
			<tr>
				<td class="valignTop">
					<div class="picture_box">
						<div class="picture_box_inner imgLiquid">
							<img id="employee_create__picture" alt="Photo" src="${tg.url('/images/silhouette.png')}"/>
						</div>
					</div>
				</td>
				<td><p><label for="employee_create__employee_name">Nom :</label>
						<input id="employee_create__employee_name" type="text" name="employee_name"
							value="${new_employee.employee_name}"
							placeholder="Nom / prénom"
							title="Nom de l’employé (requis)" /></p>
					<p><label for="employee_create__worked_hours">h/sem. travaillées :</label>
						<input id="employee_create__worked_hours" type="number" name="worked_hours"
							value="${new_employee.worked_hours}"
							placeholder="39" size="2" min="1" max="39"
							title="Nombre d’heures travaillées par semaine (requis)" /></p>
					<p><label for="employee_create__entry_date">Date d’entrée :</label>
						<input id="employee_create__entry_date" type="date" name="entry_date"
							value="${new_employee.entry_date}"
							title="Date d’entrée dans la société (requis)" /></p>
					<p><label for="employee_create__exit_date">Date de sortie :</label>
						<input id="employee_create__exit_date" type="date" name="exit_date"
							value="${new_employee.exit_date}"
							title="Date de sortie de la société si hors effectif (optionnel)" /></p>
					<p><label for="employee_create__photo_path">Photo :</label>
						<input id="employee_create__photo_path" type="file" name="photo_path"
							value="${new_employee.photo_path}"
							accept="image/*"
							title="Photo d’identité (optionnelle)" /></p></td>
			</tr>
			<tr>
				<td class="alignRight" colspan="2">
				<button id="employee_create__create" type="submit" class="create_button"
					title="Saisir les informations concernant un nouvel employé">Créer</button></td>
			</tr>
		</table>
	</fieldset>
</form>

%endif

<script type='text/javascript'>
	if (!Modernizr.inputtypes.date) {
		$('#employee_content input[type=date]').datepicker();
	}
	$("#employee_content .imgLiquid").imgLiquid({
		fill : true,
		horizontalAlign : "center",
		verticalAlign : "center"
	});
	$("#employee_content .create_button").button({
		text : true,
		icons : {
			primary : "ui-icon-check"
		}
	});
	$('#employee_create').ajaxForm({
		target : '#employee_content',
		success: refresh_accordion
	});
</script>
