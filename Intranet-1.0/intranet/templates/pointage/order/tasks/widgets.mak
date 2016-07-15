<%namespace file="intranet.templates.pointage.order.tasks.assignations.widgets" import="assignations"/>
##
## Task form widget
## ================
##
<%def name="task_form(task, active_employees, form_errors=None, values=None, **hidden)">
<%
STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE = "PENDING", "IN_PROGRESS", "DONE"
task_id = "task_{0}".format(task.uid)
task_form_id = "task_form_{0}".format(task.uid)
assignations_id = "assignations_{0}".format(task.uid)
form_errors = form_errors or dict()
values = values or dict()
obj_label = values.get("label") or task.label
obj_description = values.get("description") or task.description
obj_estimated_duration = values.get("estimated_duration") or task.estimated_duration
obj_remain_duration = values.get("remain_duration") or task.remain_duration
obj_task_status = values.get("task_status") or task.task_status
plan_status_info = task.plan_status_info
can_plan = plan_status_info['can_plan']
can_plan_cls = "ui-icon ui-icon-circle-check" if can_plan else "ui-icon ui-icon-triangle-1-e"
%>
<form id="${task_form_id}" class="ui-widget"
      action="${tg.url('./{task.order_uid}/tasks/{task.uid}'.format(task=task))}"
      method="post" enctype="multipart/form-data">
    <input type="hidden" name="_method" value="PUT"/>
    %for hidden_name, hidden_value in hidden.iteritems():
    <input type="hidden" name="${hidden_name}" value="${hidden_value}">
    %endfor
    <fieldset class="task ui-widget-content">
        <div class="row-xs">
            <div class="col-xs-9">
                <input class="change label" name="label" value="${obj_label}"
                       title="Nom de la tâche"/>
                %if 'label'in form_errors:
                <p><span class="error">${form_errors['label']}</span></p>
                %endif
            </div>
            <div class="col-xs-3">
                <span class="ui-widget">
                    <span class="ui-state-default ui-corner-all" style="padding: 0 .7em;">
                        <span>
                            <span class="${can_plan_cls}" style="float: left; margin-right: .3em;"></span>
                            <span title="${plan_status_info['description']}">${plan_status_info['label']}</span>
                        </span>
                    </span>
                </span>
            </div>
        </div>
        <div class="row-xs">
            <div class="col-xs-6">
                <label class="description" for="${task_form_id}__description">Description&nbsp;:</label>
                        <textarea class="change description" id="${task_form_id}__description" name="description"
                                  title="Description de la tâche à effectuer"
                                  rows="3" cols="30">${obj_description}</textarea>
                %if 'description'in form_errors:
                <p><span class="error">${form_errors['description']}</span></p>
                %endif
            </div>
            <div class="col-xs-6">
                <table class="charge">
                    <thead>
                    <tr>
                        <th></th>
                        <th>Estimée</th>
                        <th>Effectuée</th>
                        <th>Restante</th>
                        <th>Totale</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <th>Charge&nbsp;:</th>
                        <td>
                            %if obj_task_status in [STATUS_PENDING]:
                            <input class="change"
                                   name="estimated_duration" type="number" value="${obj_estimated_duration}"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée estimée à partir des statistiques"/>
                            %else:
                            <input class="change"
                                   name="estimated_duration" type="number" value="${obj_estimated_duration}"
                                   readonly="readonly"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée estimée à partir des statistiques"/>
                            %endif
                        </td>
                        <td>
                            <input class="change"
                                   name="tracked_duration" type="number" value="${task.tracked_duration}"
                                   readonly="readonly"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée déjà effectuée et pointée"/>
                        </td>
                        <td>
                            %if obj_task_status in [STATUS_PENDING, STATUS_IN_PROGRESS]:
                            <input class="change"
                                   name="remain_duration" type="number" value="${obj_remain_duration}"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée restante estimée"/>
                            %else:
                            <input class="change"
                                   name="remain_duration" type="number" value="${obj_remain_duration}"
                                   readonly="readonly"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée restante estimée"/>
                            %endif
                        </td>
                        <td>
                            <input class="change"
                                   name="total_duration" type="number" value="${task.total_duration}"
                                   readonly="readonly"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée totale : effectuée + restante"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Statut&nbsp;:</th>
                        <td colspan="4">
                            <div class="task_status">
                                %for status_info in task.all_status_info:
                                %if status_info['checked']:
                                <label title="${status_info['description']}"><input class="change"
                                                                                    type="radio" checked="checked"
                                                                                    value="${status_info['value']}"
                                                                                    name="task_status"/>${status_info['label']}</label>
                                %else:
                                <label title="${status_info['description']}"><input class="change"
                                                                                    type="radio"
                                                                                    value="${status_info['value']}"
                                                                                    name="task_status"/>${status_info['label']}</label>
                                %endif
                                %endfor
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
        %if 'exc'in form_errors:
        <div class="row-xs">
            <div class="col-xs-12">
                <p><span class="error">${form_errors['exc']}</span></p>
            </div>
        </div>
        %endif
        <div class="row-xs">
            <div class="col-xs-12">
                <nav>
                    <button type="button" class="refresh_button"
                            title="Recalcul les durées de la tâche">Réévaluer</button>
                    <button type="submit" class="update_button"
                            title="Appliquer les modifications sur la tâche">Appliquer</button>
                    <button type="reset" class="cancel_button"
                            title="Annuler les modifications">Annuler</button>
                </nav>
            </div>
        </div>
    </fieldset>
