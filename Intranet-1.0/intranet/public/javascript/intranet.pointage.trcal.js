"use strict";
/*jslint browser: true, devel: true, es5: false, plusplus: true, unparam: true, white: true */
/*global $*/


function on_accordion_refresh(responseText, statusText, xhr) {
	var index, search_list = [], searchable_node_list = $("#accordion .searchable"), keyword;
	for (index = 0; index < searchable_node_list.length; ++index) {
		keyword = $.trim($(searchable_node_list[index]).text());
		search_list.push(keyword);
	}
	$('#order_get_all__keyword').autocomplete({
		source : search_list
	});
	$('#order_get_all__keyword').autocomplete('close');
}

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

});
