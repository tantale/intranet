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
<link rel="stylesheet" type="text/css" href="${tg.url('/css/jqueryui-editable.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.pointage.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('../order_cat.css')}" />
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
		<div id="searchFrame">
			<form id="order_get_all" class="minimal_form"
				action="${tg.url('./get_all/')}" method="get">
				<p>
					<input id="order_get_all__keyword" type="search" name="keyword"
						placeholder="Mot-clef"
						title="Saisir un mot-clef" />
					<input type="hidden" name="uid" value="" />
					<input type="hidden" name="order_ref" value="" />
					<button id="order_get_all__search" type="submit" class="search_button"
						title="Rechercher selon le mot-clef">Rechercher</button>
				</p>
			</form>
		</div>\
		<form id="order_new" class="minimal_form alignCenter"
			action="${tg.url('./new')}" method="get">
			<p>
				<button id="order_new__new" type="submit" class="new_button"
					title="Ajouter une commande">Nouvelle commande</button>
			</p>
		</form>
		<div id="accordion_content"></div>
	</div>
	<div id="rightFrame" class="ui-layout-center">
		<div id="order_content">
			<br />
			<br />
			<br />
			<h1>← Veuillez sélectionner une commande dans la liste ci-contre.</h1>
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
<script type='text/javascript' src="${tg.url('/javascript/modernizr.custom.32767.js')}"></script>
<script type='text/javascript' src="https://www.google.com/jsapi"></script>
<script type='text/javascript' src="${tg.url('/javascript/jqueryui-editable.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.ui.datepicker-fr.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.layout-latest.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.form.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.order.js')}"></script>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
		$.fn.editable.defaults.mode = 'inline';
		$('#order_get_all').ajaxForm({
			target: '#accordion_content',
			success: on_accordion_refresh
		});
		$('#order_new').ajaxForm({
			target: '#order_content',
			beforeSubmit: function(arr, form, options) {
				console.log("hide #flash...");
				$('#flash').hide();
				console.log("deactivate #accordion...");
				$('#accordion').accordion("option", "active", false);
			}
		});
		$('#confirm_dialog').dialog({
			autoOpen: false,
			width: 400,
			height: 200,
			modal: true
		});
		$('#order_get_all').submit();
	});
</script>
</body>
</html>
