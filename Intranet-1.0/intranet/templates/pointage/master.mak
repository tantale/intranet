<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="${response.charset}"/>
    <title>${self.title()}</title>
    <meta name="description" content="Gestion des commandes pour l'intranet de pointage"/>
    <link rel="icon" type="image/ico" href="${tg.url('/favicon.ico')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/blitzer/jquery-ui-1.10.3.custom.min.css')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/layout-default-latest.css')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/jqueryui-editable.css')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/fullcalendar.css')}" />
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.css')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.pointage.css')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('../order_cat.css')}"/>
</head>
<body>
<div id="topFrame" class="ui-layout-north">
<nav id="toolbar" class="ui-widget-header">
    <h1 title="${main_menu.description}">${main_menu.display_name}</h1>
    %for item in main_menu.item_list:
    %if item.is_separator:
    <span>|</span>
    %else:
    <a id="toolbar_${item.uid}" href="${item.target_page}" title="${item.description}">${item.display_name}</a>
    %endif
    %endfor
</nav>
</div>
<div id="leftFrame" class="ui-layout-west">
<aside id="searchFrame">${self.search_frame()}</aside>
<aside id="newFrame">${self.new_frame()}</aside>
<aside id="accordion_content">${self.accordion_content()}</aside>
</div>
<div id="rightFrame" class="ui-layout-center">
<section id="contentFrame">${self.content_frame()}</section>
</div>
<div id="confirm_dialog" title="${_(u'Confirmation')}">
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
<script type='text/javascript' src="${tg.url('/javascript/imgLiquid-min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.layout-latest.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.form.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/fullcalendar.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.js')}"></script>
<script type='text/javascript'>
	"use strict";
	$(function() {
		$.fn.editable.defaults.mode = 'inline';
	});
    %for item in main_menu.item_list:
    %if not item.is_separator:
	$("#toolbar_${item.uid}").button({
		text : true,
		icons : {
			primary : "${item.icon_name}"
		}
	});
    %endif
    %endfor
</script>
${self.extra_scripts()}
</body>
</html>
