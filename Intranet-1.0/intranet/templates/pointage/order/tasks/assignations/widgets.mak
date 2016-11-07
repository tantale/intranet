<%! import json %>
<%! import datetime %>

##
## All assignations of a given task
## ================================
##
<%def name="assignations(task, active_employees, **hidden)">
%for assignation in task.assignation_list:
${assignation_form(assignation, **hidden)}
%endfor
${new_assignation_form(task, active_employees, **hidden)}
</%def>

##
## New Assignation form : "badge" button used to add a new assignation
## ===================================================================
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
        $('#${new_assignation_form_id}').ajaxForm({target: '#confirm_dialog_content'});
        $('#${new_assignation_form_id} select').change(function(){
            if ($(this).val()) {
                $(this).closest('form').submit();
            }
        });
    });
</script>
%endif
</%def>

##
## Assignation form : "badge" form use to edit an assignation or plan it
## =====================================================================
##
<%def name="assignation_form(assignation, **hidden)">
<%
assignation_id = "assignation_{0}".format(assignation.uid)
assignation_badge_id = "assignation_form_{0}".format(assignation.uid)
tz_offset = hidden['tz_offset']
tz_delta = datetime.timedelta(minutes=int(tz_offset))
if assignation.start_planning_date:
    start_planning_date = (assignation.start_planning_date - tz_delta).isoformat()
else:
    start_planning_date = ""
if assignation.end_planning_date:
    end_planning_date = (assignation.end_planning_date - tz_delta).isoformat()
else:
    end_planning_date = ""
%>
<div id="${assignation_badge_id}" class="badge ui-widget ui-state-default ui-corner-all">
    <%img_src = assignation.employee.photo_path if assignation.employee.photo_path else tg.url('/images/silhouette.min.png')%>
    <table class="planning">
        <tbody>
        <tr>
            <td rowspan="2"><img class="valignMiddle picture_box_inner_min"
                                 alt="${assignation.employee.employee_name}"
                                 title="${assignation.employee.employee_name}"
                                 src="${img_src}"></td>
            <td><label class="tooltip"><b>du&nbsp;:</b>
                <input name="start_planning_date"
                       value="${start_planning_date}"
                       type="datetime-local"
                disabled="disabled"></label></td>
            <td>
                <button type="submit" class="edit_button_icon" title="Modifier l‘affectation">!</button>
            </td>
        </tr>
        <tr>
            <td><label class="tooltip"><b>au&nbsp;:</b>
                <input name="end_planning_date"
                       value="${end_planning_date}"
                       type="datetime-local"
                disabled="disabled"></label></td>
            <td>
                <button type="button" class="calendar_button_icon" title="Planifier l‘affectation">#</button>
            </td>
        </tr>
        </tbody>
    </table>
</div>
<script type="application/javascript" defer="defer">
    $(function() {
        $("#${assignation_badge_id} .edit_button_icon").button({
            text : false,
            icons : {
                primary : "ui-icon-pencil"
            }
        }).click(function() {
            var data = ${json.dumps(hidden)|n};
            var url = "${tg.url('./{assignation.order_phase.order_uid}/tasks/{assignation.order_phase.uid}/assignations/{assignation.uid}/edit'.format(assignation=assignation))|n}";
            url += "?" + jQuery.param(data);
            console.log({url: url});
            $('#confirm_dialog_content').load(url);  // GET method
        });
        $("#${assignation_badge_id} .calendar_button_icon").button({
            text : false,
            icons : {
                primary : "ui-icon-calendar"
            }
        }).click(function() {
            var data = ${json.dumps(hidden)|n};
            var url = "${tg.url('./{assignation.order_phase.order_uid}/tasks/{assignation.order_phase.uid}/assignations/{assignation.uid}/plan_one'.format(assignation=assignation))|n}";
            url += "?" + jQuery.param(data);
            console.log({url: url});
            $('#confirm_dialog_content').load(url);  // GET method
        });
    });
</script>
</%def>

