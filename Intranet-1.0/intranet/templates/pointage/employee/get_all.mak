# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.employee.get_all
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%! import json %>
<div id="accordion">
<h2>Employés</h2>
<div>
%if employee_list:
	%for employee in employee_list:
		<%img_src = employee.photo_path if employee.photo_path else tg.url('/images/silhouette.min.png')%>\
		<form id="employee_edit_${employee.uid}" class="minimal_form"
			action="${tg.url('./{employee.uid}/edit'.format(employee=employee))}" method="get">
			<p><button id="employee_edit_${employee.uid}__edit" type="submit"
				class="edit_button searchable"
				title="Sélectionner ${employee.employee_name}"><img
					class="valignMiddle picture_box_inner_min"
					id="employee_edit_${employee.uid}__picture"
					alt="${employee.employee_name} - Photo"
					src="${img_src}" />${employee.employee_name}</button></p>
		</form>
	%endfor
%else:
    <p>Aucun employé</p>
%endif
</div>
</div>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$('#accordion .minimal_form').ajaxForm({
		target: '#employee_content',
		beforeSubmit: function(arr, $form, options) {
			$('#flash').hide();
		}
	});
	$('#accordion form button').button();
	$('#accordion').accordion({
		collapsible: false,
		heightStyle: "content",
		beforeActivate: function(event, ui) {
			if (ui.oldHeader.attr('id')) {
				console.log("empty #employee_content...");
				$('#employee_content').empty();
			}
		}
	});
</script>