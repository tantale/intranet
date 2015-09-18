<%! import datetime %>
<%
duration0 = datetime.timedelta(days=0)
def duration(total):
    hours, remainder = divmod(int(total.total_seconds()), 3600)
    minute, seconds = divmod(remainder, 60)
    return "{hours:02d}:{minute:02d}".format(hours=hours, minute=minute)
%>
%for week_hours in week_hours_list:
<article id="week_hours_${week_hours.uid}">
    <h2><span id="week_hours_${week_hours.uid}_label" class="label editable"
              title="${_(u'Le libellé des horaires doit être unique')}">${week_hours.label}</span></h2>

    <p><span id="week_hours_${week_hours.uid}_description" class="description editable"
             title="${_(u'Description des horaires')}">${week_hours.description}</span></p>

    <table id="table_week_hours_${week_hours.uid}" cellpadding="0" cellspacing="2" border="0"
           style="page-break-inside: avoid">
        <thead>
        <tr>
            <th style="visibility: hidden;">Jours</th>
            %for day_period in week_hours.day_period_list:
            <th colspan="2" title="${day_period.description}">${day_period.label}</th>
            %endfor
            <th>Durée</th>
        </tr>
        </thead>
        <tbody>
        <% hours_interval_table = week_hours.get_hours_interval_table(week_day_list) %>
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
                total = sum([sum(((i and i.duration or duration0) for i in row), duration0)
                             for row in hours_interval_table], duration0)
                %>${duration(total)}</strong>&#x2003;</th>
        </tr>
        </tfoot>

    </table>

    <nav>
        <form id="week_hours_${week_hours.uid}_delete_form" class="delete_form inline_form"
              action="${tg.url('/admin/planning/week_hours/{0}/delete'.format(week_hours.uid))}"
              method="get">
            <p>
                <button id="week_hours_${week_hours.uid}_delete" type="submit" class="delete_button"
                        title="Supprimer le calendrier : ${week_hours.label}">${_(u"Supprimer")}
                </button>
            </p>
        </form>
    </nav>

</article>
%endfor

<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
        $('#week_hours .delete_form').ajaxForm({
            target: '#confirm_dialog_content'
        });
        $('#week_hours .delete_button').button({
            text: true,
            icons: {
                primary: "ui-icon-trash"
            }
        });
        // see: http://vitalets.github.io/x-editable/docs.html
        $('#week_hours .label.editable').editable({
            type: "text",
            clear: true,
            pk: "unused",
            url: "${tg.url('/admin/planning/week_hours/edit_in_place')}",
            title: "Saisir le libellé du calendrier",
            placeholder: "Libellé",
            emptytext: "(vide)",
            showbuttons: false,
            onblur: "cancel",
            success: function(response, newValue) {
                if (response.status === 'error') {
                    return response.msg;
                }
            },
            inputclass: "input-large label"
        });
        $('#week_hours .description.editable').editable({
            type: "textarea",
            rows: 2,
            clear: true,
            pk: "unused",
            url: "${tg.url('/admin/planning/week_hours/edit_in_place')}",
            title: "Saisir la description du calendrier",
            placeholder: "Description du calendrier",
            emptytext: "(vide)",
            showbuttons: true,
            onblur: "cancel",
            success: function(response, newValue) {
                if (response.status === 'error') {
                    return response.msg;
                }
            },
            inputclass: "input-large description"
        });
		$('#week_hours table').styleTable();
	});
</script>
