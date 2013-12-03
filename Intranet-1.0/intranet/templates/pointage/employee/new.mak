# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.employee.new
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if flash:
	${flash | n}
%endif
<form id="employee_create" class="ui-widget"
	action="${tg.url('./')}"
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
							value="${values.get('employee_name')}"
							placeholder="Nom / prénom"
							title="Nom de l’employé (requis)" />
							%if 'employee_name' in form_errors:
							<span class="error">${form_errors['employee_name']}</span>
							%endif
							</p>
					<p><label for="employee_create__worked_hours">h/sem. travaillées :</label>
						<input id="employee_create__worked_hours" type="number" name="worked_hours"
							value="${values.get('worked_hours')}"
							placeholder="39" size="2" min="1" max="39"
							title="Nombre d’heures travaillées par semaine (requis)" />
							%if 'worked_hours' in form_errors:
							<span class="error">${form_errors['worked_hours']}</span>
							%endif
							</p>
					<p><label for="employee_create__entry_date">Date d’entrée :</label>
						<input id="employee_create__entry_date" type="date" name="entry_date"
							value="${values.get('entry_date')}"
							title="Date d’entrée dans la société (requis)" />
							%if 'entry_date' in form_errors:
							<span class="error">${form_errors['entry_date']}</span>
							%endif
							</p>
					<p><label for="employee_create__exit_date">Date de sortie :</label>
						<input id="employee_create__exit_date" type="date" name="exit_date"
							value="${values.get('exit_date')}"
							title="Date de sortie de la société si hors effectif (optionnel)" />
							%if 'exit_date' in form_errors:
							<span class="error">${form_errors['exit_date']}</span>
							%endif
							</p>
					<p><label for="employee_create__photo_path">Photo :</label>
						<input id="employee_create__photo_path" type="file" name="photo_path"
							value="${values.get('photo_path')}"
							accept="image/*"
							title="Photo d’identité (optionnelle)" />
							%if 'photo_path' in form_errors:
							<span class="error">${form_errors['photo_path']}</span>
							%endif
							</p></td>
			</tr>
			<tr>
				<td class="alignRight" colspan="2">
				<button id="employee_create__create" type="submit" class="create_button"
					title="Saisir les informations concernant un nouvel employé">Créer</button></td>
			</tr>
		</table>
	</fieldset>
</form>
<script type='text/javascript'>
	"use strict";
	/*global $, Modernizr*/
	if (!Modernizr.inputtypes.date) {
		$('#employee_content input[type=date]').datepicker();
	}
	$('#employee_content .imgLiquid').imgLiquid({
		fill : true,
		horizontalAlign : "center",
		verticalAlign : "center"
	});
	$('#employee_content .create_button').button({
		text : true,
		icons : {
			primary : "ui-icon-check"
		}
	});
	$('#employee_create').ajaxForm({
		target : '#employee_content',
		beforeSubmit: function(arr, form, options) {
			$('#flash').hide();
		},
		success: function(responseText, statusText, xhr) {
			console.log("search for '<div id=\"flash\"><div class=\"ok\">' tag...");
			var ok = $('<div/>').append(responseText).find('#flash div.ok');
			if (ok.length) {
				var input = $('#employee_get_all input[name=uid]');
				console.log("OK, update the employees list but don't select any employee...");
				input.val("");
				$('#employee_get_all').submit();
			} else {
				console.log("ERROR: don't update the employees list.");
			}
		}
	});
</script>
