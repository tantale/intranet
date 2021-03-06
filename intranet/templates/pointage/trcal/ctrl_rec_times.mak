# -*- coding: utf-8 -*-
##        return dict(employee_uid=employee_uid,
##                    employee_name=employee.employee_name,
##                    worked_hours=employee.worked_hours,
##                    week_start=week_start,
##                    week_end=week_end,
##                    week_list=week_list)
<%
def format_number(number):
    value = "{:0.2f}".format(number)
    return value.replace(".", ",")

%>
<div id='ctrl_rec_times' class="ctrl-page">
    <h2>Contrôle du pointage de ${employee_name}</h2>

    <p class="alignCenter">h/sem. travaillées : <span
        id="ctrl_rec_times__worked_hours">${worked_hours}</span></p>

    <p class="alignCenter">Période du <span
        id="ctrl_rec_times__week_start">${week_start}</span> au <span
        id="ctrl_rec_times__week_end">${week_end}</span></p>

    <table class="ctrl-table" style="page-break-inside: avoid">
    <caption>Nombre d’heures par semaine</caption>
    <thead>
    <tr>
    <th>Semaine</th>
    <th>Lun.</th>
    <th>Mar.</th>
    <th>Mer.</th>
    <th>Jeu.</th>
    <th>Ven.</th>
    <th>Sam.</th>
    <th>Dim.</th>
    <th>Total</th>
%if display_messages:
    <th>Statut</th>
%else:
    <th></th>
%endif
    </tr>
    </thead>
    <tbody>
%for week in week_list:
    <%
    week_number = week['week_number']
    day_list = week['day_list']
    duration_total = week['duration_total']
    message = week['message']
    status = week['status']
    icon = week['icon']
    %>
    <tr class="${status}" title="${message}">
    <th>Sem. ${week_number}</th>
%for day in day_list:
    <td class="alignRight">${format_number(day)}</td>
%endfor
    <td class="alignRight"><strong>${format_number(duration_total)}</strong></td>
%if display_messages:
    <td>${message}</td>
%else:
    <td><span class="ui-icon ${icon}"></span></td>
%endif
    </tr>
%endfor
    </tbody>
    </table>

<script type='text/javascript'>
    "use strict";
    /*global $*/
    $(function() {
        $('#ctrl_rec_times__week_start').text((new Date(${week_start} * 1000)).toLocaleDateString());
        $('#ctrl_rec_times__week_end').text((new Date(${week_end} * 1000)).toLocaleDateString());
        $('#ctrl_rec_times .ctrl-table').styleTable();
    });
</script>

</div>