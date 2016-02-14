##
## Task form widget
## ================
##
<%def name="task_form(task, active_employees, form_errors=None, values=None)">
<%
STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_DONE = "PENDING", "IN_PROGRESS", "DONE"
task_id = "task_{0}".format(task.uid)
task_form_id = "task_form_{0}".format(task.uid)
form_errors = form_errors or dict()
values = values or dict()
obj_label = values.get("label") or task.label
obj_description = values.get("description") or task.description
obj_estimated_duration = values.get("estimated_duration") or task.estimated_duration
obj_remain_duration = values.get("remain_duration") or task.remain_duration
obj_task_status = values.get("task_status") or task.task_status
%>
<form id="${task_form_id}"
      action="${tg.url('./{task.order_uid}/tasks/{task.uid}'.format(task=task))}"
      method="post" enctype="multipart/form-data">
    <input type="hidden" name="_method" value="PUT"/>
    <input type="hidden" name="tz_offset">
    <fieldset class="task ui-widget">
        <div class="row-xs">
            <div class="col-xs-12">
                <input class="label" name="label" value="${obj_label}"
                       title="Nom de la tâche"/>
                %if 'label'in form_errors:
                <p><span class="error">${form_errors['label']}</span></p>
                %endif
            </div>
        </div>
        <div class="row-xs">
            <div class="col-xs-6">
                <label class="description" for="${task_form_id}__description">Description&nbsp;:</label>
                        <textarea class="description" id="${task_form_id}__description" name="description"
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
                            <input name="estimated_duration" type="number" value="${obj_estimated_duration}"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée estimée à partir des statistiques"/>
                            %else:
                            <input name="estimated_duration" type="number" value="${obj_estimated_duration}"
                                   readonly="readonly"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée estimée à partir des statistiques"/>
                            %endif
                        </td>
                        <td>
                            <input name="tracked_duration" type="number" value="${task.tracked_duration}"
                                   readonly="readonly"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée déjà effectuée et pointée"/>
                        </td>
                        <td>
                            %if obj_task_status in [STATUS_PENDING, STATUS_IN_PROGRESS]:
                            <input name="remain_duration" type="number" value="${obj_remain_duration}"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée restante estimée"/>
                            %else:
                            <input name="remain_duration" type="number" value="${obj_remain_duration}"
                                   disabled="disabled"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée restante estimée"/>
                            %endif
                        </td>
                        <td>
                            <input name="total_duration" type="number" value="$task.total_duration}"
                                   disabled="disabled"
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
                                <label title="${status_info['description']}"><input type="radio" checked="checked"
                                                                                    value="${status_info['value']}"
                                                                                    name="task_status"/>${status_info['label']}</label>
                                %else:
                                <label title="${status_info['description']}"><input type="radio"
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
            <div class="col-xs-2">
                <label class="assignment">Affectation(s)&nbsp;:</label>
            </div>
            <div class="col-xs-10">
                <div class="assignment">
                    <%
                    unassigned_employees = list(task.get_unassigned_employees(active_employees))
                    unassigned_employees.sort(key=lambda e: e.employee_name)
                    %>
                    %if unassigned_employees:
                    <div class="badge ui-widget ui-state-default ui-corner-all">
                        <!--
                        <select name="employee_uid" class="add ui-widget ui-state-default ui-corner-all"
                                title="Liste des employés">
                            <option value="" selected="selected">&lt;Ajoutez&gt;</option>
                            %for employee in task.get_unassigned_employees(active_employees):
                            <option value="${employee.uid}">${employee.employee_name}</option>
                            %endfor
                        </select>
                        -->
                    </div>
                    %endif
                </div>
            </div>
        </div>
        <div class="row-xs">
            <div class="col-xs-12">
                <nav>
                    <button type="submit" class="refresh_button"
                            title="Met à jour la planificarion de la tâche">Re-estimer</button>
                    <button type="submit" class="update_button"
                            title="Modifier la tâche">Appliquer</button>
                </nav>
            </div>
        </div>
    </fieldset>
</form>
<script type="application/javascript" defer="defer">
    $(function() {
        var today = new Date();
        var tz_offset = today.getTimezoneOffset();
        $('#${task_form_id}').find('input[name=tz_offset]').val(tz_offset);
        $('#${task_form_id}').ajaxForm({target: '#${task_id}'});
    });
</script>
</%def>
