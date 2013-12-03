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
	action="${tg.url('./')}"
	method="post" enctype="multipart/form-data">
##
## Hidden fields for the relationships: employee_uid, order_phase_uid (required)
## and Time zone offset (for UTC date/time calculation)
##
	<p style="display: none; visibility: hidden;">
	<input name="employee_uid" type="hidden" value="${employee.uid}" />
	<input name="order_phase_uid" type="hidden" value="${order_phase.uid}" />
	<input name="tz_offset" type="hidden" value="${tz_offset}" />
	</p>
##
## Referenced objects: order, order phase (with project_cat's css)
##
	<p class="colorFrame ${order_phase.order.project_cat}"><span
	title="Pointage pour la commande : ${order_phase.order.order_ref}">${order_phase.order.order_ref}</span><span> : </span><span
	title="Pointage pour la phase : ${order_phase.label}">${order_phase.label}</span></p>
	
##
## Calendar event fields: event_start, event_duration, comment
##
	<p><label for="cal_event_create__event_start">Date / Heure :</label>
		<input id="cal_event_create__event_start" type="datetime-local" name="event_start"
			value="${values.get('event_start')}"
			title="Date (et heure) du pointage (requis)" />
	%if 'event_start' in form_errors:
	<span class="error">${form_errors['event_start']}</span>
	%endif
	</p>

	<p><label for="cal_event_create__event_duration">Durée (h) :</label>
		<input id="cal_event_create__event_duration" type="number" name="event_duration"
			min="0.25" max="12" step="0.25"
			value="${values.get('event_duration')}"
			placeholder="1"
			title="Durée en heure, ex. : 1,50 pour 1h30 (requis)" />
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
	
</form>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$('#cal_event_create input[name=event_duration]').focus()
		.change(function(event) {
			if (event.target.validity.valid) {
				$(this).removeClass('error');
			} else {
				$(this).addClass('error');
			}
		});
	$('#cal_event_create .create_button').button({
		text : true,
		icons : {
			primary : "ui-icon-check"
		}
	});
	$('#cal_event_create').ajaxForm({
		target : '#confirm_dialog_content',
		beforeSubmit: function(arr, form, options) {
			$('#flash').hide();
		},
		success: function(responseText, statusText, xhr) {
			console.log("search for '<div id=\"flash\"><div class=\"error\">' tag...");
			var error = $('<div/>').append(responseText).find('#flash div.error');
			if (error.length) {
				// keep '#confirm_dialog' opened
				console.log("ERROR: don't update the cal_event list.");
			} else {
				var event_obj = jQuery.parseJSON(responseText),
					start = $.fullCalendar.parseISO8601(event_obj.start);
				console.log("OK, update the cal_event list but don't select any cal_event...");
				console.log("start: " + start.toISOString());
				$('#confirm_dialog').dialog("close");
				$('#calendar')
					.fullCalendar('renderEvent', event_obj)
					.fullCalendar('gotoDate', start);
			}
		}
	});
</script>
