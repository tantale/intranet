# -*- coding: utf-8 -*-
<div id="accordion">
<h2>Employés</h2>
<div>
%if employee_list:
	%for employee in employee_list:
		<%img_src = employee.photo_path if employee.photo_path else tg.url('/images/silhouette.min.png')%>\
		<form id="employee_edit_${employee.uid}" class="minimal_form"
			action="${tg.url('/pointage/employee/{employee.uid}/edit'.format(employee=employee))}" method="get">
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
	$('#accordion .minimal_form').ajaxForm({
		target : '#employee_content',
		beforeSubmit: function(arr, $form, options) {
			$('#flash').hide();
		}
	});
	$('#accordion form button').button();
	$('#accordion').accordion({
		heightStyle : "auto"
	});
</script>