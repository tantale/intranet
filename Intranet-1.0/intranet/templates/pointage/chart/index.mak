<%inherit file="local:templates.pointage.master"/>

<%def name="title()">${_(u"Statistiques des pointages")}</%def>

<%def name="search_frame()">
</%def>

<%def name="new_frame()">
</%def>

<%def name="accordion_content()">
<form id="search_get_all" class="minimal_form"
      action="${tg.url('./get_all/')}" method="get">

    <div id="accordion">
        <h2>${_(u"Sélection")}</h2>

        <div>
            <p>
                <label for="search_get_all__uid">${_(u'N° commande :')}</label>
                <input id="search_get_all__uid"
                       type="search" name="uid"
                       title="${_(u'Numéro de la commande')}"/>
            </p>

            <p>
                <label for="search_get_all__order_ref">${_(u'Ref. commande :')}</label>
                <input id="search_get_all__order_ref"
                       type="search" name="order_ref"
                       title="${_(u'Référence de la commande')}"/>
            </p>

            <p>
                <label for="search_get_all__project_cat">${_(u'Catégorie de projet :')}</label>
                <input id="search_get_all__project_cat"
                       type="search" name="project_cat"
                       title="${_(u'Catégorie de projet de la commande')}"/>
            </p>
        </div>
        <h2>${_(u"Intervalle de dates")}</h2>

        <div>
            <p>
                <label for="search_get_all__start_date">${_(u'Date de début :')}</label>
                <input id="search_get_all__start_date" type="date" name="start_date"
                       title="${_(u'Date de début de recherche')}"/>
            </p>

            <p><label for="search_get_all__end_date">${_(u'Date de fin :')}</label>
                <input id="search_get_all__end_date" type="date" name="end_date"
                       title="${_(u'Date de fin de recherche')}"/>
            </p>

            <p><label for="search_get_all__closed">${_(u'Statut :')}</label>
                <select id="search_get_all__closed" name="closed"
                        title="${_(u'Statut de la commande (clôturée ou non)')}">
                    <option value="">${_(u'Indifférent')}</option>
                    <option value="true">${_(u'Clôturée')}</option>
                    <option value="false">${_(u'Non clôturée')}</option>
                </select>
            </p>
        </div>
    </div>

    <button id="search_get_all__search" type="submit" class="search_button"
            title="${_(u'Rechercher / filtrer selon les critères')}">${_(u"Rechercher")}</button>
</form>
</%def>

<%def name="content_frame()">
<div id="chart_content">
</div>
</%def>

<%def name="extra_scripts()">
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
		$('#accordion').accordion({
			collapsible: false,
			heightStyle: "content"
		});
		$('#search_get_all').ajaxForm({
			target: '#chart_content'
		});
		$('#confirm_dialog').dialog({
			autoOpen: false,
			width: 400,
			height: 200,
			modal: true
		});
	});
</script>
</%def>
