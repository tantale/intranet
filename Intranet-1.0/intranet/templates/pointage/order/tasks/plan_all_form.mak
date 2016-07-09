<section id="plan_section">
    <style scoped="scoped" type="text/css">
        #plan_section label b {
            display: inline-block;
            width: 18em;
        }
        span.help-content {
            font-size: .9em;
        }
        .ui-icon-help {
            display: inline-block;
        }
    </style>
    <header>
        <h3 class="tooltip">${title}
            <span class="ui-icon ui-icon-help"></span></h3>
        <p class="ui-tooltip" hidden="hidden"><span class="ui-tooltip-content">
            Planification de toutes les tâches selon les règles suivantes :

            les tâches sont prises dans l'ordre des phases
            &#9702;&#160;les tâches sans affectation sont ignorées
            &#9702;&#160;les tâches clôturées ne peuvent pas être planifiées et sont aussi ignorées
            &#9702;&#160;les affectations déjà planifiées sont ignorées (la planification courante sera conservée)
            &#9702;&#160;la date et l’heure de fin d’une tâche conditionnera la date et l’heure de début de planification
            de la tâche suivante : les tâches sont censées s’enchainer dans l’ordre chronologique (sans chevauchement).
        </span></p>
    </header>
    <form id="plan_all_form" action="./${order.uid}/tasks/plan_all" method="get">
        %for hidden_name, hidden_value in hidden.iteritems():
        <input type="hidden" name="${hidden_name}" value="${hidden_value}">
        %endfor
        <p style="margin-bottom: .3em;">Liste des tâches à planifier&#160;:</p>
        <table>
            %for task in order.order_phase_list:
            <%
            can_plan = task.plan_status_info['can_plan']
            style = "" if can_plan else "color: grey;"
            %>
            <tr style="${style}">
                <td>
                    %if task.plan_status_info['can_plan']:
                    <span class="ui-icon ui-icon-circle-check"></span>
                    %else:
                    <span class="ui-icon ui-icon-triangle-1-e"></span>
                    %endif
                </td>
                <td><b>${task.label}&#160;:</b></td>
                <td>${task.plan_status_info['label']}</td>
                <td><span class="ui-icon ui-icon-help"></span>
                    <p class="ui-tooltip" hidden="hidden"><span class="ui-tooltip-content">${task.plan_status_info['description']}</span></p>
                </td>
            </tr>
            %endfor
        </table>
    </form>
    <script type="application/javascript" defer="defer">
    $(function() {
        $("#plan_section").tooltip({
            track: true,
            items: ".ui-icon-help",
            show: {
                delay: 500
            },
            content: function () {
                var element = $(this).parent();
                if (element.is("h3")) {
                    return element.next(".ui-tooltip").html();
                } else if (element.is("p")) {
                    return element.next(".ui-tooltip").html();
                } else if (element.is("td")) {
                    return element.find(".ui-tooltip").html();
                } else {
                    return element.attr("title");
                }
            },
            tooltipClass: "info"
        });

        var today = new Date();
        var tz_offset = today.getTimezoneOffset();
        $('#plan_all_form').find('input[name=tz_offset]').val(tz_offset);
    });
    </script>
</section>
