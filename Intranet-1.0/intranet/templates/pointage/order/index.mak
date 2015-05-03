<%inherit file="local:templates.pointage.master"/>

<%def name="title()">${_(u"Gestion des commandes")}</%def>

<%def name="search_frame()">
<form id="order_get_all" class="minimal_form order_get_all"
    action="${tg.url('./get_all/')}" method="get">
    <p>
        <input id="order_get_all__uid" type="number" name="uid"
                value="${uid}"
                placeholder="N° commande"
                title="${_(u'Numéro de la commande recherchée')}"/><br/>
        <input id="order_get_all__keyword" type="search" name="keyword"
                value="${keyword}"
                placeholder="Mot-clef"
                title="${_(u'Saisir un mot-clef')}"/>
        <input type="hidden" name="order_ref" value="" />
        <button id="order_get_all__search" type="submit" class="search_button"
            title="${_(u'Rechercher selon le mot-clef')}">${_(u"Rechercher")}</button>
    </p>
</form>
</%def>

<%def name="new_frame()">
<form id="order_new" class="minimal_form alignCenter order_new"
    action="${tg.url('./new')}" method="get">
    <p>
        <button id="order_new__new" type="submit" class="new_button"
            title="${_(u'Ajouter une nouvelle commande.')}">${_(u"Nouvelle commande")}</button>
    </p>
</form>
</%def>

<%def name="accordion_content()">
</%def>

<%def name="content_frame()">
<div id="order_content">
    <%include file="local:templates.pointage.order.order_help"/>
</div>
</%def>

<%def name="extra_scripts()">
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.order.js')}"></script>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
		$.fn.editable.defaults.mode = 'inline';
		$('.order_get_all').ajaxForm({
			target: '#accordion_content',
			success: on_accordion_refresh
		});
		$('.order_new').ajaxForm({
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
</%def>
