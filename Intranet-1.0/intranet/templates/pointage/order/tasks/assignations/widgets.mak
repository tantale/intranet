##
## Task assignation widget
## =======================
##
<%def name="new_assignation_form(task, active_employees, **hidden)">
<%
task_id = "task_{0}".format(task.uid)
new_assignation_form_id = "new_assignation_form_{0}".format(task.uid)
unassigned_employees = list(task.get_unassigned_employees(active_employees))
unassigned_employees.sort(key=lambda e: e.employee_name)
%>
%if unassigned_employees:
<div class="badge ui-widget ui-state-default ui-corner-all">
    <form id="${new_assignation_form_id}" class="ui-widget"
          action="${tg.url('./{task.order_uid}/tasks/{task.uid}/assignations/new'.format(task=task))}"
          method="get">
        %for hidden_name, hidden_value in hidden.iteritems():
        <input type="hidden" name="${hidden_name}" value="${hidden_value}">
        %endfor
        <select name="employee_uid" class="add ui-widget ui-state-default ui-corner-all"
                title="Liste des employés">
            <option value="" selected="selected">+&nbsp;Ajouter</option>
            %for employee in task.get_unassigned_employees(active_employees):
            <option value="${employee.uid}">${employee.employee_name}</option>
            %endfor
        </select>
    </form>
</div>
<script type="application/javascript" defer="defer">
    $(function() {
        $('#${new_assignation_form_id} select').change(function(){
            $(this).closest('form').submit();
        });
    });
</script>
%endif
</%def>

<%def name="assignation_form(assignation, **hidden)">
<%
assignation_id = "assignation_{0}".format(assignation.uid)
assignation_form_id = "assignation_form_{0}".format(assignation.uid)
%>
<div class="badge ui-widget ui-state-default ui-corner-all">
    <form id="${assignation_form_id}" class="ui-widget"
          action="${tg.url('./{assignation.order_phase.order_uid}/tasks/{assignation.order_phase.uid}/assignations/{assignation.uid}/edit'.format(assignation=assignation))}"
          method="get">
        %for hidden_name, hidden_value in hidden.iteritems():
        <input type="hidden" name="${hidden_name}" value="${hidden_value}">
        %endfor
        <%img_src = assignation.employee.photo_path if assignation.employee.photo_path else tg.url('/images/silhouette.min.png')%>
        <table class="planning">
            <tbody>
            <tr>
                <td rowspan="2"><img class="valignMiddle picture_box_inner_min"
                                     alt="${assignation.employee.employee_name}"
                                     src="${img_src}"></td>
                <td><label class="tooltip"><b>Taux&nbsp;:</b>
                    <input name="rate_percent" value="${assignation.rate_percent}" type="number"
                           disabled="disabled"
                           min="5.0" max="100.0" step="5.0">&nbsp;%</label></td>
                <td>
                    <button type="submit" class="edit_button_icon" title="Modifier l‘affectation">!</button>
                </td>
            </tr>
            <tr>
                <td><label class="tooltip"><b>Date&nbsp;:</b>
                    <input name="start_planning_date" value="${assignation.start_planning_date}" type="date"
                    disabled="disabled"></label></td>
                <td>
                    <button type="button" class="calendar_button_icon" title="Planifier l‘affectation">#</button>
                </td>
            </tr>
            </tbody>
        </table>
    </form>
</div>
<script type="application/javascript" defer="defer">
    $(function() {
        $("#${assignation_form_id} .edit_button_icon").button({
            text : false,
            icons : {
                primary : "ui-icon-pencil"
            }
        });
        $("#${assignation_form_id} .calendar_button_icon").button({
            text : false,
            icons : {
                primary : "ui-icon-calendar"
            }
        });
    });
</script>
</%def>

<%def name="assignation_section(actions,
                                title,
                                question,
                                error_message,
                                employee,
                                task,
                                form_errors,
                                values,
                                **hidden)">
