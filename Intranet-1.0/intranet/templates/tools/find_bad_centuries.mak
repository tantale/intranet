# -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<%def name="title()">${tool['label']}</%def>

<h2>${tool['title']}</h2>

%if employee_list:
<p>${_(u'Enregistrements problématiques dans la table des employés :')}</p>
%else:
<p><em>${_(u'Aucun enregistrement problématique dans la table des employés.')}</em></p>
%endif

%if employee_list:
<table class="record-table" style="page-break-inside: avoid">
<thead>
<tr>
<th class="record-table-uid">uid</th>
<th class="record-table-date">entry_date</th>
<th class="record-table-date">exit_date</th>
<th class="record-table-label">employee_name</th>
</tr>
</thead>
<tbody>
%for employee in employee_list:
<tr>
<td class="record-table-uid">${employee.uid}</td>
<td class="record-table-date">${employee.entry_date}</td>
<td class="record-table-date">${employee.exit_date}</td>
<td class="record-table-label">${employee.employee_name}</td>
</tr>
%endfor
</tbody>
</table>
%endif

%if order_list:
<p>${_(u'Enregistrements problématiques dans la table des commandes :')}</p>
%else:
<p><em>${_(u'Aucun enregistrement problématique dans la table des commandes.')}</em></p>
%endif

%if order_list:
<table class="record-table" style="page-break-inside: avoid">
<thead>
<tr>
<th class="record-table-uid">uid</th>
<th class="record-table-date">creation_date</th>
<th class="record-table-date">close_date</th>
<th class="record-table-label">order_ref</th>
</tr>
</thead>
<tbody>
%for order in order_list:
<tr>
<td class="record-table-uid">${order.uid}</td>
<td class="record-table-date">${order.creation_date}</td>
<td class="record-table-date">${order.close_date}</td>
<td class="record-table-label">${order.order_ref}</td>
</tr>
%endfor
</tbody>
</table>
%endif

%if cal_event_list:
<p>${_(u'Enregistrements problématiques dans la table des événements :')}</p>
%else:
<p><em>${_(u'Aucun enregistrement problématique dans la table des événements.')}</em></p>
%endif

%if cal_event_list:
<table class="record-table" style="page-break-inside: avoid">
<thead>
<tr>
<th class="record-table-uid">uid</th>
<th class="record-table-datetime">event_start</th>
<th class="record-table-datetime">event_end</th>
<th class="record-table-label">ref / label</th>
</tr>
</thead>
<tbody>
%for cal_event in cal_event_list:
<%
ref_label = _(u"{ref}\u00a0: {label}").format(ref=cal_event.order_phase.order.order_ref,
                                              label=cal_event.order_phase.label)
%>
<tr>
<td class="record-table-uid">${cal_event.uid}</td>
<td class="record-table-datetime">${cal_event.event_start}</td>
<td class="record-table-datetime">${cal_event.event_end}</td>
<td class="record-table-label">${ref_label}</td>
</tr>
%endfor
</tbody>
</table>
%endif

%if employee_list or order_list or cal_event_list:
<p><a href="./fix_bad_centuries">${_(u"Corriger les problèmes")}</a></p>
%else:
<p><strong>${_(u"Aucun problème détecté au niveau des dates.")}</strong></p>
%endif

<br>
<hr width="50%" align="left">

<%def name="script()">
<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(".record-table").styleTable();
</script>
</%def>
