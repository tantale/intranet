<td>
    <input id="calendar_${uid}__label" type="text" name="label"
           value="${values.get('label')}"
           placeholder="Libellé"
           title="Le libellé du calendrier doit être unique"/>
    %if 'label' in form_errors:
    <span class="error">${form_errors['label']}</span>
    %endif
</td>
<td>
    <input id="calendar_${uid}__description" type="text" name="description"
           value="${values.get('description')}"
           placeholder="Description"
           title="Description du calendrier : dans quel contexte on l’utilise…"/>
    %if 'description' in form_errors:
    <span class="error">${form_errors['description']}</span>
    %endif
</td>
<td>
    <select id="calendar_${uid}__employee" name="employee_uid"
            title="Attribuer un calendrier à un employé">
        %if values.get('employee_uid'):
        <option value="" selected="selected">(aucun)</option>
        %else:
        <option value="">(aucun)</option>
        %endif
        %for employee in employee_list:
        %if values.get('employee_uid') == employee.uid:
        <option value="${employee.uid}" selected="selected">${employee.employee_name}</option>
        %else:
        <option value="${employee.uid}">${employee.employee_name}</option>
        %endif
        %endfor
    </select>
</td>
<td>
    <select id="calendar_${uid}__week_hours" name="week_hours_uid"
            title="Sélectionner les horaires de travail pour ce calendrier">
        %for week_hours in week_hours_list:
        %if values.get('week_hours_uid') == week_hours.uid:
        <option value="${week_hours.uid}" selected="selected">${week_hours.label}</option>
        %else:
        <option value="${week_hours.uid}">${week_hours.label}</option>
        %endif
        %endfor
    </select>
</td>
<td>
    <form id="calendar_${uid}__delete_form" class="delete_form inline_form"
          action="${tg.url('/admin/planning/calendar/{0}/delete'.format(uid))}"
          method="get">
        <p>
            <button id="calendar_${uid}__delete" type="submit" class="delete_button"
                    title="Supprimer le calendrier : ${values.get('label')}">${_(u"Supprimer")}
            </button>
        </p>
    </form>
</td>
<script type='text/javascript'><!--
    "use strict";
    /*global $*/
    $(function() {
        $('#calendar_${uid}__delete_form').button({
            text : false,
            icons : {
                primary : "ui-icon-trash"
            }
        });
    });
-->
</script>