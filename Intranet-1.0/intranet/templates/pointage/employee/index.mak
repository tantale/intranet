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
			<form id="employee_get_all" class="minimal_form employee_get_all"
				action="${tg.url('./get_all/')}" method="get">
                <p>
                    <input id="employee_get_all__keyword" type="search" name="keyword"
                           value="${keyword}"
                           placeholder="Mot-clef"
                           title="Saisir un mot-clef"/>
                    <input type="hidden" name="uid" value="${uid}"/>
                    <button id="employee_get_all__search" type="submit" class="search_button"
                            title="Rechercher selon le mot-clef">Rechercher
                    </button>
                </p>
            </form>
		</div>\
		<form id="employee_new" class="minimal_form alignCenter employee_new"
			action="${tg.url('./new')}" method="get">
			<p>
				<button id="employee_new__new" type="submit" class="new_button"
					title="Ajouter un employé">Nouvel employé</button>
			</p>
		</form>
		<div id="accordion_content"></div>
	</div>
	<div id="rightFrame" class="ui-layout-center">
		<div id="employee_content">
            <%include file="local:templates.pointage.employee.employee_help"/>
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
<script type='text/javascript' src="${tg.url('/javascript/jquery.ui.datepicker-fr.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/imgLiquid-min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.layout-latest.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.form.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.employee.js')}"></script>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
		$('.employee_get_all').ajaxForm({
			target: '#accordion_content',
			success: on_accordion_refresh
		});
		$('.employee_new').ajaxForm({
			target: '#employee_content',
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
		$('#employee_get_all').submit();
	});
</script>
</body>
</html>
