<%inherit file="local:templates.pointage.master"/>

<%def name="title()">${_(u"Préférences utilisateur")}</%def>

<%def name="search_frame()">
</%def>

<%def name="new_frame()">
</%def>

<%def name="accordion_content()">
<div id="accordion">
    <h2>${_(u"Catégories de commandes")}</h2>
    <div>
        <ul class="menu">
            <li><a href="${tg.url('/admin/order_cat/index.html?display=detail')}"
                   title="${_(u'Liste complète des catégories de commandes')}"><span
                    class="ui-button-icon-primary ui-icon ui-icon-document-b"></span>${_(u"Tableau des catégories")}</a>
            </li>
            <li><a href="${tg.url('/admin/order_cat/get_orphans?display=detail')}"
                   title="${_(u'Affiche la liste des commandes sans catégorie')}"><span
                    class="ui-button-icon-primary ui-icon ui-icon-alert"></span>${_(u"Commandes sans catégorie")}</a>
            </li>
            <li><a href="${tg.url('/admin/order_cat.css?display=html')}"
                   title="${_(u'Affichage de la feuille de styles CSS des catégories de commandes')}"><span
                    class="ui-button-icon-primary ui-icon ui-icon-script"></span>${_(u"Feuille de styles CSS")}</a>
            </li>
        </ul>
    </div>
</div>
</%def>

<%def name="content_frame()">
<div id="prefs_content">
    <%include file="local:templates.pointage.prefs.prefs_help"/>
</div>
</%def>

<%def name="extra_scripts()">
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.prefs.js')}"></script>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
		$(".menu").menu();
		$(".menu a").click(function(event){
			event.preventDefault();
		    $("#prefs_content").load($(this).attr("href"));
		    return false;
		});
		$('#accordion').accordion({
			collapsible: false,
			heightStyle: "content"
		});
		$('#confirm_dialog').dialog({
			autoOpen: false,
			width: 400,
			height: 200,
			modal: true
		});
        $("#help-section-01 a.button").button({icons: {primary: "ui-icon-document-b"}});
        $("#help-section-02 a.button").button({icons: {primary: "ui-icon-alert"}});
        $("#help-section-03 a.button").button({icons: {primary: "ui-icon-script"}});
		$("#help-article a.button").click(function(event){
			event.preventDefault();
		    $("#prefs_content").load($(this).attr("href"));
		    return false;
		});
	});
</script>
</%def>
