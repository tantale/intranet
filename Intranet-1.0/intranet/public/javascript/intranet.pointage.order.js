"use strict";
/*jslint browser: true, devel: true, es5: false, plusplus: true, unparam: true, white: true */
/*global $*/

//function find_accordion_active(uid) {
//	var index, search_id = "order_" + uid, searchable_node_list = $("#accordion .searchable");
//	for (index = 0; index < searchable_node_list.length; ++index) {
//		var curr_id = $(searchable_node_list[index]).attr('id');
//		if (curr_id === search_id) {
//			return index;
//		}
//	}
//	return -1;
//}

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

function refresh_accordion(uid, order_ref) {
	var keyword = $('#order_get_all__keyword').val();
	if (uid) {
		$("#order_get_all input[name=uid]").val(uid);
	} else {
		$("#order_get_all input[name=uid]").val("");
	}
	if (order_ref) {
		$("#order_get_all input[name=order_ref]").val(order_ref);
	} else {
		$("#order_get_all input[name=order_ref]").val("");
	}
	$("#order_get_all").submit();
}

$(function() {
	$(".editInPlace").editInPlace({
		url : "http://edit"
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
		west__maxSize : 500
	});
});

$('#order_new').ajaxForm({
    target: '#order_content',
    success: function(responseText, statusText, xhr) {
        alert('status: ' + statusText + '\n\nresponseText: \n' + responseText +
			'\n\nThe output div should have already been updated with the responseText.'); 
    	$("#accordion").accordion("option", "active", false);
    }
});
