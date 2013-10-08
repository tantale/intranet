# -*- coding: utf-8 -*-
## cal_date=cal_date,
## start_date=start_date,
## end_date=end_date,
## employee=employee,
## employee_list=employee_list,
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

<form id="employee_refresh" class="inline_form"
	action="${tg.url('/pointage/trcal/get_all/')}" method="get">
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
		<input type="hidden" name="cal_date" value="${cal_date}" />
		<button id="employee_refresh__refresh" type="submit" class="refresh_button"
			title="Mettre à jour le calendrier des pointages">Mettre à jour</button></td>
	</p>
</form>
</div>
<div id='calendar'><!-- calendar placeholder --></div>
<%
events_url = tg.url('/pointage/trcal/events', dict(employee_uid=employee.uid))
events_url_json = json.dumps(events_url)

new_url = tg.url('/pointage/trcal/new', dict(employee_uid=employee.uid))
new_url_json = json.dumps(new_url)
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
	
	function open_new_event_dialog(calendar, date, allDay) {
		if (allDay) {
			console.debug("allDay == true => set hour to 8 O'clock...")
			date.setHours(8, 0, 0);
			console.debug("date: " + date.toISOString());
		}
		var time_zone_offset = date.getTimezoneOffset(),
			local_date = new Date(date.getTime() - (time_zone_offset / 60) * 3600000);
		console.debug("local_date: " + local_date.toISOString());

		var url = ${new_url_json|n},
			iso = local_date.toISOString().replace(/\.\d+Z$/, "");
		url += "&event_start=" + iso;
		url += "&time_zone_offset=" + time_zone_offset.toString();
		
		var selected = $('ul.selectable .ui-selected');
		if (selected.length) {
			console.debug("Selected: " + selected.attr('id'));
			// order_phase_li_###
			var order_phase_uid =  selected.attr('id').split('_')[3];
			url += "&order_phase_uid=" + order_phase_uid;
			$('#confirm_dialog_content').load(url);
			$('#confirm_dialog').dialog({
				width: 	600,
				height: 400,
				buttons: {
					"Ajouter": function() {
						$('#cal_event_create').submit();
					},
					"Annuler": function() {
						$(this).dialog("close");
					}
				},
				title: "Saisir un pointage pour le " + local_date.getDate() + "/" + local_date.getMonth(),
				close: function() {
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
				title: "Aucune phase sélectionnée"
			}).dialog("open");
		}
	}
	
	
	$('#calendar').fullCalendar(
			{
				theme : true,
				header : {
					left : 'month,agendaWeek,agendaDay',
					center : 'title',
					right : 'today prev,next'
				},
				editable : true,
				firstDay : 1, // Monday
				firstHour : 8, // 8h
				weekends : true, // 7 days

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
				drop: function(date, allDay) {
					open_new_event_dialog(this, date, allDay);
			    },
				dayClick: function(date, allDay, jsEvent, view) {
					open_new_event_dialog(this, date, allDay);
			    },
				eventSources: [{
					url: ${events_url_json|n},
					error: function() {
						var msg = $('<div id="flash"></div>')
							.append($('<div class="error"/>')
									.text("Impossible de récupérer les événements\u00a0!"));
						$('#confirm_dialog_content').empty().append(msg);
						$('#confirm_dialog').dialog({
							width: 	400,
							height: 200,
							buttons: {
								"OK": function() {
									$(this).dialog("close");
								}
							},
							title: "Erreur interne"
						}).dialog("open");
		            },
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
