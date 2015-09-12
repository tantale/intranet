<%namespace file="intranet.templates.planning.calendar.ctrl_select_class_name" import="select_class_name"/>
%for calendar in calendar_list:
<article id="calendar_${calendar.uid}">

    <h2><span id="calendar_${calendar.uid}_label" class="label editable"
              title="${_(u'Le libellé du calendrier doit être unique')}">${calendar.label}</span></h2>

    <p><span id="calendar_${calendar.uid}_description" class="description editable"
             title="${_(u'Description du calendrier, contexte d’utilisation, etc.')}">${calendar.description}</span></p>

    <p><label for="calendar_${calendar.uid}_employee_uid">Calendrier de&nbsp: </label>
        <select id="calendar_${calendar.uid}_employee_uid"
                class="employee_uid editable ui-widget ui-state-default ui-corner-all"
                title="Attribuer un calendrier à un employé">
            %if calendar.employee_uid:
            <option value="" selected="selected">(personne)</option>
            %else:
            <option value="">(personne)</option>
            %endif
            %for employee in employee_list:
            %if calendar.employee_uid == employee.uid:
            <option value="${employee.uid}" selected="selected">${employee.employee_name}</option>
            %else:
            <option value="${employee.uid}">${employee.employee_name}</option>
            %endif
            %endfor
        </select>
    </p>

    <p><label for="calendar_${calendar.uid}_week_hours_uid">Horaires applicables&nbsp;: </label>
        <select id="calendar_${calendar.uid}_week_hours_uid"
                class="week_hours_uid editable ui-widget ui-state-default ui-corner-all"
                title="Sélectionner les horaires de travail pour ce calendrier">
            %for week_hours in week_hours_list:
            %if calendar.week_hours_uid == week_hours.uid:
            <option value="${week_hours.uid}" selected="selected">${week_hours.label}</option>
            %else:
            <option value="${week_hours.uid}">${week_hours.label}</option>
            %endif
            %endfor
        </select>
    </p>

    <details>
        <summary>Couleurs et style</summary>
        <table border="0">
            <tbody>
            <tr>
                <td><label for="calendar_${calendar.uid}_background_color">fond&nbsp;: </label></td>
                <td><input id="calendar_${calendar.uid}_background_color" class="background_color editable" type="color"
                           name="background_color" title="${_(u'Couleur du fond')}"
                           value="${calendar.background_color}"/>
                </td>
            </tr>
            <tr>
                <td><label for="calendar_${calendar.uid}_border_color">bordures&nbsp;: </label></td>
                <td><input id="calendar_${calendar.uid}_border_color" class="border_color editable" type="color"
                           name="border_color" title="${_(u'Couleur des bordures')}" value="${calendar.border_color}"/>
                </td>
            </tr>
            <tr>
                <td><label for="calendar_${calendar.uid}_text_color">texte&nbsp;: </label></td>
                <td><input id="calendar_${calendar.uid}_text_color" class="text_color editable" type="color"
                           name="text_color" title="${_(u'Couleur du texte')}" value="${calendar.text_color}"/></td>
            </tr>
            <tr>
                <td><label for="calendar_${calendar.uid}_groups">catégorie&nbsp;: </label></td>
                <td>${select_class_name("calendar_${calendar.uid}_groups",
                    "class_name", _(u"Sélectionnez une catégorie"),
                    order_cat_groups, selected_cat_name=calendar.class_name, empty_label=_(u"(Aucune)"))}
                </td>
            </tr>
            </tbody>
        </table>
    </details>

    <nav>
        <form id="calendar_${calendar.uid}_delete_form" class="delete_form inline_form"
              action="${tg.url('/admin/planning/calendar/{0}/delete'.format(calendar.uid))}"
              method="get">
            <p>
                <button id="calendar_${calendar.uid}_delete" type="submit" class="delete_button"
                        title="Supprimer le calendrier : ${calendar.label}">${_(u"Supprimer")}
                </button>
            </p>
        </form>
    </nav>

</article>
%endfor

<script type='text/javascript'><!--
    "use strict";
    /*global $*/
    $(function() {
        $('#calendar .delete_form').ajaxForm({
            target: '#confirm_dialog_content'
        });
        $('#calendar .delete_button').button({
            text: true,
            icons: {
                primary: "ui-icon-trash"
            }
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
            inputclass: "input-large label"
        });
        $('#calendar .description.editable').editable({
            type: "textarea",
            rows: 2,
            clear: true,
            pk: "unused",
            url: "${tg.url('/admin/planning/calendar/edit_in_place')}",
            title: "Saisir la description du calendrier",
            placeholder: "Description du calendrier",
            emptytext: "(vide)",
            showbuttons: true,
            onblur: "cancel",
            success: function(response, newValue) {
                if (response.status === 'error') {
                    return response.msg;
                }
            },
            inputclass: "input-large description"
        });
        $('#calendar select.editable').change(function() {
            jQuery.post("${tg.url('/admin/planning/calendar/edit_in_place')}",
                {name: this.id, value: this.value});
        });
        $('#calendar input[type=color].editable').change(function() {
            jQuery.post("${tg.url('/admin/planning/calendar/edit_in_place')}",
                {name: this.id, value: this.value});
        });
    });
-->

</script>
