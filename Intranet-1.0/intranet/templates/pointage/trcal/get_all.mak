# -*- coding: utf-8 -*-
## tz_offset=tz_offset,
## cal_start=cal_start,
## cal_end=cal_end,
## cal_curr=cal_curr,
## start_date=start_date,
## end_date=end_date,
## employee=employee,
## employee_list=employee_list
<%! import json %>
<div id='caltoolbar'>
<%
if employee is not None and employee.photo_path:
	img_src = employee.photo_path
	img_alt = employee.employee_name + " - Photo"
else:
	img_src = tg.url('/images/silhouette.min.png')
	img_alt = "Silhouette"
%>\

## -- Display the "Control recorded times" button to the right
%if employee:
<form id="ctrl_rec_times" class="inline_form" style="float: right;"
	action="${tg.url('./ctrl_rec_times')}" method="get">
	<input type="hidden" name="employee_uid" value="${employee.uid}"/>
	<input type="hidden" name="week_start"/>
	<input type="hidden" name="week_end"/>
	<button id="ctrl_rec_times__ctrl" type="submit" class="ctrl_button"
		title="Contrôler les pointages de la semaine">Contrôler les pointages</button></td>
</form>
%endif

## -- Display the list of employees
<form id="employee_refresh" class="inline_form"
	action="${tg.url('./get_all/')}" method="get">
	<p><img class="valignMiddle picture_box_inner_min"
			id="employee_refresh__picture"
			alt="${img_alt}"
			src="${img_src}" />
		%if employee:
		<select id="employee_refresh__select" name="employee_uid"
			class="ui-widget ui-state-default ui-corner-all"
			title="Liste des employés">
			%for option in employee_list:
			%if option.uid == employee.uid:
			<option selected="selected"
				value="${option.uid}">${option.employee_name}</option>
			%else:
			<option
				value="${option.uid}">${option.employee_name}</option>
			%endif
			%endfor
		</select>
		%else:
		<select id="employee_refresh__select" disabled="disabled"
			class="ui-widget ui-state-default ui-corner-all"
			title="Aucun employée en activité"></select>
		%endif
		<input type="hidden" name="cal_start" value="${cal_start}" />
		<input type="hidden" name="cal_end" value="${cal_end}" />
		<input type="hidden" name="cal_curr" value="${cal_curr}" />
		<button id="employee_refresh__refresh" type="submit" class="refresh_button"
			title="Mettre à jour le calendrier des pointages">Mettre à jour</button></td>
	</p>
</form>
<div style="ui-helper-clearfix"></div>
</div>
<div id='calendar'><!-- calendar placeholder --></div>
<%
events_url = tg.url('./events', dict(employee_uid=employee.uid))
events_url_json = json.dumps(events_url)

new_url = tg.url('./new', dict(employee_uid=employee.uid))
new_url_json = json.dumps(new_url)

edit_url = tg.url('./edit')
edit_url_json = json.dumps(edit_url)

event_drop_url = tg.url('./event_drop')
event_drop_url_json = json.dumps(event_drop_url)

event_resize_url = tg.url('./event_resize')
event_resize_url_json = json.dumps(event_resize_url)

cal_curr_json = json.dumps(cal_curr)
%>\
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$('#employee_refresh').ajaxForm({
		target : '#calendar_content',
		beforeSubmit: function(arr, $form, options) {
			$('#flash').hide();
		}
	});
	$('#employee_refresh .refresh_button').button({
		text : false,
		icons : {
			primary : "ui-icon-refresh"
		}
	});
	$('#employee_refresh__select').change(function(){
		$('#employee_refresh').submit();
	});
