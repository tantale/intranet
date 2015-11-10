# -*- coding: utf-8 -*-
## cal_start=cal_start,
## cal_end=cal_end,
## cal_curr=cal_curr,  # @deprecated
## employee=employee,
## employee_list=employee_list
<%
if employee is None:
    img_src = tg.url('/images/silhouette-question.min.png')
    img_alt = "Silhouette inconnue"
elif employee.photo_path:
    img_src = employee.photo_path
    img_alt = employee.employee_name + " - Photo"
else:
    img_src = tg.url('/images/silhouette.min.png')
    img_alt = "Silhouette"
%>\

## -- Display the "Control recorded times" button to the right
%if employee:
<form id="ctrl_rec_times" class="inline_form" style="float: right;"
    action="${tg.url('./ctrl_rec_times')}" method="get">
    <input type="hidden" name="employee_uid" value="${employee.uid}"/>
    <input type="hidden" name="week_start"/>
    <input type="hidden" name="week_end"/>
    <input type="hidden" name="tz_offset"/>
    <button id="ctrl_rec_times__ctrl" type="submit" class="ctrl_button"
        title="Contrôler les pointages de la semaine">Contrôler les pointages</button></td>
</form>
<form id="print_rec_times" class="ui-helper-hidden" target='_blank'
    action="${tg.url('./print_rec_times')}" method="get">
    <input type="hidden" name="employee_uid" value="${employee.uid}"/>
    <input type="hidden" name="week_start"/>
    <input type="hidden" name="week_end"/>
    <input type="hidden" name="tz_offset"/>
    <button id="print_rec_times__print" type="submit" class="print_button"
        title="Imprimer les pointages de la semaine">Imprimer les pointages</button></td>
</form>
%endif

## -- Display the list of employees
<form id="employee_refresh" class="inline_form"
    action="${tg.url('./get_all/')}" method="get">
    <p><img class="valignMiddle picture_box_inner_min"
            id="employee_refresh__picture"
            alt="${img_alt}"
            src="${img_src}" />
        <select id="employee_refresh__select" name="employee_uid"
            class="ui-widget ui-state-default ui-corner-all"
            title="Liste des employés">
            %if not employee:
            <option selected="selected"
                value="">(Sélectionnez un employé)</option>
            %endif
            %for option in employee_list:
            %if employee and option.uid == employee.uid:
            <option selected="selected"
                value="${option.uid}">${option.employee_name}</option>
            %else:
            <option
                value="${option.uid}">${option.employee_name}</option>
            %endif
            %endfor
        </select>
        <input type="hidden" name="cal_start" value="${cal_start}" />
        <input type="hidden" name="cal_end" value="${cal_end}" />
        <button id="employee_refresh__refresh" type="submit" class="refresh_button"
            title="Mettre à jour le calendrier des pointages">Mettre à jour</button>
    </p>
</form>
<div style="ui-helper-clearfix"></div>

<script type='text/javascript'>
    "use strict";
    /*global $*/
    $('#employee_refresh').ajaxForm({
        target : '#calendar_content',
        beforeSubmit: function(arr, form, options) {
            $('#flash').hide();
        }
    });
    $('#employee_refresh .refresh_button').button({
        text : false,
        icons : {
            primary : "ui-icon-refresh"
        }
    });
    $('#employee_refresh__select').change(function(){
        $('#employee_refresh').submit();
    });
##
## -- Display the "Control recorded times" button to the right
%if employee:
    $('#ctrl_rec_times .ctrl_button').button({
        text : true,
        icons : {
            primary : "ui-icon-check"
        }
    });
    $('#ctrl_rec_times, #print_rec_times').submit(function(event){
        // -- Compute the start/end dates of the week (or month)
        var calendar = $('#calendar'), // fullCalendar object
            view = calendar.fullCalendar('getView'), // viewObject
            week_start = view.visStart,
            week_end = view.visEnd;
        if (view.name === "basicDay" || view.name === "agendaDay") {
            var firstDay = calendar.fullCalendar('option', 'firstDay'), // int
                days = (week_start.getDay() === 0) ?
                        (7 - firstDay) % 7 :
                        week_start.getDay() - firstDay;
            week_start = view.visStart;
            week_start.setDate(week_start.getDate() - days); // Monday
            week_end = new Date(week_start);
            week_end.setDate(week_end.getDate() + 7);
        }
        $(event.target).find('input[name=week_start]').val(week_start.getTime() / 1000);
        $(event.target).find('input[name=week_end]').val(week_end.getTime() / 1000);
        $(event.target).find('input[name=tz_offset]').val(week_start.getTimezoneOffset());
    });
    $('#ctrl_rec_times').ajaxForm({
        target : '#confirm_dialog_content',
        beforeSubmit: function(arr, form, options) {
            $('#flash').hide();
        },
        success: function(responseText, statusText, xhr) {
            $('#confirm_dialog').dialog({
                width: 	620,
                height: 500,
                buttons: {
                    "OK": function() {
                        $(this).dialog("close");
                    },
                    "Imprimer": function() {
                        $('#print_rec_times').submit();
                    }
                },
                title: "Contrôle des pointages",
                close: function() {
                }
            }).dialog("open");
        },
        error: function() {
            var title = "Erreur de connexion HTTP",
                text = "Impossible contrôler les événements\u00a0!";
            display_err_dialog(title, text);
        }
    });
    $('#print_rec_times .print_button').button({
        text : true,
        icons : {
            primary : "ui-icon-print"
        }
    });
%endif
</script>
