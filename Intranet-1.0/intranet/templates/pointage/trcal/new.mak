# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.trcal.new
:date: 2013-09-22
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if flash:
	${flash | n}
%endif
<form id="cal_event_create" class="ui-widget"
	action="${tg.url('/pointage/trcal/')}"
	method="post" enctype="multipart/form-data">
##
## Hidden fields for the relationships: employee_uid, order_phase_uid (required)
## and Time zone offset (for UTC date/time calculation)
##
	<p style="display: none; visibility: hidden;">
	<input name="employee_uid" type="hidden" value="${employee.uid}" />
	<input name="order_phase_uid" type="hidden" value="${order_phase.uid}" />
	<input name="time_zone_offset" type="hidden" value="${time_zone_offset}" />
	</p>
##
## Referenced objects: employee, order, order phase (with project_cat's css)
##
	<p><label for="cal_event_create__employee_name">Nom :</label>
		<input id="cal_event_create__employee_name" type="text"
			value="${employee.employee_name}"
			disabled="disabled"
			title="Pointage pour l’employé : ${employee.employee_name}" /></p>
	
	<p><label for="cal_event_create__order_ref">Réf. commande :</label>
		<input id="cal_event_create__order_ref" type="text"
			value="${order_phase.order.order_ref}"
			disabled="disabled"
			title="Pointage pour la commande : ${order_phase.order.order_ref}" /></p>
	
	<p><label for="cal_event_create__order_phase_label">Phase :</label>
		<input id="cal_event_create__order_phase_label" type="text"
			class="${order_phase.order.project_cat}"
			value="${order_phase.label}"
			disabled="disabled"
			title="Pointage pour la phase : ${order_phase.label}" /></p>
##
## Calendar event fields: title, event_start, event_duration, comment
##
	<p><label for="cal_event_create__title">Titre :</label>
		<input id="cal_event_create__title" type="text" name="title"
			size="50"
			value="${values.get('title')}"
			placeholder="Titre"
			title="Titre du pointage" />
	%if 'title' in form_errors:
	<span class="error">${form_errors['title']}</span>
	%endif
	</p>

	<p><label for="cal_event_create__event_start">Date / Heure :</label>
		<input id="cal_event_create__event_start" type="datetime-local" name="event_start"
			value="${values.get('event_start')}"
			title="Date (et heure) du pointage (requis)" />
	%if 'event_start' in form_errors:
	<span class="error">${form_errors['event_start']}</span>
	%endif
	</p>

	<p><label for="cal_event_create__event_duration">Durée (h/100) :</label>
		<input id="cal_event_create__event_duration" type="number" name="event_duration"
			min="1" max="999"
			value="${values.get('event_duration')}"
			placeholder="100"
			title="Durée en centième d'heure, ex. : 100 pour 1 heure (requis)" />
	%if 'event_duration' in form_errors:
	<span class="error">${form_errors['event_duration']}</span>
	%endif
	</p>
	
	<p><label for="cal_event_create__comment">Commentaire :</label>
		<textarea id="cal_event_create__comment" name="comment"
			rows="4" cols="50"
			placeholder="Commentaire (facultatif)"
			title="Commentaire (optionnel)">${values.get('comment')}</textarea>
	%if 'comment' in form_errors:
	<span class="error">${form_errors['comment']}</span>
	%endif
	</p>

	<!-- <p><button id="cal_event_create__create" type="submit" class="create_button"
		title="Saisir les informations concernant un pointage">Créer</button></p> -->
</form>
<script type='text/javascript'>
	"use strict";
	/*global $, Modernizr*/
	function time_zone_offset() {
		var date = new Date();
		return date.getTimezoneOffset();
	}
	if (!Modernizr.inputtypes.date) {
		$('#cal_event_create input[type=date]').datepicker();
	}
	$('#cal_event_create input[name=time_zone_offset]').val(time_zone_offset());
	$('#cal_event_create input[name=event_duration]').focus();
	$('#cal_event_create .create_button').button({
		text : true,
		icons : {
			primary : "ui-icon-check"
		}
	});
	$('#cal_event_create').ajaxForm({
		target : '#confirm_dialog_content',
		beforeSubmit: function(arr, $form, options) {
			$('#flash').hide();
		},
		success: function(responseText, statusText, xhr) {
			console.log("search for '<div id=\"flash\"><div class=\"ok\">' tag...");
			var ok = $('<div/>').append(responseText).find('#flash div.ok');
			if (ok.length) {
				console.log("OK, update the cal_event list but don't select any cal_event...");
				$('#calendar').fullCalendar('renderEvent', jQuery.parseJSON(responseText));
			} else {
				console.log("ERROR: don't update the cal_event list.");
			}
		}
	});
</script>