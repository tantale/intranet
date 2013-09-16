"use strict";
/*jslint browser: true, devel: true, es5: false, plusplus: true, unparam: true, white: true */
/*global $*/

function on_accordion_refresh(responseText, statusText, xhr) {
	var index, search_list = [], searchable_node_list = $("#accordion .searchable"), keyword;
	for (index = 0; index < searchable_node_list.length; ++index) {
		keyword = $.trim($(searchable_node_list[index]).text());
		search_list.push(keyword);
	}
	$('#employee_get_all__keyword').autocomplete({
		source : search_list
	});
	$('#employee_get_all__keyword').autocomplete('close');
}

$(function() {
	$('body').layout({
		north__size : "auto",
		north__closable : false,
		north__resizable : false,
		north__slidable : false,
		north__spacing_open : 0,
		north__spacing_closed : 0,

		west__size : 260,
		west__minSize : 230,
		west__maxSize : 500
	});
});

$('#employee_new').ajaxForm({
    target: '#employee_content',
    success: function(responseText, statusText, xhr) {
        alert('status: ' + statusText + '\n\nresponseText: \n' + responseText +
			'\n\nThe output div should have already been updated with the responseText.'); 
    	$("#accordion").accordion("option", "active", false);
    }
});