##
## -- Display the "Control recorded times" button to the right
%if employee:
	$('#ctrl_rec_times .ctrl_button').button({
		text : true,
		icons : {
			primary : "ui-icon-check"
		}
	});
	$('#ctrl_rec_times').submit(function(event){
		// -- Compute de start/end dates of the week (or month)
		var calendar = $('#calendar'), // fullCalendar object
			view = calendar.fullCalendar('getView'), // viewObject
			week_start = view.visStart,
			week_end = view.visEnd;
		if (view.name === "basicDay" || view.name === "agendaDay") {
			var firstDay = calendar.fullCalendar('option', 'firstDay'), // int
				days = (week_start.getDay() === 0) ?
						(7 - firstDay) % 7 :
						week_start.getDay() - firstDay;
			week_start = view.visStart;
			week_start.setDate(week_start.getDate() - days); // Monday
			week_end = new Date(week_start);
			week_end.setDate(week_end.getDate() + 7);
		}
		$('#ctrl_rec_times input[name=week_start]').val(week_start.getTime() / 1000);
		$('#ctrl_rec_times input[name=week_end]').val(week_end.getTime() / 1000);
		// event.preventDefault();
	});
	$('#ctrl_rec_times').ajaxForm({
		target : '#confirm_dialog_content',
		beforeSubmit: function(arr, $form, options) {
			$('#flash').hide();
		},
		success: function(responseText, statusText, xhr) {
			$('#confirm_dialog').dialog({
				width: 	620,
				height: 500,
				buttons: {
					"OK": function() {
						$(this).dialog("close");
					}
				},
				title: "Contrôle des pointages",
				close: function() {
				}
			}).dialog("open");
		},
		error: function() {
			var title = "Erreur de connexion HTTP",
				text = "Impossible contrôler les événements\u00a0!";
			display_err_dialog(title, text);
        }
	});
