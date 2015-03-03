# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="${response.charset}" />
<title>${_(u"Préférences utilisateur")}</title>
<meta name="description" content="Gestion des commandes pour l'intranet de pointage" />
<link rel="icon" type="image/ico" href="${tg.url('/favicon.ico')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/blitzer/jquery-ui-1.10.3.custom.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/layout-default-latest.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/jqueryui-editable.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.pointage.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('../order_cat.css')}" />
<style>
.ui-menu {
	xxwidth: 200px;
}
</style>
</head>
<body>
	<div id="topFrame" class="ui-layout-north">
		<div id="toolbar" class="ui-widget-header">
			<h1>${main_menu['title']}</h1>
			%for item in main_menu['item_list']:
			<a id="${item['id']}" href="${item['href']}" title="${item['title']}">${item['content']}</a>
			%endfor
		</div>\
	</div>
	<div id="leftFrame" class="ui-layout-west">
		<div id="accordion_content">
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
			</div><!-- /#accordion -->
		</div>
	</div>
	<div id="rightFrame" class="ui-layout-center">
		<div id="prefs_content">
            <%include file="local:templates.pointage.prefs.prefs_help"/>
        </div>
    </div>
	<div id="confirm_dialog" title="Confirmation">
		<div id="confirm_dialog_content"></div>
	</div>
##
## text/javascript
##
<script type='text/javascript' src="${tg.url('/javascript/jquery-1.9.1.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery-ui-1.10.3.custom.min.js')}"></script>
<script type='text/javascript' src="https://www.google.com/jsapi"></script>
<script type='text/javascript' src="${tg.url('/javascript/jqueryui-editable.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.ui.datepicker-fr.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.layout-latest.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.form.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.prefs.js')}"></script>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
		$.fn.editable.defaults.mode = 'inline';
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
</body>
</html>
