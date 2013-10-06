# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.trcal.get_delete
:date: 2013-08-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%! import json %>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if cal_event is None:
%if flash:
	${flash | n}
%endif

<% confirm_dialog_title_json = json.dumps(u"Commande supprimée") %>

<script type='text/javascript'>
	"use strict";
	/*global $*/
	$('#confirm_dialog').dialog({
		width: 400,
		height: 200,
		buttons: {
			Ok: function() {
				$(this).dialog("close");
			}
		},
		title: ${confirm_dialog_title_json|n},
		close: function() {
			console.log("empty #calendar_content...");
			$('#calendar_content').empty();
		}
	}).dialog("open");
</script>

%else:

<form id="cal_event_post_delete" class="ui-widget"
	action="${tg.url('/pointage/trcal/{uid}'.format(uid=cal_event.uid))}"
	method="post">
	<% cal_event_phase_count = len(cal_event.cal_event_phase_list) %>
	%if cal_event_phase_count == 0:
		<p>Cette commande ne comporte aucune phase (ni aucun pointage).</p>
	%elif cal_event_phase_count == 1:
		<p>Cette commande comporte 1 phase qui sera supprimée.</p>
		<p><strong>NB :</strong> tous les pointages associées à cette commande seront supprimés.</p>
	%else:
		<p>Cette commande comporte ${cal_event_phase_count} phase(s) qui seront supprimées.</p>
		<p><strong>NB :</strong> tous les pointages associées à cette commande seront supprimés.</p>
	%endif
	<input type="hidden" name="_method" value="DELETE" />
</form>

<%
uid_json = json.dumps(cal_event.uid)
confirm_dialog_title_fmt = u"Voulez-vous supprimer la commande {title} ?"
confirm_dialog_title = confirm_dialog_title_fmt.format(title=cal_event.title)
confirm_dialog_title_json = json.dumps(confirm_dialog_title)
%>

<script type='text/javascript'>
	"use strict";
	/*global $*/
	$('#confirm_dialog').dialog({
		width: 500,
		height: 200,
		buttons: {
			"Supprimer": function() {
				$('#cal_event_post_delete').submit();
				$(this).dialog("close");
			},
			"Annuler": function() {
				$(this).dialog("close");
			}
		},
		title: ${confirm_dialog_title_json|n},
		close: function() {
		}
	}).dialog("open");
	$('#cal_event_post_delete').ajaxForm({
		target : '#confirm_dialog_content',
		success: function(responseText, statusText, xhr) {
			console.log("search for '<div id=\"flash\"><div class=\"ok\">' tag...");
			var ok = $('<div/>').append(responseText).find('#flash div.ok');
			if (ok.length) {
				var input = $('#cal_event_get_all input[name=uid]');
				console.log("OK, update the cal_event list but don't select any cal_event...");
				input.val("");
				$('#cal_event_get_all').submit();
			} else {
				console.log("ERROR: don't update the cal_event list.");
			}
		}
	});
</script>
%endif
