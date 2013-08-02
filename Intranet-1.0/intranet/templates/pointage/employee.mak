# -*- coding: utf-8 -*-
<%inherit file="local:templates.pointage.master"/>\
<%def name="title()">Gestion des employés</%def>\
<%def name="extra_css()"></%def>\
<%def name="extra_script()">\
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.employee.js')}"></script>\
<script>
	$(function() {
		$('.minimal_form').ajaxForm({
			target : '#employee_content'
		});
		$(".imgLiquid").imgLiquid({
			fill : true,
			horizontalAlign : "center",
			verticalAlign : "center"
		});
	});
</script>
</%def>\
<%def name="new_button()">\
<form id="employee_new" class="minimal_form alignCenter" action="new" method="get">
	<p>
		<button id="employee_new__new" type="submit" class="new_button"
			title="Ajouter un employé">Nouvel employé</button>
	</p>
</form>
</%def>\
<%def name="accordion()">\
<h2>Employés</h2>
<div>
%if employee_list:
	%for employee in employee_list:
		<%img_src = employee.photo_path if employee.photo_path else tg.url('/images/silhouette.min.png')%>\
		<form id="employee_select_${employee.uid}" class="minimal_form" action="select" method="get">
			<p>
				<input type="hidden" name="uid" value="${employee.uid}" />
				<button id="employee_select_${employee.uid}__select" type="submit" class="select_button searchable"
					title="Sélectionner ${employee.employee_name}">
					<img class="imgLiquid picture_box_inner_min valignMiddle"
						id="employee_select_${employee.uid}__picture"
						alt="${employee.employee_name} - Photo" src="${img_src}" />
					${employee.employee_name}</button>
			</p>
		</form>
	%endfor
%else:
	<p>Aucun employé en base de données</p>
%endif
</div>\
</%def>\
