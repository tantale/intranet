<%inherit file="local:templates.pointage.master"/>

<%def name="title()">${_(u"Gestion des employés")}</%def>

<%def name="search_frame()">
<form id="employee_get_all" class="minimal_form employee_get_all"
    action="${tg.url('./get_all/')}" method="get">
    <p>
        <input id="employee_get_all__keyword" type="search" name="keyword"
               value="${keyword}"
               placeholder="Mot-clef"
               title="${_(u'Saisir un mot-clef')}"/>
        <input type="hidden" name="uid" value="${uid}"/>
        <button id="employee_get_all__search" type="submit" class="search_button"
                title="${_(u'Rechercher selon le mot-clef')}">${_(u"Rechercher")}</button>
    </p>
</form>
</%def>

<%def name="new_frame()">
<form id="employee_new" class="minimal_form alignCenter employee_new"
    action="${tg.url('./new')}" method="get">
    <p>
        <button id="employee_new__new" type="submit" class="new_button"
            title="${_(u'Ajouter un nouvel employé.')}">${_(u"Nouvel employé")}</button>
    </p>
</form>
</%def>

<%def name="accordion_content()">
</%def>

<%def name="content_frame()">
<div id="employee_content">
    <%include file="local:templates.pointage.employee.employee_help"/>
</div>
</%def>

<%def name="extra_scripts()">
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.employee.js')}"></script>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
        jQuery.get("./layout.json", function(data){
            $('body').layout($.extend(data, {
                west__onresize : function(name, element, state, options, layout_name) {
                    jQuery.ajax("./layout", {method: "put", data: {west__size: state.size}});
                }}));
        });
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
</%def>
