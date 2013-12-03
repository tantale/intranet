# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.employee.edit
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%! import json %>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if flash:
	${flash | n}
%endif
<%img_src = values.get('photo_path') or tg.url('/images/silhouette.png')%>\
<form id="employee_update" class="ui-widget"
	action="${tg.url('./{uid}'.format(uid=values['uid']))}"
	method="post" enctype="multipart/form-data">
	<fieldset>
		<legend class="ui-widget-header">Modifier les informations concernant ${values.get('employee_name')}</legend>
		<table>
			<tr>
				<td style="vertical-align: top;">
					<div class="picture_box">
						<div class="picture_box_inner imgLiquid">
							<img id="employee_update__picture" alt="Photo" src="${img_src}"/>
						</div>
					</div>
				</td>
				<td><p><label for="employee_update__employee_name">Nom :</label>
						<input id="employee_update__employee_name" type="text" name="employee_name"
							value="${values.get('employee_name')}"
							placeholder="Nom / prénom"
							title="Nom de l’employé (requis)" />
							%if 'employee_name' in form_errors:
							<span class="error">${form_errors['employee_name']}</span>
							%endif
							</p>
					<p><label for="employee_update__worked_hours">h/sem. travaillées :</label>
						<input id="employee_update__worked_hours" type="number" name="worked_hours"
							value="${values.get('worked_hours')}"
							placeholder="39" min="1" max="39"
							title="Nombre d’heures travaillées par semaine (requis)" />
							%if 'worked_hours' in form_errors:
							<span class="error">${form_errors['worked_hours']}</span>
							%endif
							</p>
					<p><label for="employee_update__entry_date">Date d’entrée :</label>
						<input id="employee_update__entry_date" type="date" name="entry_date"
							value="${values.get('entry_date')}"
							title="Date d’entrée dans la société (requis)" />
							%if 'entry_date' in form_errors:
							<span class="error">${form_errors['entry_date']}</span>
							%endif
							</p>
					<p><label for="employee_update__exit_date">Date de sortie :</label>
						<input id="employee_update__exit_date" type="date" name="exit_date"
							value="${values.get('exit_date')}"
							title="Date de sortie de la société si hors effectif (optionnel)" />
							%if 'exit_date' in form_errors:
							<span class="error">${form_errors['exit_date']}</span>
							%endif
							</p>
					<p><label for="employee_update__photo_path">Photo :</label>
						<input id="employee_update__photo_path" type="file" name="photo_path"
							accept="image/*"
							title="Photo d’identité (optionnelle)" />
							%if 'photo_path' in form_errors:
							<span class="error">${form_errors['photo_path']}</span>
							%endif
							</p></td>
			</tr>
			<tr>
				<td class="alignRight" colspan="2">
				<input type="hidden" name="_method" value="PUT" />
				<button id="employee_update__update" type="submit" class="update_button"
					title="Modifier les informations concernant cet employé">Modifier</button>
				%if not values.get('exit_date'):
				<button id="employee_update__close" type="submit" class="close_button"
					title="Indiquer comme hors effectif à la date du jour">Hors effectif</button>
				%endif
				</td>
			</tr>
		</table>
	</fieldset>
</form>

<form id="employee_get_delete" class="minimal_form"
	action="${tg.url('./{uid}/delete'.format(uid=values['uid']))}"
	method="get">
	<p>
		<button id="employee_get_delete__delete" type="submit" class="delete_button"
			title="Supprimer les informations concernant ${values.get('employee_name')}">Supprimer</button>
	</p>
</form>

<script type='text/javascript'>
"use strict";
/*global $*/
$('#employee_content .imgLiquid').imgLiquid({
	fill : true,
	horizontalAlign : "center",
	verticalAlign : "center"
});
$('#employee_content .update_button').button({
	text : true,
	icons : {
		primary : "ui-icon-pencil"
	}
});
%if not values.get('exit_date'):
$('#employee_content .close_button').button({
	text : true,
	icons : {
		primary : "ui-icon-circle-close"
	}
}).click(function() {
	var date = new Date();
	$('#employee_update__exit_date').val(date.toISOString().split("T")[0]);
});
%endif
$('#employee_update').ajaxForm({
	target : '#employee_content',
	beforeSubmit : function(arr, form, options) {
		$('#flash').hide();
	},
	success : function(responseText, statusText, xhr) {
		var ok = $('<div/>').append(responseText).find('#flash div.ok');
		if (ok.length) {
			var input = $('#employee_get_all input[name=uid]'), //
				uid = input.val();
			input.val("");
			$('#employee_get_all').submit();
			input.val(uid);
		}
	}
});
$('#employee_get_delete .delete_button').button({
	text : true,
	icons : {
		primary : "ui-icon-trash"
	}
});
$('#employee_get_delete').ajaxForm({
	target : '#confirm_dialog_content'
});
</script>