##
## new/edit/delete Assignation form(s) : dialog boxes
## ==================================================
##
<%def name="assignation_dialog(actions,
                               title,
                               question,
                               error_message,
                               employee,
                               task,
                               assignation,
                               form_errors,
                               values,
                               **hidden)">
<%
assignations_id = "assignations_{0}".format(task.uid)
if assignation:
    action_url = tg.url('./{task.order_uid}/tasks/{task.uid}/assignations/{assignation.uid}/'.format(task=task, assignation=assignation))
else:
    action_url = tg.url('./{task.order_uid}/tasks/{task.uid}/assignations/'.format(task=task))
assignation_list = [assigned for assigned in task.assignation_list
                    if not assignation or assignation.uid != assigned.uid]
%>
<section id="assignation_dialog" title="${title}">
    <style scoped="scoped" type="text/css">
        #assignation_dialog label b {
            display: inline-block;
            width: 8em;
        }
        #assignation_dialog form p {
            margin-bottom: .5em;
        }
        span.help-content {
            font-size: .9em;
        }
        .ui-icon-help {
            display: inline-block;
        }
    </style>
    <form action="${action_url}" method="post" class="new_or_edit ui-widget">
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

        <p><label class="tooltip"><b>Heures&nbsp;:</b>
            <input name="assigned_hours" value="${values['assigned_hours']}" type="number"
                   style="width: 5em;"
                   min="0.25" step="0.25">&nbsp;h</label>
            <span class="ui-icon ui-icon-help"></span></p>
        <p class="ui-tooltip" hidden="hidden"><span class="ui-tooltip-content">
            Nombre d’heures de travail affectées à ${employee.employee_name} pour cette tâche.
            Par défaut, le nombre d’heures est égal au nombre d’heures estimées de la tâche.
            Affectez un nombre d’heures moindre si plusieurs personnes travaillent sur la même tâche.
        </span></p>
        %if 'assigned_hours'in form_errors:
        <p><span class="error">${form_errors['assigned_hours']}</span></p>
        %endif

        <p><label class="tooltip"><b>Taux&nbsp;:</b>
            <input name="rate_percent" value="${values['rate_percent']}" type="number"
                   style="width: 5em;"
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

        %if assignation_list:
        <details>
            <summary>Personnes déjà assignées</summary>
            <ol>
                %for assigned in assignation_list:
                <li>${assigned.get_assignation(tz_offset=hidden['tz_offset'])}</li>
                %endfor
            </ol>
        </details>
        %else:
        <p>Aucune assignation</p>
        %endif
    </form>
    <form action="${action_url}" method="post" class="delete ui-helper-hidden">
        <input type="hidden" name="_method" value="DELETE"/>
    </form>
    <script type="application/javascript" defer="defer">
    $(function() {
%if actions == "new":
        var thisDialog = $('#confirm_dialog').dialog({
            width: 550,
            height: 350,
            modal: true,
            buttons: {
                "Ajouter": function() {
                    $("#assignation_dialog form.new_or_edit").submit();
                },
                "Annuler": function() {
                    $(this).dialog("close");
                }
            },
            title: "${title|n}"
        });
%elif actions == "edit_or_delete":
        var thisDialog = $('#confirm_dialog').dialog({
            width: 550,
            height: 350,
            modal: true,
            buttons: {
                "Modifier": function() {
                    $("#assignation_dialog form.new_or_edit").submit();
                },
                "Supprimer": function() {
                    $("#assignation_dialog form.delete").submit();
                },
                "Annuler": function() {
                    $(this).dialog("close");
                }
            },
            title: "${title|n}"
        });
%endif

        var ajaxFormProp = {
            target: '#assignation_dialog',
            beforeSubmit: function(arr, form, options) {
                $("body").css("cursor", "progress");
                return true;
            },
            error: function(responseText, statusText, xhr) {
                var errorMsg = "Échec de connexion au serveur";
                if (responseText != null && typeof responseText === 'object') {
                    errorMsg += " : " + responseText.status + " \u2013 " + responseText.statusText;
                }
                $("body").css("cursor", "default");
                $('#confirm_dialog_content').html('<p><span class="error">' + errorMsg + '</span></p>');
                console.log(xhr);
            },
            success: function(responseText, statusText, xhr) {
                $("body").css("cursor", "default");
                var error = $('<div/>').append(responseText).find('span.error');
                if (error.length) {
                    $('#confirm_dialog_content').html(responseText);
                } else {
                    var url = "${tg.url('./{task.order_uid}/tasks/{task.uid}/assignations/'.format(task=task))|n}";
                    $('#${assignations_id}').load(url, "tz_offset=" + ${hidden['tz_offset']|n});
                    thisDialog.dialog("close");
                }
            }
        };

        $("#assignation_dialog form.new_or_edit").ajaxForm(ajaxFormProp);
        $("#assignation_dialog form.delete").ajaxForm(ajaxFormProp);

        thisDialog.dialog("open");

        $("#assignation_dialog").tooltip({
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


##
## Plan form : dialog box
## ======================
##
<%def name="plan_dialog(title,
                        question,
                        assignation,
                        **hidden)">
<%
task = assignation.order_phase
assignations_id = "assignations_{0}".format(task.uid)
action_url = tg.url('./{task.order_uid}/tasks/{task.uid}/assignations/{assignation.uid}/plan'.format(task=task, assignation=assignation))
%>
<section id="plan_dialog" title="${title}">
    <style scoped="scoped" type="text/css">
        #plan_dialog form p {
            margin-bottom: .5em;
        }
    </style>
    <form action="${action_url}" method="get" class="plan ui-widget">
        %for k, v in hidden.iteritems():
        <input type="hidden" name="${k}" value="${v}">
        %endfor
        <p>${question}</p>
        <p>${assignation.get_assignation(hidden["tz_offset"])}</p>
        %if assignation.planning_event_list:
        <div class="ui-widget">
            <div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em;">
                <p style="margin: 0.5em 0;"><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>
                    L’affectation est déjà planifiée.
                    Cliquer sur «&#160;Planifier&#160;» pour recommancer la planification,
                    ou sur «&#160;Annuler&#160;» pour abandonner.</p>
            </div>
        </div>
        %endif
    </form>
    <script type="application/javascript" defer="defer">
    $(function() {
        var thisDialog = $('#confirm_dialog').dialog({
            width: 550,
            height: 250,
            modal: true,
            buttons: {
                "Planifier": function() {
                    $("#plan_dialog form.plan").submit();
                },
                "Annuler": function() {
                    $(this).dialog("close");
                }
            },
            title: "${title|n}"
        });

        var ajaxFormProp = {
            target: '#plan_dialog',
            beforeSubmit: function(arr, form, options) {
                $("body").css("cursor", "progress");
                return true;
            },
            error: function(responseText, statusText, xhr) {
                var errorMsg = "Échec de connexion au serveur";
                if (responseText != null && typeof responseText === 'object') {
                    errorMsg += " : " + responseText.status + " \u2013 " + responseText.statusText;
                }
                $("body").css("cursor", "default");
                $('#confirm_dialog_content').html('<p><span class="error">' + errorMsg + '</span></p>');
                console.log(xhr);
            },
            success: function(responseText, statusText, xhr) {
                $("body").css("cursor", "default");
                var error = $('<div/>').append(responseText).find('span.error');
                if (error.length) {
                    $('#confirm_dialog_content').html(responseText);
                } else {
                    var url = "${tg.url('./{task.order_uid}/tasks/{task.uid}/assignations/'.format(task=task))|n}";
                    $('#${assignations_id}').load(url, "tz_offset=" + ${hidden['tz_offset']|n});
                    thisDialog.dialog("close");
                }
            }
        };

        $("#plan_dialog form.plan").ajaxForm(ajaxFormProp);

        thisDialog.dialog("open");
    });
    </script>
</section>
</%def>
