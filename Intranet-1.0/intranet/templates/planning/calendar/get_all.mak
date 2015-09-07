%for calendar in calendar_list:
<tr id="calendar_${calendar.uid}">
    <td>
    <span id="calendar_${calendar.uid}_label" class="label editable"
          title="${_(u'Le libellé du calendrier doit être unique')}">${calendar.label}</span>
    </td>
    <td>
    <span id="calendar_${calendar.uid}_description" class="description editable"
          title="${_(u'Description du calendrier, contexte d’utilisation, etc.')}">${calendar.description}</span>
    </td>
    <td>
        <select id="calendar_${calendar.uid}_employee_uid" class="employee_uid editable"
                title="Attribuer un calendrier à un employé">
            %if calendar.employee_uid:
            <option value="" selected="selected">(aucun)</option>
            %else:
            <option value="">(aucun)</option>
            %endif
            %for employee in employee_list:
            %if calendar.employee_uid == employee.uid:
            <option value="${employee.uid}" selected="selected">${employee.employee_name}</option>
            %else:
            <option value="${employee.uid}">${employee.employee_name}</option>
            %endif
            %endfor
        </select>
    </td>
    <td>
        <select id="calendar_${calendar.uid}_week_hours_uid" class="week_hours_uid editable"
                title="Sélectionner les horaires de travail pour ce calendrier">
            %for week_hours in week_hours_list:
            %if calendar.week_hours_uid == week_hours.uid:
            <option value="${week_hours.uid}" selected="selected">${week_hours.label}</option>
            %else:
            <option value="${week_hours.uid}">${week_hours.label}</option>
            %endif
            %endfor
        </select>
    </td>
    <td>
        <form id="calendar_${calendar.uid}_delete_form" class="delete_form inline_form"
              action="${tg.url('/admin/planning/calendar/{0}/delete'.format(calendar.uid))}"
              method="get">
            <p>
                <button id="calendar_${calendar.uid}_delete" type="submit" class="delete_button"
                        title="Supprimer le calendrier : ${calendar.label}">${_(u"Supprimer")}
                </button>
            </p>
        </form>
    </td>
</tr>
%endfor
<script type='text/javascript'><!--
    "use strict";
    /*global $*/
    $(function() {
        $('#calendar .delete_form').ajaxForm({
            target: '#confirm_dialog_content'
        });
        $('#calendar .delete_button').button({
            text: false,
            icons: {
                primary: "ui-icon-trash"
            }
        });
    });
	// see: http://vitalets.github.io/x-editable/docs.html
    $('#calendar .label.editable').editable({
		type: "text",
		clear: true,
		pk: "unused",
		url: "${tg.url('/admin/planning/calendar/edit_in_place')}",
		title: "Saisir le libellé du calendrier",
		placeholder: "Libellé",
		emptytext: "(vide)",
		showbuttons: false,
		onblur: "cancel",
		success: function(response, newValue) {
			if (response.status === 'error') {
				return response.msg;
			}
		},
		inputclass: "input-medium code"
	});
    $('#calendar .description.editable').editable({
		type: "text",
		clear: true,
		pk: "unused",
		url: "${tg.url('/admin/planning/calendar/edit_in_place')}",
        title: "Saisir la description du calendrier",
		placeholder: "Description du calendrier",
		emptytext: "(vide)",
		showbuttons: false,
		onblur: "cancel",
		success: function(response, newValue) {
			if (response.status === 'error') {
				return response.msg;
			}
		},
		inputclass: "input-medium description"
	});
    $('#calendar select.editable').change(function() {
        jQuery.post("${tg.url('/admin/planning/calendar/edit_in_place')}",
            {name: this.id, value: this.value});
    });
-->


</script>
