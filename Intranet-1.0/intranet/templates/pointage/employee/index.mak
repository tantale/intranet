# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.employee.index
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="${response.charset}" />
<title>Gestion des employés</title>
<meta name="description" content="Gestion des employés pour l'intranet de pointage" />
<link rel="icon" type="image/ico" href="${tg.url('/favicon.ico')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/blitzer/jquery-ui-1.10.3.custom.min.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/layout-default-latest.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.pointage.css')}" />
<script type='text/javascript' src="${tg.url('/javascript/jquery-1.9.1.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery-ui-1.10.3.custom.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.ui.datepicker-fr.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/modernizr.custom.32767.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/imgLiquid-min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.layout-latest.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.form.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.employee.js')}"></script>
<script type='text/javascript'>
	$(function() {
		$('#search_form').ajaxForm({
			target: '#accordion_content',
			success: on_accordion_refresh
		});
		$('#employee_new').ajaxForm({
			target: '#employee_content',
			beforeSubmit: function(arr, $form, options) {
				$('#flash').hide();
			}
		});
		$('#employee_get_all').ajaxForm({
			target: '#accordion_content',
			success: on_accordion_refresh
		});
		refresh_accordion();
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
			<form id="search_form" class="minimal_form"
				action="${tg.url('/pointage/employee/search')}" method="get">
				<p>
					<input id="search_form__keyword" type="search" name="keyword"
						placeholder="Mot-clef"
						title="Saisir un mot-clef" />
					<button id="search_form__search" type="submit" class="search_button"
						title="Rechercher selon le mot-clef">Rechercher</button>
				</p>
			</form>
		</div>\
		<form id="employee_get_all" class="inline_form alignCenter"
			action="${tg.url('/pointage/employee/get_all/')}" method="get">
			<p>
				<button id="employee_get_all__refresh" type="submit" class="refresh_button"
					title="Mettre à jour la liste des employés">Mettre à jour</button>
			</p>
		</form>
		<form id="employee_new" class="inline_form alignCenter"
			action="${tg.url('/pointage/employee/new')}" method="get">
			<p>
				<button id="employee_new__new" type="submit" class="new_button"
					title="Ajouter un employé">Nouvel employé</button>
			</p>
		</form>
		<div id="accordion_content">
		</div>
	</div>
	<div id="rightFrame" class="ui-layout-center">
		<div id="employee_content"/>
	</div>
</body>
</html>
