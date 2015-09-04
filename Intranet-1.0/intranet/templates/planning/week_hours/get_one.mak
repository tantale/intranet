<%! import datetime %>
<%
duration0 = datetime.timedelta(days=0)
def duration(total):
hours, remainder = divmod(int(total.total_seconds()), 3600)
minute, seconds = divmod(remainder, 60)
return "{hours:02d}:{minute:02d}".format(hours=hours, minute=minute)
%>
<link rel="stylesheet" type="text/css" href="${tg.url('/css/blitzer/jquery-ui-1.10.3.custom.min.css')}"/>
<div id="week_hours_${week_hours.uid}">
    <style scoped="scoped">
        .ts-time {text-align: right;}
        .ts-start {color: rgb(238, 130, 14);}
        .ts-end {color: rgb(8, 151, 59);}
        .ts-delta {color: rgb(18, 151, 214);}
        .ts-interval-invalid {
        background-color: #f2dede;
        border-color: #eed3d7;
        color: #b94a48;
        }

        .styleTable { border-collapse: separate; }
        .styleTable TD { font-weight: normal !important; padding: .4em; border-top-width: 0px !important; }
        .styleTable TH { text-align: center; padding: .8em .4em; }
        .styleTable TD.first, .styleTable TH.first { border-left-width: 0px !important; }

    </style>
    <table id="table_week_hours_${week_hours.uid}" cellpadding="0" cellspacing="2" border="0"
           style="page-break-inside: avoid">
        <caption title="${week_hours.description}">${week_hours.label}</caption>
        <thead>
        <tr>
            <th style="visibility: hidden;">Jours</th>
            %for day_period in day_period_list:
            <th colspan="2" title="${day_period.description}">${day_period.label}</th>
            %endfor
            <th>Durée</th>
        </tr>
        </thead>
        <tbody>
        %for row_idx, row in enumerate(hours_interval_table):
        <%week_day = week_day_list[row_idx]%>
        <tr>
            <th title="${week_day.description}">${week_day.label}</th>
            %for hours_interval in row:
            %if hours_interval:
            <td>&#x2002;de <input size="5" class="ts-time ts-start" type="time" value="${hours_interval.start_hour}"/>
            </td>
            <td>à <input size="5" class="ts-time ts-end" type="time" value="${hours_interval.end_hour}"/>&#x2002;</td>
            %else:
            <td>&#x2002;de <input size="5" class="ts-time ts-start" type="time" value=""/></td>
            <td>à <input size="5" class="ts-time ts-end" type="time" value=""/>&#x2002;</td>
            %endif
            %endfor
            <td style="text-align: right"><strong class="ts-delta">${duration(sum(((i and i.duration or duration0) for i
                in row), duration0))}</strong>&#x2003;</td>
        </tr>
        %endfor
        </tbody>
        <tfoot>
        <tr>
            <th colspan="5" style="text-align: right">Durée totale de la semaine :</th>
            <th style="text-align: right"><strong><%
                total = sum([sum(((i and i.duration or duration0) for i in row), duration0) for row in
                hours_interval_table], duration0)
                %>${duration(total)}</strong>&#x2003;</th>
        </tr>
        </tfoot>

    </table>
    <script type='text/javascript' src="${tg.url('/javascript/jquery-1.9.1.js')}"></script>
    <script type='text/javascript' src="${tg.url('/javascript/jquery-ui-1.10.3.custom.min.js')}"></script>
    <script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
    <script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
		$('#table_week_hours_${week_hours.uid}').styleTable();
	});

    </script>
</div>