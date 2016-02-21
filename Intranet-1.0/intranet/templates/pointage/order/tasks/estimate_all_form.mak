<%!
    def heures(text):
        return unicode(text).replace(".", ",")
%>
<section id="estimate_section">
    <style scoped="scoped" type="text/css">
        #estimate_section label b {
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
        <p class="ui-tooltip" hidden="hidden"><span class="ui-tooltip-content">Ce calcultateur permet d’estimer
            la durée des phases de production en analysant
            les heures déjà déjà pointées sur les commandes les plus récentes.
            L’analyse statistique est réalisée sur un échantillon représentatif
            sélectionné selon les paramètres ci-dessous (<mark>nombre de commandes</mark> et
            <mark>statut de la commande</mark>).
            Les estimations de durées sont calculée en excluant les cas extrêmes
            (très grosses / très petites commandes).
        </span></p>
    </header>
    <form id="estimate_all_form" action="./${order.uid}/tasks/estimate_all" method="get">
        %for hidden_name, hidden_value in hidden.iteritems():
        <input type="hidden" name="${hidden_name}" value="${hidden_value}">
        %endfor
        <p><label class="tooltip"><b>Nombre de commandes à analyser&nbsp;:</b>
            <input name="max_count" type="number" min="32" max="128" value="${max_count}"></label>
            <span class="ui-icon ui-icon-help"></span></p>
        <p class="ui-tooltip" hidden="hidden"><span class="ui-tooltip-content">Ce paramètre permet de definir la taille de l’échantillon
            pour les calculs statistiques. Plus l’échantillon est grand et plus le calcul sera précis.
            Cependant, le temps de calcul peut s’avérer plus long avec un grand nombre de commandes.</span></p>
        %if 'max_count'in form_errors:
        <p><span class="error">${form_errors['max_count']}</span></p>
        %endif

        <p><label class="tooltip"><b>Statut des commandes&nbsp;:</b>
            <%
            closed_mapping = {None: dict(value="", selected=False, label=u"Indifférent"),
            True: dict(value="true", selected=False, label=u"Clôturée"),
            False: dict(value="false", selected=False, label=u"Non clôturée")}
            closed_mapping[closed]["selected"] = True
            %>
            <select name="closed">
                %for option in closed_mapping.itervalues():
                %if option["selected"]:
                <option value="${option['value']}" selected="selected">${option['label']}</option>
                %else:
                <option value="${option['value']}">${option['label']}</option>
                %endif
                %endfor
            </select></label>
            <span class="ui-icon ui-icon-help"></span></p>
        <p class="ui-tooltip" hidden="hidden"><span class="ui-tooltip-content">L’estimation sera plus pertinente si l’on sélectionne
            <mark>Clôturée</mark>, mais on peut aussi sélectionner <mark>Indifférent</mark>
            pour analyser l’intégralité des commandes&nbsp;;
            Si l’on sélectionne <mark>Non clôturée</mark>, on analysera les commandes en cours de pointage,
            la mesure sera moins pertinente, car certaines phases ne seront pas terminées.</span></p>
        %if 'closed'in form_errors:
        <p><span class="error">${form_errors['closed']}</span></p>
        %endif
    </form>
    <div>
        %if order.estimated_duration:
        <p class="ui-state-highlight">Cette commande est estimées à ${order.estimated_duration|heures}&#160;heures.
            Voulez-vous vraiment recalculer la durée de toutes les tâches&#160;?</p>
        %endif
    </div>
    <script type="application/javascript" defer="defer">
    $(function() {
        $("#estimate_section").tooltip({
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
                } else {
                    return element.attr("title");
                }
            },
            tooltipClass: "info"
        });

        var today = new Date();
        var tz_offset = today.getTimezoneOffset();
        $('#estimate_all_form').find('input[name=tz_offset]').val(tz_offset);
    });
    </script>
</section>
