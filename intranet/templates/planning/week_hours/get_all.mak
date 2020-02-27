<%! import datetime %>
<%namespace file="intranet.templates.planning.week_hours.day_period.day_period_label" import="day_period_label"/>
<%
duration0 = datetime.timedelta(days=0)
def duration(total):
    hours, remainder = divmod(int(total.total_seconds()), 3600)
    minute, seconds = divmod(remainder, 60)
    return "{hours:02d}:{minute:02d}".format(hours=hours, minute=minute)
%>
%for week_hours in week_hours_list:
<!--
<%
article_id = "week_hours_{0}".format(week_hours.uid)
%>
-->
<article id="${article_id}">
    <h2><span id="${article_id}_label" class="label editable"
              title="${_(u'Le libellé des horaires doit être unique')}">${week_hours.label}</span></h2>

    <p><span id="${article_id}_description" class="description editable"
             title="${_(u'Description des horaires')}">${week_hours.description}</span></p>

    <table class="ts-grid" id="${article_id}_table" cellpadding="0" cellspacing="2" border="0"
           style="page-break-inside: avoid">
        <thead>
        <tr>
            <th style="visibility: hidden;">Jours</th>
            %for col, day_period in enumerate(week_hours.day_period_list):
            <% placeholder_id = "week_hours_{0}_day_period_{1}_placeholder".format(week_hours.uid, day_period.uid) %>
            <th class="ts-col-${col}" id="${placeholder_id}">${day_period_label(week_hours.uid, day_period)}</th>
            %endfor
            <th class="new_day_period" style="display: none;"
                id="${article_id}_new_day_period"><!-- placeholder --></th>
            <th><input id="${article_id}_toggle"
                       class="toggle_button_icon" type="checkbox"><label for="${article_id}_toggle"
                       title="${u'Afficher/masquer les nouvelles plages horaires'}">+</label>
                Durée&#x2003;</th>
        </tr>
        </thead>
        <tbody>
        <% hours_interval_table = week_hours.get_hours_interval_table(week_day_list) %>
        %for row_idx, row in enumerate(hours_interval_table):
        <%week_day = week_day_list[row_idx]%>
        <tr class="ts-row">
            <th title="${week_day.description}">${week_day.label}</th>
            %for col, hours_interval in enumerate(row):
            <td class="ts-range">&#x2002;de <input
                    id="start_${hours_interval.week_day_uid}_${hours_interval.day_period_uid}"
                    size="5"
                    class="ts-start"
                    type="time"
                    step="900"
                    value="${hours_interval.start_hour}"/>
                à <input
                    id="end_${hours_interval.week_day_uid}_${hours_interval.day_period_uid}"
                    size="5"
                    class="ts-end"
                    type="time"
                    step="900"
                    value="${hours_interval.end_hour}"/>&#x2002;</td>
            %endfor
            <td class="ts-range new_day_period" style="display: none;">&#x2002;de <input size="5"
                                                                                         class="ts-start"
                                                                                         type="time"
                                                                                         step="900"
                                                                                         disabled="disabled"/>
                à <input size="5"
                         class="ts-end"
                         type="time"
                         step="900"
                         disabled="disabled"/>&#x2002;</td>
            <td style="text-align: right;"><strong class="ts-sum"></strong>&#x2003;</td>
        </tr>
        %endfor
        </tbody>
        <tfoot>
        <tr>
            <th colspan="${1 + len(week_hours.day_period_list)}" style="text-align: right">Durée totale de la semaine :</th>
            <th class="new_day_period" style="display: none;"></th>
            <th><strong class="ts-total"></strong>&#x2003;</th>
        </tr>
        </tfoot>

    </table>

    <nav>
        <form id="${article_id}_delete_form" class="delete_form inline_form"
              action="${tg.url('/admin/planning/week_hours/{0}/delete'.format(week_hours.uid))}"
              method="get">
            <p>
                <button id="${article_id}_delete" type="submit" class="delete_button"
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
            error: function(response, newValue) {
                response = JSON.parse(response.responseText);
                return response.msg;
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
            error: function(response, newValue) {
                response = JSON.parse(response.responseText);
                return response.msg;
            },
            inputclass: "input-large description"
        });
		$('#week_hours table').styleTable().workedHoursGrid({
            units: {
                hours: "h",
                minutes: "min",
                seconds: "s"
            },
            selectors: {
                row: ".ts-row",
                range: ".ts-range",
                start: ".ts-start",
                end: ".ts-end",
                sum: ".ts-sum",
                total: ".ts-total"
            }
        });
        $('#week_hours table input').change(function(){
            var
                id = $(this).attr("id") || "",
                parts = id.split("_"),
                range = $(this).closest(".ts-range"),
                data = {
                    week_day_uid: parts[1],
                    day_period_uid: parts[2],
                    start_hour: $(range).find(".ts-start").val(),
                    end_hour: $(range).find(".ts-end").val()
                },
                url = "${tg.url('/admin/planning/week_hours/edit_hours_interval')}";
            if (id.startsWith("start_") || id.startsWith("end_")) {
                $.post(url, data, function(data, textStatus, jqXHR) {
                    console.log(data);
                    console.log(textStatus);
                }, "json");
            }
        });
        $('#week_hours .toggle_button_icon').button({
            text: false,
            icons: {
                primary: "ui-icon-arrowreturnthick-1-s"
            }
        }).click(function(event){
            event.preventDefault();
            var week_hours_uid = $(this).parents("article").attr("id").split("_")[2];
            var url = "/admin/planning/week_hours/" + week_hours_uid + "/day_periods/new";
            var target = "#week_hours_" + week_hours_uid + "_new_day_period";
            var parent_table = $(this).parents("table");
            $(target).load(url, function(){
                parent_table.find('.new_day_period').show();
                parent_table.find('.new_day_period input:first').focus().tooltip({
                    position: {
                        my: "center top",
                        at: "center bottom+5"
                    },
                    show: {duration: 500},
                    hide: {duration: 1500},
                    tooltipClass: "info"
                }).tooltip("open");
            })
        });
	});
</script>
