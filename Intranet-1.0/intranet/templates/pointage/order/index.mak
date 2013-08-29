# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.order.index
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="${response.charset}" />
<title>Gestion des commandes</title>
<meta name="description" content="Gestion des commandes pour l'intranet de pointage" />
<link rel="icon" type="image/ico" href="${tg.url('/favicon.ico')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/blitzer/jquery-ui-1.10.3.custom.min.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/layout-default-latest.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.pointage.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/pointage/order_cat.css')}" />
<script type='text/javascript' src="${tg.url('/javascript/jquery-1.9.1.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery-ui-1.10.3.custom.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.ui.datepicker-fr.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/modernizr.custom.32767.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.layout-latest.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.form.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.editinplace.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.order.js')}"></script>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
		$('#order_get_all').ajaxForm({
			target: '#accordion_content',
			success: on_accordion_refresh
		});
		$('#order_new').ajaxForm({
			target: '#order_content',
			success: function(responseText, statusText, xhr) {
				$("#accordion").accordion("option", "active", false);
			}
		});
		$('#confirm_dialog').dialog({
			autoOpen: false,
			width: 400,
			height: 200,
			modal: true
		});
		$("#order_get_all").submit();
	});
</script>
</head>
<body>
	<div id="topFrame" class="ui-layout-north">
		<div id="toolbar" class="ui-widget-header">
			<h1>Gestion des pointages</h1>
			<a id="toolbar_employee" href="${tg.url('/pointage/employee/index')}">Employés</a>
			<a id="toolbar_order" href="${tg.url('/pointage/order/index')}">Commandes</a>
			<a id="toolbar_calendar" href="${tg.url('/pointage/calendar/index')}">Calendrier</a>
		</div>\
	</div>
	<div id="leftFrame" class="ui-layout-west">
		<div id="searchFrame">
			<form id="order_get_all" class="minimal_form"
				action="${tg.url('/pointage/order/get_all/')}" method="get">
				<p>
					<input id="order_get_all__keyword" type="search" name="keyword"
						placeholder="Mot-clef"
						title="Saisir un mot-clef" />
					<input type="hidden" name="uid" value="" />
					<button id="order_get_all__search" type="submit" class="search_button"
						title="Rechercher selon le mot-clef">Rechercher</button>
				</p>
			</form>
		</div>\
		<form id="order_new" class="minimal_form alignCenter"
			action="${tg.url('/pointage/order/new')}" method="get">
			<p>
				<button id="order_new__new" type="submit" class="new_button"
					title="Ajouter une commande">Nouvelle commande</button>
			</p>
		</form>
		<div id="accordion_content">
		</div>
	</div>
	<div id="rightFrame" class="ui-layout-center">
		<div id="order_content"/>
	</div>
	<div id="confirm_dialog" title="Confirmation">
		<div id="confirm_dialog_content"/>
	</div>
</body>
</html>