%endif

	function load_order_list(cal_start, cal_end) {
		if (!cal_start || !cal_end) {
			var cal_curr = new Date(), y = cal_curr.getFullYear(), m = cal_curr.getMonth();
			cal_start = new Date(y, m, 1);
			cal_end = new Date(y, m + 1, 1);
		}
		$('#order_get_all input[name=cal_start]').val(cal_start.getTime() / 1000);
		$('#order_get_all input[name=cal_end]').val(cal_end.getTime() / 1000);
		$('#order_get_all').submit();
	}
	
	function load_employee_list(cal_start, cal_end, cal_curr) {
		if (!cal_start || !cal_end || !cal_curr) {
			cal_curr = new Date(), y = cal_curr.getFullYear(), m = cal_curr.getMonth();
			cal_start = new Date(y, m, 1);
			cal_end = new Date(y, m + 1, 1);
		}
		$('#employee_refresh input[name=cal_start]').val(cal_start.getTime() / 1000);
		$('#employee_refresh input[name=cal_end]').val(cal_end.getTime() / 1000);
		$('#employee_refresh input[name=cal_curr]').val(cal_curr.getTime() / 1000);
		// $('#employee_refresh').submit();
	}
	
	function on_events_load(start_date, end_date, callback) {
		var curr_date = $('#calendar').fullCalendar('getDate');
		$.ajax({
            url: ${events_url_json|n},
            dataType: 'json',
            data: {
                start: Math.round(start_date.getTime() / 1000),
                end: Math.round(end_date.getTime() / 1000)
            },
            success: function(events) {
                callback(events);
                load_order_list(start_date, end_date);
                load_employee_list(start_date, end_date, curr_date);
            },
			error: function() {
				callback();
				var title = "Erreur de connexion HTTP",
					text = "Impossible de récupérer les événements\u00a0!";
				display_err_dialog(title, text);
            }
        });
	}
	
	function on_event_render(event, element, view) {
		var start_date = $.fullCalendar.parseDate(event.start),
			end_date = $.fullCalendar.parseDate(event.end),
			duration = Math.floor((end_date - start_date) / 36000.0);
		element.attr('title', event.comment).find('.fc-event-time')
			.text(duration).css('padding-left: .5em;');
	}
	
	function on_event_drop(event, dayDelta, minuteDelta, allDay, revertFunc, jsEvent, ui, view) {
    	if (allDay) {
    		console.info("Please, this event ins't a all day event!");
    		revertFunc();
    	} else {
    		$.ajax({
    			type: "GET",
    			url: ${event_drop_url_json|n},
    			data: {
    				// id = 'cal_event_###'
    				uid: event.id.split('_')[2],
    				day_delta: dayDelta,
    				minute_delta: minuteDelta
    			},
    			success: function(){
		    		$('#calendar').fullCalendar('gotoDate', event.start);
    			},
    			error: function() {
    				revertFunc();
    				var title = "Erreur de connexion HTTP",
    					text = "Impossible de mettre à jour l\u2019événement\u00a0!";
    				display_err_dialog(title, text);
    	        }
    		});
    	}
    }
	
	function on_event_resize(event, dayDelta, minuteDelta, revertFunc, jsEvent, ui, view) {
		$.ajax({
			type: "GET",
			url: ${event_resize_url_json|n},
			data: {
				// id = 'cal_event_###'
				uid: event.id.split('_')[2],
				day_delta: dayDelta,
				minute_delta: minuteDelta
			},
			success: function(){
				console.info("Event duration succefully updated.");
	    		console.info("gotoDate: " + event.start.toISOString());
	    		$('#calendar').fullCalendar('gotoDate', event.start);
	    		if (dayDelta) {
	    			$('#calendar').fullCalendar('refetchEvents');
	    		}
			},
			error: function() {
				revertFunc();
				var title = "Erreur de connexion HTTP",
					text = "Impossible de mettre à jour la durée de l\u2019événements\u00a0!";
				display_err_dialog(title, text);
	        }
		});
    }
	
	function open_new_event_dialog(event_td, date, allDay) {
		var selected = $('ul.selectable .ui-selected');
		if (selected.length) {
			console.debug('------- open_new_event_dialog');
			var url = ${new_url_json|n}, // contains: employee_uid
				tz_offset = date.getTimezoneOffset(), // UTC offset
				order_phase_uid =  selected.attr('id').split('_')[3];
			console.debug('------- tz_offset: ' + tz_offset.toString());

			url += "&order_phase_uid=" + order_phase_uid;
			url += "&date=" + date.toISOString();
			url += "&allDay=" + allDay;
			url += "&tz_offset=" + tz_offset.toString();

			$('#confirm_dialog_content').load(url);
			$('#confirm_dialog').dialog({
				width: 	540,
				height: 370,
				buttons: {
					"Ajouter": function() {
						$('#cal_event_create').submit();
					},
					"Annuler": function() {
						$(this).dialog("close");
					}
				},
				title: "Saisir un pointage",
				close: function() {
					console.info('gotoDate: '+ date.toISOString());
					$('#calendar').fullCalendar('gotoDate', date);
					console.debug('------- /open_new_event_dialog');
				}
			}).dialog("open");
		} else {
			var msg = $('<div id="flash"></div>')
				.append($('<div class="error"/>')
						.text("Veuillez sélectionner une phase dans la liste des commandes\u00a0!"));
			$('#confirm_dialog_content').empty().append(msg);
			$('#confirm_dialog').dialog({
				width: 	400,
				height: 200,
				buttons: {
					"OK": function() {
						$(this).dialog("close");
					}
				},
				title: "Aucune phase sélectionnée",
				close: function() {
					console.info('gotoDate: '+ date.toISOString());
					$('#calendar').fullCalendar('gotoDate', date);
				}
			}).dialog("open");
		}
	}
	
	function open_edit_event_dialog(event_div, event, view) {
		// 'this' is set to the event's <div> element.
		var uid = event.id.split('_')[2], // id = 'cal_event_###'
			tz_offset = event.start.getTimezoneOffset(),
			url = ${edit_url_json|n} + "?uid=" + uid;
			url += "&tz_offset=" + tz_offset;
		$('#confirm_dialog_content').load(url);
		$('#confirm_dialog').dialog({
			width: 	540,
			height: 370,
			buttons: {
				"Modifier": function() {
					$('#cal_event_update').submit();
				},
				"Supprimer": function() {
					$('#cal_event_delete').submit();
				},
				"Annuler": function() {
					$(this).dialog("close");
				}
			},
			title: "Modifier un pointage",
			close: function() {
				console.info('gotoDate: '+ event.start.toISOString());
				$('#calendar').fullCalendar('gotoDate', event.start);
			}
		}).dialog("open");
	}
	
	function display_err_dialog(title, text) {
		var msg = $('<div id="flash"></div>') //
			.append($('<div class="error"/>').text(text));
		$('#confirm_dialog_content').empty().append(msg);
		$('#confirm_dialog').dialog({
			width: 	400,
			height: 200,
			buttons: {
				"OK": function() {
					$(this).dialog("close");
				}
			},
			title: title
		}).dialog("open");
	}
	
	var curr_date = new Date(parseInt(${cal_curr_json|n}, 10) * 1000);
	
	$('#calendar').fullCalendar(
			{
				year : curr_date.getFullYear(),
				month : curr_date.getMonth(),
				day : curr_date.getDay(),
				theme : true,
				header : {
					left : 'month,agendaWeek,agendaDay',
					center : 'title',
					right : 'today prev,next'
				},
				editable : true,
				eventStartEditable : true,
				eventDurationEditable : true,
				firstDay : 1, // Monday
				firstHour : 8, // 8h
				weekends : true, // 7 days
				ignoreTimezone: false,

				allDayText : 'Toute la journ\u00e9e',
				axisFormat : 'H:mm',
				timeFormat : {
					agenda : 'H:mm{ - H:mm}',
					'' : 'H(:mm)'
				},
				columnFormat : {
					month : 'ddd',
					week : 'ddd d/M',
					day : 'dddd d/M'
				},
				titleFormat : {
					month : 'MMMM yyyy',
					week : "d[ MMM][ yyyy]{ '&#8212;' d MMM yyyy}",
					day : 'dddd d MMM yyyy'
				},
				monthNames : [ 'Janvier', 'F\u00e9vrier', 'Mars', 'Avril',
						'Mai', 'Juin', 'Juillet', 'Ao\u00fbt', 'Septembre',
						'Octobre', 'Novembre', 'D\u00e9cembre' ],
				monthNamesShort : [ 'Jan.', 'F\u00e9v.', 'Mar.', 'Avr.', 'Mai',
						'Juin', 'Juil.', 'Ao\u00fbt', 'Sept.', 'Oct.', 'Nov.',
						'D\u00e9c.' ],
				dayNames : [ 'Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi',
						'Vendredi', 'Samedi' ],
				dayNamesShort : [ 'Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven',
						'Sam' ],
				buttonText : {
					prev : "<span class='fc-text-arrow'>&lsaquo;</span>",
					next : "<span class='fc-text-arrow'>&rsaquo;</span>",
					prevYear : "<span class='fc-text-arrow'>&laquo;</span>",
					nextYear : "<span class='fc-text-arrow'>&raquo;</span>",
					today : 'Aujoud\u2019hui',
					month : 'mois',
					week : 'semaine',
					day : 'jour'
				},
				droppable: true,
			    eventDrop: on_event_drop,
				drop: function(date, allDay) {
					// 'this' is set to the <td> of the clicked day.
					open_new_event_dialog(this, date, allDay);
			    },
				dayClick: function(date, allDay, jsEvent, view) {
					// 'this' is set to the <td> of the clicked day.
					open_new_event_dialog(this, date, allDay);
			    },
			    eventClick: function(event, jsEvent, view) {
			    	// 'this' is set to the event's <div> element
					open_edit_event_dialog(this, event, view);
			    },
			    eventResize: on_event_resize,
				eventSources: [{
					// http://arshaw.com/fullcalendar/docs/event_data/events_function/
					events: on_events_load
					}],
				eventRender : on_event_render
			});

	$('body').layout({
		north__size : "auto",
		north__closable : false,
		north__resizable : false,
		north__slidable : false,
		north__spacing_open : 0,
		north__spacing_closed : 0,

		west__size : 260,
		west__minSize : 230,
		west__maxSize : 500,

		center__onresize : function() {
			$('#calendar').fullCalendar('render');
		}
	});
	
	$('#calendar').fullCalendar('render');
</script>
