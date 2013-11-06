# -*- coding: utf-8 -*-
##        return dict(employee_uid=employee_uid,
##                    employee_name=employee.employee_name,
##                    worked_hours=employee.worked_hours,
##                    week_start=week_start,
##                    week_end=week_end,
##                    week_list=week_list)
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
	<th>Sem.</th>
	<th>Lun.</th>
	<th>Mar.</th>
	<th>Mer.</th>
	<th>Jeu.</th>
	<th>Ven.</th>
	<th>Sam.</th>
	<th>Dim.</th>
	<th>Total</th>
	<th></th>
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
	<td class="alignRight">${day}</td>
%endfor
	<td class="alignRight"><strong>${duration_total}</strong></td>
	<td><span class="ui-icon ${icon}"></span></td>
	</tr>
%endfor
	</tbody>
	</table>

<script type='text/javascript'>
	"use strict";
	/*global $*/
	$('#ctrl_rec_times__week_start').text((new Date(${week_start} * 1000)).toLocaleDateString());
	$('#ctrl_rec_times__week_end').text((new Date(${week_end} * 1000)).toLocaleDateString());
	$('#ctrl_rec_times .ctrl-table').styleTable();
</script>

</div>