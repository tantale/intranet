# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.order.get_delete
:date: 2013-08-28
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%! import json %>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if order is None:
%if flash:
	${flash | n}
%endif

<% confirm_dialog_title_json = json.dumps(u"Commande supprimée") %>

<script type='text/javascript'>
	"use strict";
	/*global $*/
	$("#confirm_dialog").dialog({
		width: 400,
		height: 200,
		buttons: {
			Ok: function() {
				$(this).dialog("close");
			}
		},
		title: ${confirm_dialog_title_json|n},
		close: function() {
			$("#order_content").empty();
		}
	}).dialog("open");
</script>

%else:

<form id="order_post_delete" class="ui-widget"
	action="${tg.url('/pointage/order/{uid}'.format(uid=order.uid))}"
	method="post">
	<% order_phase_count = len(order.order_phase_list) %>
	%if order_phase_count == 0:
		<p>Cette commande ne comporte aucune phase (ni aucun pointage).</p>
	%elif order_phase_count == 1:
		<p>Cette commande comporte 1 phase qui sera supprimée.</p>
		<p><strong>NB :</strong> tous les pointages associées à cette commande seront supprimés.</p>
	%else:
		<p>Cette commande comporte ${order_phase_count} phase(s) qui seront supprimées.</p>
		<p><strong>NB :</strong> tous les pointages associées à cette commande seront supprimés.</p>
	%endif
	<input type="hidden" name="_method" value="DELETE" />
</form>

<%
uid_json = json.dumps(order.uid)
confirm_dialog_title_fmt = u"Voulez-vous supprimer la commande {order_ref} ?"
confirm_dialog_title = confirm_dialog_title_fmt.format(order_ref=order.order_ref)
confirm_dialog_title_json = json.dumps(confirm_dialog_title)
%>

<script type='text/javascript'>
	"use strict";
	/*global $*/
	$("#confirm_dialog").dialog({
		width: 500,
		height: 200,
		buttons: {
			"Supprimer": function() {
				$('#order_post_delete').submit();
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
	$('#order_post_delete').ajaxForm({
		target : '#confirm_dialog_content',
		success: function(responseText, statusText, xhr) {
			console.log("search for '<div id=\"flash\"><div class=\"ok\">' tag...");
			var ok = $('<div/>').append(responseText).find('#flash div.ok');
			if (ok.length) {
				var input = $("#order_get_all input[name=uid]");
				console.log("OK, update the order list but don't select any order...");
				input.val("");
				$("#order_get_all").submit();
			} else {
				console.log("ERROR: don't update the order list.");
			}
		}
	});
</script>
%endif
