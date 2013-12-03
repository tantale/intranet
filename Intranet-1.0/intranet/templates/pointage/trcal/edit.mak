# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.trcal.edit
:date: 2013-09-22
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%! import json %>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if flash:
	${flash | n}
%endif
<form id="cal_event_update" class="ui-widget"
	action="${tg.url('./{uid}'.format(uid=values['uid']))}"
	method="post" enctype="multipart/form-data">
##
## Hidden field for PUT method
##
	<p style="display: none; visibility: hidden;">
	<input name="tz_offset" type="hidden" value="${tz_offset}" />
	<input type="hidden" name="_method" value="PUT" />
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
	<p><label for="cal_event_update__event_start">Date / Heure :</label>
		<input id="cal_event_update__event_start" type="datetime-local" name="event_start"
			value="${values.get('event_start')}"
			title="Date (et heure) du pointage (requis)" />
	%if 'event_start' in form_errors:
	<span class="error">${form_errors['event_start']}</span>
	%endif
	</p>

	<p><label for="cal_event_update__event_duration">Durée (h) :</label>
		<input id="cal_event_update__event_duration" type="number" name="event_duration"
			min="0.25" max="12" step="0.25"
			value="${values.get('event_duration')}"
			placeholder="1"
			title="Durée en heure, ex. : 1,50 pour 1h30 (requis)" />
	%if 'event_duration' in form_errors:
	<span class="error">${form_errors['event_duration']}</span>
	%endif
	</p>
	
	<p><label for="cal_event_update__comment">Commentaire :</label>
		<textarea id="cal_event_update__comment" name="comment"
			rows="4" cols="50"
			placeholder="Commentaire (facultatif)"
			title="Commentaire (optionnel)">${values.get('comment')}</textarea>
	%if 'comment' in form_errors:
	<span class="error">${form_errors['comment']}</span>
	%endif
	</p>
</form>

<form id="cal_event_delete" class="minimal_form"
	action="${tg.url('./{uid}'.format(uid=values['uid']))}"
	method="post">
	<p style="display: none; visibility: hidden;">
	<input type="hidden" name="_method" value="DELETE" />
	</p>
</form>

<script type='text/javascript'>
	"use strict";
	/*global $*/
	$('#cal_event_update').ajaxForm({
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
				var updated_event = jQuery.parseJSON(responseText),
					calendar = $('#calendar'), event_list, event;
				$('#confirm_dialog').dialog("close");
				event_list = calendar.fullCalendar('clientEvents', updated_event.id);
				event = event_list[0];
				event.start = updated_event.start;
				event.end = updated_event.end;
				event.comment = updated_event.comment;
				calendar.fullCalendar('updateEvent', event);
			}
		}
	});
	$('#cal_event_delete').ajaxForm({
		target : '#confirm_dialog_content',
		beforeSubmit: function(arr, form, options) {
			$('#flash').hide();
		},
		success: function(responseText, statusText, xhr) {
			var deleted_event = jQuery.parseJSON(responseText);
			$('#confirm_dialog').dialog("close");
			$('#calendar').fullCalendar('removeEvents', deleted_event.id);
		}
	});
</script>
