# -*- coding: utf-8 -*-
<%!
import datetime
import json
%>
<%
def format_date(date):
	return "{date:%d/%m/%Y}".format(date=date)

curr_date = format_date(datetime.date.today())

def format_number(number):
	value = "{:0.2f}".format(number)
	return value.replace(".", ",")

%>
<div class="chart-page">
	<h2 class="colorFrame ${order.project_cat}">Bilan des pointages de « ${order.order_ref} »</h2>
##
## header
##
	<p><strong>Bilan des pointages à la date du :</strong> ${curr_date}
	<p><strong>N° commande :</strong> ${order.uid}</p>
	<p><strong>Ref. commande :</strong> ${order.order_ref}</p>
	<p><strong>Date de création :</strong> ${format_date(order.creation_date)}</p>
%if order.close_date is None:
	<p><strong>Date de clôture :</strong> <em>(aucune)</em></p>
	<p><em>Note : cette commande n’est pas clôturée ; le bilan est donc temporaire.</em></p>
%else:
	<p><strong>Date de clôture :</strong> ${format_date(order.close_date)}</p>
%endif

<% total_count = sum(statistics.values()) %>
%if order.order_phase_list and total_count:
##
## chart-table
##
	<table class="chart-table" style="page-break-inside: avoid">
	<caption>Tableau des pointages</caption>
	<thead>
	<tr>
	<th>N°</th>
	<th>Phase<br />de production</th>
	<th>Heures pointées<br />(h)</th>
	<th>Pourcentage</th>
	</tr>
	</thead>
	<tbody>
%for order_phase in order.order_phase_list:
	<%
	key = (order_phase.position, order_phase.label)
	count = statistics[key]
	%>
	<tr>
	<td class="chart-table-position">${order_phase.position}</td>
	<td class="chart-table-label">${order_phase.label}</td>
	<td class="chart-table-count">${format_number(count)}</td>
	<td class="chart-table-percent">${"{percent:.1%}".format(percent=float(count) / total_count)}</td>
	</tr>
%endfor
	</tbody>
	<tfoot>
	<tr>
	<th class="chart-table-summary" colspan="2">Total de la commande :</th>
	<th class="chart-table-count">${format_number(total_count)}</th>
	<th class="chart-table-percent">${"{percent:.1%}".format(percent=1.0)}</th>
	</tr>
	</tfoot>
	</table>
##
## chart-pie
##
	<div id="chart-pie" style="margin-left: auto; margin-right: auto; width: 600px; height: 500px;"></div>
%else:
	<h3>Avertissement</h3>
	<p><strong>Cette commande ne contient pas de pointage.</strong></p>
%endif
	</div><!-- /chart-page -->

%if order.order_phase_list and total_count:
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(".chart-table").styleTable();
</script>
##
## json data for chart-pie
##
<%
title = u"Taux de pointage de « {order_ref} » par phase".format(order_ref=order.order_ref)
title_json = json.dumps(title)
data_table = [[u"Phase de production", u"Heures pointées"]]
for order_phase in order.order_phase_list:
	key = (order_phase.position, order_phase.label)
	count = statistics[key]
	data_table.append([u"{position} - {label}".format(position=order_phase.position, label=order_phase.label),
	                   count])
data_table_json = json.dumps(data_table)
%>
<script type='text/javascript'>
	"use strict";

	function drawChart() {
		var data = google.visualization.arrayToDataTable(${data_table_json|n});
		var options = {
			title: ${title_json|n}
		};
		var chart = new google.visualization.PieChart($('#chart-pie')[0]);
		chart.draw(data, options);
	}

	function loadPies() {
		google.load("visualization", "1", {packages: ["corechart"], callback: drawChart});
	}

	loadPies();
</script>
%endif
