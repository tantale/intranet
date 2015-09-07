<!--
<%flash = tg.flash_obj.render('flash', use_js=False)%>
-->
<tr>
    <td>
        <!-- <%
        input_name = "label"
        input_title = _(u'Libellé du calendrier (il doit être unique)')
        input_placeholder = _(u'Libellé')
        has_error = input_name in form_errors
        input_cls = "error" if has_error else ""
        input_val = values.get(input_name, "")
        %> -->
        <input type="text" form="calendar_new__create_form"
               name="${input_name}" title="${input_title}" placeholder="${input_placeholder}"
               class="${input_cls}" value="${input_val}"/>
        %if has_error:
        <br/>
        <span class="error">${form_errors[input_name]}</span>
        %endif
    </td>
    <td>
        <!-- <%
        input_name = "description"
        input_title = _(u'Description du calendrier, contexte d’utilisation, etc.)')
        input_placeholder = _(u'Description du calendrier')
        has_error = input_name in form_errors
        input_cls = "error" if has_error else ""
        input_val = values.get(input_name, "")
        %> -->
    <textarea form="calendar_new__create_form"
              name="${input_name}" title="${input_title}" placeholder="${input_placeholder}"
              class="${input_cls}">${input_val}</textarea>
        %if has_error:
        <br/>
        <span class="error">${form_errors[input_name]}</span>
        %endif
    </td>
    <td>
        <!-- <%
        input_name = "employee_uid"
        input_title = _(u'Attribuer un calendrier à un employé')
        input_val = values.get(input_name, "")
        %> -->
        <select form="calendar_new__create_form"
                name="${input_name}" title="${input_title}">
            %if values.get('employee_uid'):
            <option value="" selected="selected">(aucun)</option>
            %else:
            <option value="">(aucun)</option>
            %endif
            %for employee in employee_list:
            %if input_val == employee.uid:
            <option value="${employee.uid}" selected="selected">${employee.employee_name}</option>
            %else:
            <option value="${employee.uid}">${employee.employee_name}</option>
            %endif
            %endfor
        </select>
    </td>
    <td>
        <!-- <%
        input_name = "week_hours_uid"
        input_title = _(u'Attribuer un calendrier à un employé')
        input_val = values.get(input_name, "")
        %> -->
        <select form="calendar_new__create_form"
                name="${input_name}" title="${input_title}">
            %for week_hours in week_hours_list:
            %if input_val == week_hours.uid:
            <option value="${week_hours.uid}" selected="selected">${week_hours.label}</option>
            %else:
            <option value="${week_hours.uid}">${week_hours.label}</option>
            %endif
            %endfor
        </select>
    </td>
    <td>
        <!-- fixme: URL -->
        <form id="calendar_new__create_form" class="create_form inline_form"
              action="${tg.url('/admin/planning/calendar/')}"
              method="post" enctype="multipart/form-data">
            <p>
                <button id="calendar_new__create" type="submit" class="create_button"
                        title="Ajouter un nouveau calendrier">${_(u"Créer")}
                </button>
            </p>
        </form>
    </td>
</tr>
%if flash and not cat_group:
<tr>
    <td colspan="5">
        ${flash | n}
    </td>
</tr>
%endif
<script type='text/javascript'><!--
    "use strict";
    /*global $*/
    $(function() {
        $('#calendar tfoot .create_button').button({
            text : false,
            icons : {
                primary : "ui-icon-plus"
            }
        });
        $('#calendar tfoot .create_form').ajaxForm({
            target : '#calendar tfoot',
            success:    function() {
                $('#calendar tbody').load("${tg.url('/admin/planning/calendar/get_all')}");
            }
        });
    });
-->
</script>
