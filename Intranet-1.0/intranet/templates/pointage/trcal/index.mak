# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.trcal.index
:date: 2013-09-22
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="${response.charset}" />
<title>Calendrier des pointages</title>
<meta name="description" content="Gestion des commandes pour l'intranet de pointage" />
<link rel="icon" type="image/ico" href="${tg.url('/favicon.ico')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/blitzer/jquery-ui-1.10.3.custom.min.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/layout-default-latest.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/jqueryui-editable.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/fullcalendar.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.pointage.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('../order_cat.css')}" />
<script type='text/javascript' src="${tg.url('/javascript/jquery-1.9.1.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery-ui-1.10.3.custom.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/modernizr.custom.32767.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.layout-latest.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.form.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/fullcalendar.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.trcal.js')}"></script>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
		$('#order_get_all').ajaxForm({
			target: '#accordion_content',
			success: on_accordion_refresh
		});
		$('#confirm_dialog').dialog({
			autoOpen: false,
			width: 400,
			height: 200,
			modal: true
		});
		$('#order_get_all').submit();
		// TODO: add cal_date parameter
		$('#calendar_content').load("./");
	});
</script>
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
				action="${tg.url('./order_get_all/')}" method="get">
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
		<div id="accordion_content"></div>
	</div>
	<div id="rightFrame" class="ui-layout-center">
		<div id="calendar_content"></div>
	</div>
	<div id="confirm_dialog" title="Confirmation">
		<div id="confirm_dialog_content"></div>
	</div>
</body>
</html>
