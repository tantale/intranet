<%inherit file="local:templates.pointage.master"/>

<%def name="title()">${_(u"Calendrier des pointages")}</%def>

<%def name="search_frame()">
<form id="order_get_all" class="minimal_form"
    action="${tg.url('./order_get_all/')}" method="get">
    <p>
        <input id="order_get_all__uid" type="number" name="uid"
                value=""
                placeholder="N° commande"
                title="Numéro de la commande recherchée" /><br>
        <input id="order_get_all__keyword" type="search" name="keyword"
            placeholder="Mot-clef"
            title="Saisir un mot-clef" />
        <input type="hidden" name="cal_start" value="" />
        <input type="hidden" name="cal_end" value="" />
        <button id="order_get_all__search" type="submit" class="search_button"
            title="Rechercher selon le mot-clef">Rechercher</button>
    </p>
</form>
</%def>

<%def name="new_frame()">
</%def>

<%def name="accordion_content()">
</%def>

<%def name="content_frame()">
<div id="calendar_content"></div>
</%def>

<%def name="extra_scripts()">
<script type='text/javascript' src="${tg.url('/javascript/intranet.pointage.trcal.js')}"></script>
<script type='text/javascript'>
	"use strict";
	/*global $*/

	function load_calendar_content(cal_start, cal_end) {
		if (!cal_start || !cal_end) {
			var cal_curr = new Date(), y = cal_curr.getFullYear(), m = cal_curr.getMonth();
			cal_start = new Date(y, m, 1);
			cal_end = new Date(y, m + 1, 1);
		}
		$('#calendar_content').load("./get_all", {
			'cal_start': cal_start.getTime() / 1000,
			'cal_end': cal_end.getTime() / 1000,
			'cal_curr': Math.round(cal_curr.getTime() / 1000)
			});
	}

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
		load_calendar_content();
	});
</script>
</%def>