</form>
<div>
    <div class="row-xs">
        <div class="col-xs-2">
            <label class="assignations" style="display: inline-block; margin-top: 1.7em;">Affectation(s)&nbsp;:</label>
        </div>
        <div class="col-xs-10">
            <div id="${assignations_id}" class="assignations">
            ${assignations(task, active_employees, **hidden)}
            </div>
        </div>
    </div>
</div>
<script type="application/javascript" defer="defer">
    $(function() {
        var today = new Date();
        var tz_offset = today.getTimezoneOffset();
        $('#${task_form_id}').find('input[name=tz_offset]').val(tz_offset);

        $('#${task_form_id}').ajaxForm({target: '#${task_id}'});

        $('#${task_form_id} .refresh_button').button({
            text : true,
            disabled: false,
            icons : {
                primary : "ui-icon-refresh"
            }
        })
        .click(function(event){
            var error = function(response, status, xhr) {
                var msg = '<p><span class="error">Désolé mais il y a eu une erreur. ' +
                'statut : ' + xhr.status + ', ' +
                'message : "' + xhr.statusText + '".</span></p>';
                $('#confirm_dialog_content').html(msg);
                $('#confirm_dialog').dialog({
                    width: 500,
                    height: 200,
                    buttons: {
                        "Annuler": function() {
                            $(this).dialog("close");
                        }
                    },
                    title: "Réévaluer la tâche \"${task.label}\""
                }).dialog("open");
            }

            var success = function(response, status, xhr) {
                var thisDialog = $('#confirm_dialog').dialog({
                    width: 500,
                    height: 300,
                    buttons: {
                        "Réévaluer" : function() {
                            $('#estimate_one_form').submit();
                        },
                        "Annuler": function() {
                            $(this).dialog("close");
                        }
                    },
                    title: "Réévaluer la tâche \"${task.label}\""
                });

                var ajaxFormProp = {
                    beforeSubmit: function(arr, form, options) {
                        $("body").css("cursor", "progress");
                        return true;
                    },
                    error: function(responseText, statusText, xhr) {
                        $("body").css("cursor", "default");
                        $('#confirm_dialog_content').html('<p><span class="error">Échec de connexion au serveur</span></p>');
                    },
                    success: function(responseText, statusText, xhr) {
                        $("body").css("cursor", "default");
                        var error = $('<div/>').append(responseText).find('span.error');
                        if (error.length) {
                            $('#confirm_dialog_content').html(responseText);
                            $('#estimate_one_form').ajaxForm(ajaxFormProp);
                        } else {
                            $('#${task_id}').html(responseText);
                            thisDialog.dialog("close");
                        }
                    }
                };

                $('#estimate_one_form').ajaxForm(ajaxFormProp);

                thisDialog.dialog("open");
            }

            var url = "${tg.url('./{task.order_uid}/tasks/estimate_one_form'.format(task=task))|n}";

            $('#confirm_dialog_content').load(url,
                {
                    uid: ${task.uid},
                    closed: $('#${task_form_id} input[name=closed]').val(),
                    max_count: $('#${task_form_id} input[name=max_count]').val(),
                    tz_offset: $('#${task_form_id} input[name=tz_offset]').val()
                },
                function(response, status, xhr){
                    if (status == "error") {
                        error(response, status, xhr);
                    } else {
                        success(response, status, xhr);
                    }
                });

        });

        $('#${task_form_id} .update_button').button({
            text : true,
            disabled: true,
            icons : {
                primary : "ui-icon-pencil"
            }
        });

        $('#${task_form_id} .cancel_button').button({
            text : true,
            disabled: true,
            icons : {
                primary : "ui-icon-cancel"
            }
        })
        .click(function(event){
            $(this).closest('form').get(0).reset();
            $('#${task_form_id} .update_button').button("disable");
            $('#${task_form_id} .cancel_button').button("disable");
        });

        $('#${task_form_id} .change').change(function(){
            $('#${task_form_id} .update_button').button("enable");
            $('#${task_form_id} .cancel_button').button("enable");
        });

        %if obj_task_status in [STATUS_IN_PROGRESS, STATUS_DONE]:
        $('#${task_form_id} .refresh_button').button("disable");
        %endif
    });
</script>
</%def>
