# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head profile="http://www.w3.org/2005/10/profile">
${self.meta()}\
<title>${self.title()}</title>
<link rel="icon" type="image/ico" href="${tg.url('/favicon.ico')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/blitzer/jquery-ui-1.10.3.custom.min.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/layout-default-latest.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.css')}" />
<link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.pointage.css')}" />
${self.extra_css()}\
<script type='text/javascript' src="${tg.url('/javascript/jquery-1.9.1.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery-ui-1.10.3.custom.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/modernizr.custom.32767.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/imgLiquid-min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery.layout-latest.min.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.js')}"></script>
${self.extra_script()}\
</head>
<body>
	<div id="topFrame" class="ui-layout-north">
		${self.toolbar()}
	</div>
	<div id="leftFrame" class="ui-layout-west">
		${self.search_frame()}
		${self.add_button()}
		<div id="accordion">
			${self.accordion()}
		</div>
	</div>
	<div id="rightFrame" class="ui-layout-center">
	<%flash = tg.flash_obj.render('flash', use_js=False)%>
	%if flash:
		<div class="row"><div class="span8 offset2">
		${flash | n}
		</div></div>
	%endif
	${self.body()}
	</div>
</body>
</html>

<%def name="meta()">\
<meta charset="${response.charset}" />\
</%def>

<%def name="extra_css()"></%def>

<%def name="extra_script()"></%def>

<%def name="toolbar()">\
<div id="toolbar" class="ui-widget-header">
	<h1>Gestion des pointages</h1>
	<a id="toolbar_employee" href="../employee">Employés</a>
	<a id="toolbar_command"  href="../command">Commandes</a>
	<a id="toolbar_calendar" href="../calendar">Calendrier</a>
</div>\
</%def>

<%def name="search_frame()">\
<div id="searchFrame">
	<form id="search_form" action="#">
		<p>
			<input id="search_form__name" type="search" name="name" />
			<button id="search_form__search" type="submit">Rechercher</button>
		</p>
	</form>
</div>\
</%def>

<%def name="add_button()"></%def>

<%def name="accordion()"></%def>
