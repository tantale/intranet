# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.employee.get_delete
:date: 2013-09-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%! import json %>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if employee is None:
%if flash:
	${flash | n}
%endif

<% confirm_dialog_title_json = json.dumps(u"Employé supprimée") %>

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
			console.log("empty #employee_content...");
			$('#employee_content').empty();
		}
	}).dialog("open");
</script>

%else:

<form id="employee_post_delete" class="ui-widget"
	action="${tg.url('./{uid}'.format(uid=employee.uid))}"
	method="post">
	%if employee.cal_event_list:
	<p><strong>NB :</strong> les ${len(employee.cal_event_list)} pointages associées à cette employé seront supprimés.</p>
	%else:
	<p>Cet employé ne possède pas de pointage.</p>
	%endif
	<input type="hidden" name="_method" value="DELETE" />
</form>

<%
uid_json = json.dumps(employee.uid)
confirm_dialog_title_fmt = u"Voulez-vous supprimer l’employé {employee_name} ?"
confirm_dialog_title = confirm_dialog_title_fmt.format(employee_name=employee.employee_name)
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
				$('#employee_post_delete').submit();
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
	$('#employee_post_delete').ajaxForm({
		target : '#confirm_dialog_content',
		success: function(responseText, statusText, xhr) {
			console.log("search for '<div id=\"flash\"><div class=\"ok\">' tag...");
			var ok = $('<div/>').append(responseText).find('#flash div.ok');
			if (ok.length) {
				var input = $('#employee_get_all input[name=uid]');
				console.log("OK, update the employees list but don't select any employee...");
				input.val("");
				$('#employee_get_all').submit();
			} else {
				console.log("ERROR: don't update the employees list.");
			}
		}
	});
</script>
%endif
