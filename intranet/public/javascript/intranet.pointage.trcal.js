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

$(function() {

	$(".editButton").button({
		text : true
	});

});