<script src="https://code.jquery.com/jquery-1.12.1.min.js"></script>
<script src="https://code.jquery.com/ui/1.10.4/jquery-ui.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.form/3.51/jquery.form.min.js"></script>
<link rel="stylesheet" href="https://code.jquery.com/ui/1.10.4/themes/le-frog/jquery-ui.css">
<section id="assignation_section" title="${title}">
    <style scoped="scoped" type="text/css">
        #assignation_section label b {
            display: inline-block;
            width: 8em;
        }
        span.help-content {
            font-size: .9em;
        }
        .ui-icon-help {
            display: inline-block;
        }
    </style>
    <form action="./" method="post" class="new_or_edit ui-widget">
        %if actions == "edit_or_delete":
        <input type="hidden" name="_method" value="PUT"/>
        %endif
        <input type="hidden" name="employee_uid" value="${employee.uid}">
        %for k, v in hidden.iteritems():
        <input type="hidden" name="${k}" value="${v}">
        %endfor

        <p>${question}</p>

        %if error_message:
        <p><span class="error">${error_message}</span></p>
        %endif

        <p><label class="tooltip"><b>Taux&nbsp;:</b>
            <input name="rate_percent" value="${values['rate_percent']}" type="number"
                   min="5.0" max="100.0" step="5.0">&nbsp;%</label>
            <span class="ui-icon ui-icon-help"></span></p>
        <p class="ui-tooltip" hidden="hidden"><span class="ui-tooltip-content">
        Taux d’afffectation de l’employé sur cette tâche.
        Un taux d’affectation bas permet d’étaler le travail sur une plus longue période
        en laissant l’employé disponible pour d’autres tâches.</span></p>
        %if 'rate_percent'in form_errors:
        <p><span class="error">${form_errors['rate_percent']}</span></p>
        %endif

        <p><label class="tooltip"><b>Date de début&nbsp;:</b>
            <input name="start_date" value="${values['start_date']}" type="date"></label>
            <span class="ui-icon ui-icon-help"></span></p>
        <p class="ui-tooltip" hidden="hidden"><span class="ui-tooltip-content">
        La date de début définie un point de départ à partir duquel la plannification peut débuter.</span></p>
        %if 'start_date'in form_errors:
        <p><span class="error">${form_errors['start_date']}</span></p>
        %endif

        <p><label class="tooltip"><b>Date de fin&nbsp;:</b>
            <input name="end_date" value="${values['end_date']}" type="date"></label>
            <span class="ui-icon ui-icon-help"></span></p>
        <p class="ui-tooltip" hidden="hidden"><span class="ui-tooltip-content">
        La date de fin définie une date limite à ne pas dépasser.
        Celle-ci est optionnelle.</span></p>
        %if 'end_date'in form_errors:
        <p><span class="error">${form_errors['end_date']}</span></p>
        %endif

        %if task.assignation_list:
        <details>
            <summary>Personnes déjà assignées</summary>
            <ol>
                %for assignation in task.assignation_list:
                <li>${assignation.get_assignation(tz_offset=hidden['tz_offset'])}</li>
                %endfor
            </ol>
        </details>
        %else:
        <p>Aucune assignation</p>
        %endif
    </form>
    <form action="./" method="post" class="delete ui-helper-hidden">
        <input type="hidden" name="_method" value="DELETE" />
    </form>
    <script type="application/javascript" defer="defer">
    $(function() {
        $("#assignation_section form.new_or_edit").ajaxForm({target: '#assignation_section'});;
        $("#assignation_section form.delete").ajaxForm({target: '#assignation_section'});;

        $("#assignation_section").dialog({
            width: 600,
            height: 400,
            modal: true,
            buttons: {
%if actions == "new":
                "Ajouter": function() {
                    $("#assignation_section form.new_or_edit").submit();
                },
%elif actions == "edit_or_delete":
                "Modifier": function() {
                    $("#assignation_section form.new_or_edit").submit();
                },
                "Supprimer": function() {
                    $("#assignation_section form.delete").submit();
                },
%endif
                "Annuler": function() {
                    $(this).dialog("close");
                }
            }
        });

        $("#assignation_section").tooltip({
            track: true,
            items: ".ui-icon-help",
            show: {
                delay: 500
            },
            content: function () {
                var element = $(this).parent();
                if (element.is("h3")) {
                    return element.next(".ui-tooltip").html();
                } else if (element.is("p")) {
                    return element.next(".ui-tooltip").html();
                } else {
                    return element.attr("title");
                }
            },
            tooltipClass: "info"
        });
    });
    </script>
</section>
</%def>
