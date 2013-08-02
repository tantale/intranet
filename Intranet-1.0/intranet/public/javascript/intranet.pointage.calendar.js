/**
 * Change the rendering of an event in the calendar.
 * 
 * Display the event duration in 1/100th hours.
 * 
 * @param event
 *            Event object
 * @param element
 *            jQuery element
 * @param view
 */
function on_event_render(event, element, view) {
	var start_date = $.fullCalendar.parseDate(event.start), end_date = $.fullCalendar
			.parseDate(event.end), duration;
	duration = (end_date - start_date) / 36000.0;
	element.attr('title', event.description).find('.fc-event-time').text(
			duration).css('padding-left: .5em;');
}

$(function() {

	$(".editButton").button({
		text : true
	});

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
				events : [ {
					title : 'DUJARDIN - Table - Phase 1',
					start : '2013-07-27T08:00',
					end : '2013-07-27T12:00',
					allDay : false,
					editable : true,
					color : 'red',
					textColor : 'black',
					description : 'Phase 1 termin\u00e9e'
				}, {
					title : 'LEFEVRE - Cuisine - Phase 3',
					start : '2013-07-28T14:00',
					end : '2013-07-28T16:30',
					allDay : false,
					editable : true,
					color : 'yellow',
					textColor : 'black',
					description : 'Phase 3 en cours'
				} ],
				eventRender : on_event_render
			});

	$('#employee_carousel')
			.carousel(
					{
						// itemsPerPage: 3, // number of items to show on each
						// page
						// itemsPerTransition: 1, // number of items moved with
						// each transition
						noOfRows : 1, // number of rows (see demo)
						nextPrevLinks : true, // whether next and prev links
						// will be included
						pagination : false, // whether pagination links will be
						// included
						speed : 'normal', // animation speed
						easing : 'swing', // supports the jQuery easing plugin
						insertPrevAction : function() {
							return $(
									'<a href="#" class="rs-carousel-action rs-carousel-action-prev '
											+ 'ui-button ui-widget ui-state-default ui-corner-all '
											+ 'ui-button-icon-only" role="button" aria-disabled="false" '
											+ 'title="Pr\u00e9c\u00e9dent">'
											+ '<span class="ui-button-icon-primary ui-icon ui-icon-circle-triangle-w">'
											+ '</span>'
											+ '<span class="ui-button-text">'
											+ 'Pr\u00e9c\u00e9dent' + '</span>'
											+ '</a>').appendTo(this);
						},
						insertNextAction : function() {
							return $(
									'<a href="#" class="rs-carousel-action rs-carousel-action-next '
											+ 'ui-button ui-widget ui-state-default ui-corner-all '
											+ 'ui-button-icon-only" role="button" aria-disabled="false" '
											+ 'title="Suivant">'
											+ '<span class="ui-button-icon-primary ui-icon ui-icon-circle-triangle-e">'
											+ '</span>'
											+ '<span class="ui-button-text">'
											+ 'Suivant' + '</span>' + '</a>')
									.appendTo(this);
						}
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

});
